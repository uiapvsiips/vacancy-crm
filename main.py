from flask import Flask, request, flash, render_template, redirect, url_for, session

import db_processing
from celery_worker import send_email
import alchemy_db
from mongo_db import Mongo_process
from email_process import EmailWorker
from models import Vacancy, Event, EmailCredentials, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET'])
@app.route('/user/', methods=['GET'])
def main_page():
    user_id = session.get('user_id', None)
    if user_id:
        user = alchemy_db.db_session.query(User).filter(User.id==user_id).first()
        return f"Hello, {user.name}. This is your dashboard!"
    return redirect(url_for('get_login_page'))


@app.route('/user/calendar/', methods=['GET'])
def get_user_calendar():
    return "Get your Calendar!"


@app.route('/user/settings/', methods=['GET', 'PUT'])
def get_user_settings():
    return "Get your settings!"


@app.route('/user/templates/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_user_templates():
    return "Get your templates!"


@app.route('/user/documents/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_user_docs():
    return "Get your documents!"


@app.route('/vacancy/history/', methods=['GET'])
def get_user_vacancies_history():
    return "Get your vacancies history!"

@app.route('/registration', methods=['GET'])
def get_reg_page():
    return render_template('reg_page.html')

@app.route('/registration', methods=['POST'])
def post_reg_page():
    form = request.form
    name = form.get('name')
    email = form.get('email')
    password = generate_password_hash(form.get('password'), method='sha256')
    if not alchemy_db.db_session.query(User).filter(User.email==email).first():
        new_user = User(name, email, password)
        alchemy_db.db_session.add(new_user)
        alchemy_db.db_session.commit()
        session['user_id'] = new_user.id
        return redirect(url_for('main_page'))




@app.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])
def post_login_page():
    form = request.form
    login = form.get('login')
    password = form.get('password')
    user = alchemy_db.db_session.query(User).filter(User.email==login).first()
    if user is None:
        return redirect(url_for('get_login_page'))
    if check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(url_for('main_page'))
    else:
        flash('Incorrect login or password!')

@app.get('/user/mail/')
def get_user_mail():
    user = get_current_user()
    if user is None:
        return redirect(url_for('get_login_page'))
    email_creds = alchemy_db.db_session.query(EmailCredentials).where(EmailCredentials.user_id == user.id).first()
    email = EmailWorker(email_creds.email, email_creds.login, email_creds.password,
                        email_creds.smtp_server, email_creds.smtp_port,
                        email_creds.pop_server, email_creds.pop_port,
                        email_creds.imap_server, email_creds.imap_port)
    emails = []
    if email.imap_server:
        emails = email.get_emails([1, 2, 3], protocol='imap')
    else:
        emails = email.get_emails([1, 2, 3], protocol='pop3')
    return render_template('email_page.html', emails=emails)


@app.post('/user/mail/')
def post_user_mail():
    user = get_current_user()
    if user is None:
        return redirect(url_for('get_login_page'))
    email_creds = alchemy_db.db_session.query(EmailCredentials).where(EmailCredentials.user_id == user.id).first()
    creds_dict = alchemy_db.row2dict(email_creds)
    creds_dict.pop('id')
    creds_dict.pop('user_id')
    send_email.apply_async(args=[creds_dict, request.form.get('subject'), request.form.get('message'), request.form.get('to')])
    flash('Лист відправлено успішно', 'OK')
    email = EmailWorker(email_creds.email, email_creds.login, email_creds.password,
                        email_creds.smtp_server, email_creds.smtp_port,
                        email_creds.pop_server, email_creds.pop_port,
                        email_creds.imap_server, email_creds.imap_port)
    emails = []
    if email.imap_server:
        emails = email.get_emails([1, 2, 3], protocol='imap')
    else:
        emails = email.get_emails([1, 2, 3], protocol='pop3')
    return render_template('email_page.html', emails=emails)


@app.get('/vacancy/')
def get_user_vacancies():
    user = get_current_user()
    if user is None:
        return redirect(url_for('get_login_page'))
    vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user.id).all()
    contacts = []
    with Mongo_process() as mongo:
        for vacancy in vacancies:
            [contacts.append(mongo.get_doc(contact_id)) for contact_id in vacancy.contacts_ids.split(',')]
    return render_template('vacancy_list.html', vacancies=vacancies)
    #return render_template('vacancy_add.html', vacancies=vacancies)


@app.post('/vacancy/')
def post_new_user_vacancies():
    user = get_current_user()
    if user is None:
        return redirect(url_for('get_login_page'))
    alchemy_db.init_db()
    form = dict(request.form)
    if not form['company'] or not form['name'] or not form['description'] or not form['position_name']:
        flash('Виникла помилка. Всі поля позначені * повинні бути заповнені!', 'error')
    else:
        contacts = {"name": form.get("name"), "email": form.get("email"), "phone_number": form.get("phone_number")}
        contatct_id = None
        with Mongo_process() as mongo:
            contatct_id = str(mongo.insert_doc(contacts))
        current_vacancy = Vacancy(form.get('position_name'), form.get('company'), form.get('description'),
                                  contatct_id, user.id, comment=form.get('comment'))
        alchemy_db.db_session.add(current_vacancy)
        alchemy_db.db_session.commit()
        flash('Дані про вакансію успішно додано', 'OK')
    vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user.id).all()
    return render_template('vacancy_list.html', vacancies=vacancies)


@app.get('/vacancy/<int:vacancy_id>/')
def get_user_vacancy_by_id(vacancy_id):
    user = get_current_user()
    if user is None:
        return redirect(url_for('get_login_page'))
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id, Vacancy.user_id==user.id).first()
    if vacancy is None:
        return redirect(url_for('get_user_vacancies'))
    contacts = []
    with Mongo_process() as mongo:
        [contacts.append(mongo.get_doc(contact_id)) for contact_id in vacancy.contacts_ids.split(',')]
    vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user.id).all()
    return render_template('vacancy_page1.html', vacancy=vacancy, vacancies=vacancies, contacts = contacts)


@app.post('/vacancy/<int:vacancy_id>/')
def update_some_vacancy(vacancy_id):
    form = dict(request.form)
    vacancy = alchemy_db.db_session.query(Vacancy.contacts_ids, Vacancy.id).filter(Vacancy.id == vacancy_id).first()

    edited_contacts = {"name": form.get("name"), "email": form.get("email"), "phone_number": form.get("phone_number")}
    contacts = []

    with Mongo_process() as mongo:
        mongo.update_doc(vacancy.contacts_ids, edited_contacts)
        [contacts.append(mongo.get_doc(contact_id)) for contact_id in vacancy.contacts_ids.split(',')]
    alchemy_db.db_session.query(Vacancy).filter(Vacancy.id == vacancy_id).update(
        {Vacancy.position_name: form.get('position_name'),
         Vacancy.company: form.get('company'),
         Vacancy.description: form.get('description'),
         Vacancy.contacts_ids: form.get('contacts_ids'),
         Vacancy.comment: form.get('comment'),
         Vacancy.status: form.get('status')
         })
    alchemy_db.db_session.commit()
    flash('Інформація по вакансії успішно відредагована', 'OK')
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).first()
    # return render_template('vacancy_page.html', vacancy=vacancy, contacts = contacts)
    return render_template('vacancy_page1.html', vacancy=vacancy, contacts = contacts)


@app.get('/vacancy/<int:vacancy_id>/events/')
def get_user_events(vacancy_id):
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all().first()
    events = alchemy_db.db_session.query(Event).where(Event.vacancy_id == vacancy_id).all()
    return render_template('events_page.html', vacancy=vacancy, events=events)


@app.post('/vacancy/<int:vacancy_id>/events/')
def post_new_event_for_vacancy(vacancy_id):
    form = dict(request.form)
    if not form['title'] or not form['description'] or not form['due_to_date']:
        flash('Виникла помилка. Всі поля позначені * повинні бути заповнені!', 'error')
    else:
        current_event = Event(vacancy_id, form.get('description'),
                              form.get('title'),
                              form.get('due_to_date'))
        alchemy_db.db_session.add(current_event)
        alchemy_db.db_session.commit()
        flash('Інформація успішно додана', 'OK')
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all().first()
    events = alchemy_db.db_session.query(Event).where(Event.vacancy_id == vacancy_id).all()
    return render_template('events_page.html',
                           events=events,
                           vacancy=vacancy)


@app.get('/vacancy/<int:vacancy_id>/events/<event_id>/')
def get_event_for_vacancy_by_id(vacancy_id, event_id):
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all().first()
    event = alchemy_db.db_session.query(Event).where(Event.id == event_id).all().first()
    return render_template('one_event_page.html', event=event, vacancy=vacancy)


@app.post('/vacancy/<int:vacancy_id>/events/<int:event_id>/')
def update_some_event_for_vacancy(vacancy_id, event_id):
    form = dict(request.form)
    alchemy_db.db_session.query(Event).filter(Event.id == event_id).update(
        {Event.title: form.get('title'),
         Event.description: form.get('description'),
         Event.due_to_date: form.get('due_to_date'),
         Event.status: form.get('status')
         })
    alchemy_db.db_session.commit()
    flash('Інформація по подію успішно відредагована', 'OK')
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all().first()
    event = alchemy_db.db_session.query(Event).where(Event.id == event_id).first()
    return render_template('one_event_page.html', event=event, vacancy=vacancy)

def get_current_user():
    user_id = session.get('user_id', None)
    if not user_id:
        return None
    return alchemy_db.db_session.query(User).filter(User.id==user_id).first()

app.run(debug=True)

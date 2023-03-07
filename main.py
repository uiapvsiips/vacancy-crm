from flask import Flask, request, flash, render_template
from celery_worker import send_email
import alchemy_db
from email_process import EmailWorker
from models import Vacancy, Event, EmailCredentials

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# TODO delete user_id variable after doing user authorization
user_id = 1


@app.route('/', methods=['GET'])
@app.route('/user/', methods=['GET'])
def main_page():
    return "Hello, User. This is your dashboard!"


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


@app.get('/user/mail/')
def get_user_mail():
    email_creds = alchemy_db.db_session.query(EmailCredentials).where(EmailCredentials.user_id == user_id).first()
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
    email_creds = alchemy_db.db_session.query(EmailCredentials).where(EmailCredentials.user_id == user_id).first()
    send_email.apply_async(args=[email_creds, request.form.get('subject'), request.form.get('message'), request.form.get('to')])
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
    vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user_id).all()
    # return render_template('vacancy_list.html', vacancies=vacancies)
    return render_template('vacancy_add.html', vacancies=vacancies)


@app.post('/vacancy/')
def post_new_user_vacancies():
    alchemy_db.init_db()
    form = dict(request.form)
    if not form['company'] or not form['contacts_ids'] or not form['description'] or not form['position_name']:
        flash('Виникла помилка. Всі поля позначені * повинні бути заповнені!', 'error')
    else:
        current_vacancy = Vacancy(form.get('position_name'), form.get('company'), form.get('description'),
                                  form.get('contacts_ids'), user_id, comment=form.get('comment'))
        alchemy_db.db_session.add(current_vacancy)
        alchemy_db.db_session.commit()
        flash('Дані про вакансію успішно додано', 'OK')
        vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user_id).all()
    return render_template('vacancy_add.html',
                           vacancies=vacancies)


@app.get('/vacancy/<int:vacancy_id>/')
def get_user_vacancy_by_id(vacancy_id):
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all().first()
    vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user_id).all()
    return render_template('vacancy_page.html', vacancy=vacancy, vacancies=vacancies)
    # return render_template('vacancy_page1.html', vacancy=vacancy, vacancies=vacancies)


@app.post('/vacancy/<int:vacancy_id>/')
def update_some_vacancy(vacancy_id):
    form = dict(request.form)
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
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all().first()
    return render_template('vacancy_page.html', vacancy=vacancy)


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


app.run(debug=True)

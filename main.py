from flask import Flask, request, flash, render_template
import alchemy_db
from models import Vacancy, Event

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


@app.route('/user/mail/', methods=['GET'])
def get_user_mail():
    return "Get your Mail!"


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


@app.get('/vacancy/')
def get_user_vacancies():
    vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id==user_id).all()
    return render_template('vacancy_add.html', vacancies=vacancies)


@app.post('/vacancy/')
def post_new_user_vacancies():
    alchemy_db.init_db()
    form = dict(request.form)
    if not form['company'] or not form['contacts_ids'] or not form['description'] or not form['position_name']:
        flash('Виникла помилка. Всі поля позначені * повинні бути заповнені!', 'error')
    else:
        current_vacancy = Vacancy(form.get('position_name'), form.get('company'), form.get('description'), form.get('contacts_ids'), user_id, comment=form.get('comment'))
        alchemy_db.db_session.add(current_vacancy)
        alchemy_db.db_session.commit()
        flash('Дані про вакансію успішно додано', 'OK')
        vacancies = alchemy_db.db_session.query(Vacancy).where(Vacancy.user_id == user_id).all()
    return render_template('vacancy_add.html',
                           vacancies=vacancies)

@app.get('/vacancy/<int:vacancy_id>/')
def get_user_vacancy_by_id(vacancy_id):
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all()[0]
    return render_template('vacancy_page.html', vacancy=vacancy)


@app.post('/vacancy/<int:vacancy_id>/')
def update_some_vacancy(vacancy_id):
    form = dict(request.form)
    alchemy_db.db_session.query(Vacancy).filter(Vacancy.id==vacancy_id).update({Vacancy.position_name: form.get('position_name'),
                                                                                Vacancy.company: form.get('company'),
                                                                                Vacancy.description: form.get('description'),
                                                                                Vacancy.contacts_ids: form.get('contacts_ids'),
                                                                                Vacancy.comment: form.get('comment'),
                                                                                Vacancy.status: form.get('status')
                                                                                })
    alchemy_db.db_session.commit()
    flash('Інформація по вакансії успішно відредагована', 'OK')
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all()[0]
    return render_template('vacancy_page.html', vacancy=vacancy)

@app.get('/vacancy/<int:vacancy_id>/events/')
def get_user_events(vacancy_id):
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all()[0]
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
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all()[0]
    events = alchemy_db.db_session.query(Event).where(Event.vacancy_id == vacancy_id).all()
    return render_template('events_page.html',
                           events=events,
                           vacancy=vacancy)


@app.get('/vacancy/<int:vacancy_id>/events/<event_id>/')
def get_event_for_vacancy_by_id(vacancy_id, event_id):
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all()[0]
    event = alchemy_db.db_session.query(Event).where(Event.id == event_id).all()[0]
    return render_template('one_event_page.html', event=event, vacancy = vacancy)


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
    flash('Інформація по події успішно відредагована', 'OK')
    vacancy = alchemy_db.db_session.query(Vacancy).where(Vacancy.id == vacancy_id).all()[0]
    event = alchemy_db.db_session.query(Event).where(Event.id == event_id).all()[0]
    return render_template('one_event_page.html', event=event, vacancy=vacancy)


app.run(debug=True)

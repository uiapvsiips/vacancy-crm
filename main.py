from flask import Flask, request, flash, render_template
from db_processing import DB

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
    with DB() as db:
        vacancies = db.select_info('vacancy', conditions=f'user_id={user_id}')
    return render_template('vacancy_add.html', vacancies=vacancies)


@app.post('/vacancy/')
def post_new_user_vacancies():
    form = request.form
    with DB() as db:
        vacancies = db.select_info('vacancy', conditions=f'user_id={user_id}')
        if not form['company'] or not form['contacts_ids'] or not form['description'] or not form['pocition_name']:
            flash('Виникла помилка. Всі поля позначені * повинні бути заповнені!', 'error')
        else:
            db.insert_info('vacancy', request.form)
            flash('Дані про вакансію успішно додано', 'OK')
        return render_template('vacancy_add.html',
                               vacancies=vacancies)


@app.get('/vacancy/<int:vacancy_id>/')
def get_user_vacancy_by_id(vacancy_id):
    with DB() as db:
        vacancy = db.select_info('vacancy', conditions=f'id={vacancy_id}')[0]
    return render_template('vacancy_page.html', vacancy=vacancy)


@app.put('/vacancy/<int:vacancy_id>/')
def update_some_vacancy(vacancy_id):
    return f"Update your vacancie {vacancy_id}!"


@app.get('/vacancy/<int:vacancy_id>/events/')
def get_user_events(vacancy_id):
    with DB() as db:
        vacancy = db.select_info('vacancy', conditions=f'id={vacancy_id}')[0]
        events = db.select_info('event', conditions=f'vacancy_id={vacancy_id}')
    return render_template('events_page.html', vacancy=vacancy, events=events)


@app.post('/vacancy/<int:vacancy_id>/events/')
def post_new_event_for_vacancy(vacancy_id):
    form = dict(request.form)
    with DB() as db:
        events = db.select_info('event', conditions=f'vacancy_id={vacancy_id}')
        vacancy = db.select_info('vacancy', conditions=f'id={vacancy_id}')[0]
        if not form['title'] or not form['description'] or not form['due_to_date']:
            flash('Виникла помилка. Всі поля позначені * повинні бути заповнені!', 'error')
        else:
            form['vacancy_id'] = vacancy_id
            db.insert_info('event', form)
            flash('Інформація успішно додана', 'OK')
        return render_template('events_page.html',
                               events=events,
                               vacancy=vacancy)


@app.get('/vacancy/<int:vacancy_id>/events/<event_id>/')
def get_event_for_vacancy_by_id(vacancy_id, event_id):
    with DB() as db:
        event = db.select_info('event', conditions=f'id={event_id}')[0]
    return render_template('one_event_page.html', event=event)


@app.put('/vacancy/<int:id>/events/<int:event_id>/')
def update_some_event_for_vacancy(vacancy_id, event_id):
    return f"Update event {event_id} for vacancy {vacancy_id}!"


app.run(debug=True)

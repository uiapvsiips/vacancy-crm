from flask import Flask

app = Flask(__name__)
app.run()
list_of_vacancies = [
    {
     "id": 1,
     "creation_date": "20.01.2023", "status": 1,
     "company": "Some company2",
     "contacts_ids": [5,6],
     "description": "Vacancy description",
     "position_name": "Middle Python dev",
     "comment": "Good vacancy and company",
     "user_id": 1
     },
     {
     "id": 2,
     "creation_date": "28.01.2023", "status": 1,
     "company": "Some company3",
     "contacts_ids": [5,6],
     "description": "Vacancy description",
     "position_name": "Middle Python dev",
     "comment": "Good vacancy, bad company",
     "user_id": 1
     },
     {
     "id": 3,
     "creation_date": "23.01.2023", "status": 1,
     "company": "Some company4",
     "contacts_ids": [5,6],
     "description": "Vacancy description",
     "position_name": "Trainee Python dev",
     "comment": "Bad vacancy and company",
     "user_id": 1
     }
]

list_of_events = [
    {
    "id":1,
    "vacancy_id": 1,
    "description": "Some description",
    "event_date": "01.01.2023",
    "title": "Event title vacancy 3",
    "due_to_date": "01.02.2023",
    "status": 1
    },
    {
    "id":2,
    "vacancy_id": 2,
    "description": "Some description",
    "event_date": "29.01.2023",
    "title": "Event title vacancy 3",
    "due_to_date": "03.02.2023",
    "status": 1
    },
    {
    "id":3,
    "vacancy_id": 2,
    "description": "Some description",
    "event_date": "30.01.2023",
    "title": "Event title vacancy 3",
    "due_to_date": "05.02.2023",
    "status": 1
    },
]
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
    return "Get your vacancies!"


@app.post('/vacancy/')
def post_new_user_vacancies():
    return "Post new vacancy!"


@app.get('/vacancy/<int:vacancy_id>/')
def get_user_vacancy_by_id(vacancy_id=None):

    return f"Get your vacancie {vacancy_id}!"


@app.put('/vacancy/<int:vacancy_id>/')
def update_some_vacancy(vacancy_id=None):
    return f"Update your vacancie {vacancy_id}!"


@app.get('/vacancy/<int:vacancy_id>/events/')
def get_user_events(vacancy_id=None):
    return f"Get events for vacancy {vacancy_id}!"


@app.post('/vacancy/<int:vacancy_id>/events/')
def post_new_event_for_vacancy(vacancy_id=None):
    return f"Post new event for vacancy {vacancy_id}!"


@app.get('/vacancy/<int:vacancy_id>/events/<event_id>/')
def get_event_for_vacancy_by_id(vacancy_id=None, event_id=None):
    return f"Get event {event_id} for vacancy {vacancy_id}!"


@app.put('/vacancy/<int:id>/events/<int:event_id>/')
def update_some_event_for_vacancy(vacancy_id=None, event_id=None):
    return f"Update event {event_id} for vacancy {vacancy_id}!"

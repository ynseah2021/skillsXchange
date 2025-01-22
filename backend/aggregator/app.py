from flask_cors import CORS
from flask import Flask, request, jsonify, abort, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
from models import db
from mock_data import create_mock_data
import logging

import os
import requests

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@db:3306/db'
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize the db instance
db.init_app(app)
# register_error_handlers(app)

def init_db():
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('users'):
            db.create_all()
            create_mock_data(db)

init_db()

@app.route('/create_profile', methods=['POST'])
def create_profile():
    user_service_url = 'http://userservice:5000/create_profile'
    profile_data = request.get_json()
    response = requests.post(user_service_url, json=profile_data)
    if response.status_code == 201:
        session['user'] = response.json()
    return jsonify(response.json()), response.status_code

@app.route('/getuser/<username>', methods=['GET'])
def get_profile(username):
    user_service_url = f'http://userservice:5000/getuser/{username}'    
    response = requests.get(user_service_url)
    return jsonify(response.json()), response.status_code

@app.route("/add_skill", methods=['POST'])
def add_skill():
    userid = session['user']['id']
    app.logger.debug("Session content: %s", session)
    user_service_url = f'http://userservice:5000/add_skill/{userid}'
    skill_data = request.get_json()
    response = requests.post(user_service_url, json=skill_data)
    return jsonify(response.json()), response.status_code

@app.route('/create_class', methods=['POST'])
def create_class():
    app.logger.debug("Session content: %s", session)
    userid = session['user']['id']
    class_service_url = f'http://userclassservice:5000/{userid}/create_class'
    class_data = request.get_json()
    response = requests.post(class_service_url, json=class_data)
    return jsonify(response.json()), response.status_code

@app.route('/get_class/<class_id>', methods=['GET'])
def get_class(class_id):
    class_service_url = f'http://userclassservice:5000/get_class/{class_id}'
    response = requests.get(class_service_url)
    return jsonify(response.json()), response.status_code

@app.route('/get_user_classes', methods=['GET'])
def get_user_classes():
    userid = session['user']['id']
    class_service_url = f'http://userclassservice:5000/get_user_classes/{userid}'
    response = requests.get(class_service_url)
    return jsonify(response.json()), response.status_code

@app.route('/enroll_class/<class_id>', methods=['POST'])
def enroll_class(class_id):
    userid = session['user']['id']
    class_service_url = f'http://userclassservice:5000/enroll_class/{class_id}'
    class_data = request.get_json()
    class_data['userid'] = userid
    response = requests.post(class_service_url, json=class_data)
    return jsonify(response.json()), response.status_code

@app.route('/get_classes', methods=['GET'])
def get_classes():
    class_service_url = 'http://skillmatchclassservice:5000/get_classes'
    response = requests.get(class_service_url)
    return jsonify(response.json()), response.status_code

@app.route('/add_new_skill', methods=['POST'])
def add_new_skill():
    skill_service_url = 'http://skillmatchclassservice:5000/add_new_skill'
    skill_data = request.get_json()
    response = requests.post(skill_service_url, json=skill_data)
    return jsonify(response.json()), response.status_code

@app.route('/match_classes/default', methods=['GET'])
def get_class_default():
    class_service_url = 'http://skillmatchclassservice:5000/match_classes/default'
    response = requests.post(class_service_url, json=session['user'])
    if response.status_code != 200:
        return jsonify(response.json()), response.status_code
    
    matching_classes = response.json()
    for m in matching_classes:
        class_skills = [skill['skill_id'] for skill in m.get('skills_taught', [])]
        user_skills = [skill['skill_id'] for skill in session['user']['user_skills'] if skill["skills_type"] == "L"]

        matched_skills = set(user_skills).intersection(set(class_skills))
        m['matched_skills_count'] = len(matched_skills)
        m['number_skills'] = len(class_skills)  # Optionally, include the matched skills

    return jsonify(matching_classes), response.status_code

@app.route('/match_classes/filter', methods=['POST'])
def get_class_filter():
    class_service_url = 'http://skillmatchclassservice:5000/match_classes/filter'
    response = requests.post(class_service_url)
    return jsonify(response.json()), response.status_code

@app.route('/')
def home():
    return "Aggregator Pattern Example"

@app.route('/test')
def test():
    try:
        print("Attempting DB connection...")
        db.session.execute(text('SELECT * from users'))
        print("Database connection successful")
        return "Aggregator Pattern Example - DB connection successful"
    except Exception as e:
        print(f"Database connection failed: {e}")
        return f"Error: {e}"

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host= '0.0.0.0', port=5000, debug=True)
    session.clear()
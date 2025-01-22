from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, ClassEnrollment, Skill, Class, ClassSkill
from error_handlers import register_error_handlers
from werkzeug.utils import secure_filename
import os
import requests

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)

# Configure the Flask app with MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://user:password@db:3306/db')

# Bind SQLAlchemy to the app
db.init_app(app)
migrate = Migrate(app, db)
register_error_handlers(app)

@app.route('/<userid>/create_class', methods=['POST'])
def create_class(userid):
    data = request.get_json()

    # Validate required fields
    if not data.get('title'):
        abort(400, description="Missing information")
    
    existing_class = Class.query.filter_by(teacher_id=userid, title=data['title']).first()
    if existing_class:
        abort(400, description=f"Class with title '{data['title']}' already exists for this teacher.")

    # Create new class
    new_class = Class(
        teacher_id=userid,
        title=data['title'],
        description=data['description'],
        duration=data['duration'],
        class_time=data['class_time']
    )
    db.session.add(new_class)
    db.session.flush()

    for skill_data in data['skills_taught']:
        skill = Skill.query.filter_by(skill_name=skill_data['skill_name']).first()
        if not skill:
            abort(400, description=f"Skill '{skill_data['skill_name']}' not found.")
        class_skill = ClassSkill(class_id=new_class.id, skill_id=skill.id, proficiency=skill_data['proficiency'])
        db.session.add(class_skill)

    db.session.commit()
    return jsonify(new_class.to_dict()), 200

@app.route('/get_class/<class_id>', methods=['GET'])
def get_class(class_id):
    class_obj = Class.query.get(class_id)
    if class_obj:
        return jsonify(class_obj.to_dict()), 200
    abort(404, description="Class not found")

@app.route('/get_user_classes/<userid>', methods=['GET'])
def get_user_classes(userid):
    classes = Class.query.filter_by(teacher_id=userid).all()
    enrolled_classes = ClassEnrollment.query.filter_by(user_id=userid).all()
    classes.extend(enrolled_classes)
    return jsonify([c.to_dict() for c in classes]), 200

@app.route('/enroll_class/<class_id>', methods=['POST'])
def enroll_class(class_id):
    data = request.get_json()
    user_id = data.get('userid')
    if not user_id:
        abort(400, description="Missing information")

    class_obj = Class.query.get(class_id)
    if not class_obj:
        abort(404, description="Class not found")

    enrollment = ClassEnrollment(user_id=user_id, classid=class_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 200

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
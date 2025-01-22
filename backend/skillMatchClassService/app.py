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

@app.route('/add_new_skill', methods=['POST'])
def add_new_skill():
    data = request.get_json()

    # Validate required fields
    if not data.get('skill_name'):
        abort(400, description="Missing information")
    
    existing_skill = Skill.query.filter_by(skill_name=data['skill_name']).first()
    if existing_skill:
        abort(400, description="Skill already exists")

    # Create new skill
    new_skill = Skill(skill_name=data['skill_name'],skill_category=data.get('skill_category'))
    db.session.add(new_skill)
    db.session.commit()
    return jsonify(new_skill.to_dict()), 201

@app.route('/get_classes', methods=['GET'])
def get_classes():
    classes = Class.query.all()
    return jsonify([c.to_dict() for c in classes]), 200

#Match according to user skills
@app.route('/match_classes/default', methods=['POST'])
def get_match_default():
    data = request.get_json()
    app.logger.debug(data)
    user_skills_list = data.get('user_skills', [])
    user_skills = [skill['skill_id'] for skill in user_skills_list if skill["skills_type"] == "L"]
    # app.logger.debug(user_skills)
    if not user_skills:
        abort(400, description="No skills provided.")

    # Get all classes that have at least one of the user's skills
    classes = db.session.query(Class).join(ClassSkill).filter(ClassSkill.skill_id.in_(user_skills)).all()
    return jsonify([c.to_dict() for c in classes]), 200

# @app.route('/match_classes/advanced', methods=['POST'])
# def get_match_advanced():
#     data = request.get_json()
#     app.logger.debug(data)
#     #filter by skills
#     skills_filter = data.get('skills', [])
#     if skills_filter:
#         classes = db.session.query(Class).join(Class).filter(ClassSkill.skill_id.in_(user_skills)).all()

#     # Get all classes that have at least one of the user's skills
#     classes = db.session.query(Class).join(Class).filter(ClassSkill.skill_id.in_(user_skills)).all()
#     return jsonify([c.to_dict() for c in classes]), 200

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
    logging.basicConfig(level=logging.DEBUG)
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, UserProfile, Skill, UserSkill
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

app.config['UPLOAD_FOLDER'] = 'uploads/profile_pictures'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.get_json()

    # Validate required fields
    if not data.get('name') or not data.get('username'):
        abort(400, description="Missing information")
    
    existing_user = UserProfile.query.filter_by(username=data['username']).first()
    if existing_user:
        abort(400, description="Username already exists")

    file = request.files.get('profile_picture')
    if file and allowed_file(file.filename):
        picture_filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
    elif file:
        abort(400, description="Invalid file type")

    # Create new user profile
    new_profile = UserProfile(
        name=data['name'],
        username=data['username'],
        picture=data.get('picture'),
        bio=data.get('bio'),
        location=data.get('location'),
        hours_taught=data.get('hours_taught', 0),
        hours_learned=data.get('hours_learned', 0),
        average_reviews=data.get('average_reviews', 0.0)
    )
    db.session.add(new_profile)

    skills_data = data.get('skills', [])
    for skill_name, skill_level, type in skills_data:
        skill = Skill.query.filter_by(skill_name=skill_name).first()
        if not skill:
            # If the skill doesn't exist, create it
            skill = Skill(skill_name=skill_name)
            db.session.add(skill)
            db.session.commit()
        user_skill = UserSkill(user_id=new_profile.id, skill_id=skill.id, skill_level=skill_level, skills_type=type)
        db.session.add(user_skill)

    # Add the new profile to the database
    db.session.commit()

    return jsonify(new_profile.to_dict()), 201

@app.route('/update_profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    user = UserProfile.query.filter_by(username=user_id).first()
    if not user:
        abort(404, description="User not found")

    data = request.get_json()

    if data.get('name'):
        user.name = data['name']
    if data.get('picture'):
        user.picture = data['picture']
    if data.get('bio'):
        user.bio = data['bio']
    if data.get('location'):
        user.location = data['location']
    if data.get('hours_taught'):
        user.hours_taught = data['hours_taught']
    if data.get('hours_learned'):
        user.hours_learned = data['hours_learned']
    if data.get('average_reviews'):
        user.average_reviews = data['average_reviews']

    db.session.commit()
    return jsonify(user.to_dict()), 200

@app.route('/add_skill/<user_id>', methods=['POST'])
def add_skill(user_id):
    user = UserProfile.query.filter_by(id=user_id).first()
    if not user:
        abort(404, description="User not found")

    data = request.get_json()

    if not data.get('skill_name'):
        abort(400, description="Missing information")

    skill = Skill.query.filter_by(skill_name=data['skill_name']).first()
    if not skill:
        # If the skill doesn't exist, create it
        skill = Skill(skill_name=data['skill_name'])
        db.session.add(skill)
        db.session.commit()

    user_skill = UserSkill(user_id=user.id, skill_id=skill.id, skill_level=data.get('skill_level', 0), skills_type=data.get('skills_type'))
    db.session.add(user_skill)
    db.session.commit()

    return jsonify(user.to_dict()), 200

@app.route('/getuser/<username>', methods=['GET'])
def get_user_by_username(username):
    user = UserProfile.query.filter_by(username=username).first()
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict()), 200

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
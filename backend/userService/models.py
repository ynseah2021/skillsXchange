from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    skill_level = db.Column(db.Integer, nullable=False)
    skills_type = db.Column(db.String(1), nullable=False)

    # Relationship to Skill model
    skill = db.relationship('Skill', backref='user_skills', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_id': self.skill_id,
            'skill_level': self.skill_level,
            'skill': self.skill.to_dict() if self.skill else None,
            'skills_type': self.skills_type
        }

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(100), nullable=False, unique=True)
    skill_category = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'skill_category': self.skill_category,
        }

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    skills_taught = db.relationship('ClassSkill', backref=db.backref('class', lazy=True))
    duration = db.Column(db.Float, nullable=False) # in hours
    class_time = db.Column(db.DateTime, nullable=False) #start time

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'title': self.title,
            'description': self.description,
            'skills_taught': [{'skill_id': class_skills.skill.id, 'skill_name': class_skills.skill.skill_name, 'proficiency': class_skills.proficiency} for class_skills in self.skills_taught],
            'duration': self.duration,
            'class_time': self.class_time.isoformat()
        }

class ClassSkill(db.Model):
    __tablename__ = 'class_skills'
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    proficiency = db.Column(db.String(50), nullable=False)
    skill = db.relationship('Skill', backref='class_skills')

class ClassEnrollment(db.Model):
    __tablename__ = 'class_enrollments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classid = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    class_ = db.relationship('Class', backref=db.backref('enrollments', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserProfile', backref=db.backref('enrollments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'classid': self.classid,
            'user_id': self.user_id,
            'class': self.class_.to_dict() if self.class_ else None,  # Serialize related Class
            'user': self.user.to_dict() if self.user else None  # Serialize related UserProfile
        }


class UserProfile(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    picture = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)

    hours_taught = db.Column(db.Integer, default=0.0)
    hours_learned = db.Column(db.Integer, default=0.0)

    average_reviews = db.Column(db.Float, default=0.0)
    # reviews = db.relationship('Review', backref='user', lazy=True)

    user_skills = db.relationship('UserSkill', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'picture': self.picture,
            'bio': self.bio,
            'location': self.location,
            'hours_taught': self.hours_taught,
            'hours_learned': self.hours_learned,
            'average_reviews': self.average_reviews,
            'user_skills': [skill.to_dict() for skill in self.user_skills],  # Serialize related UserSkills
        }
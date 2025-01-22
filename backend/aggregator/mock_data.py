from models import Skill, UserProfile, UserSkill, Class, ClassSkill, ClassEnrollment
from datetime import datetime

def create_mock_data(db):
    # Mock Skills
    skills = [
        {'skill_name': 'SQL', 'skill_category': 'Coding'},
        {'skill_name': 'JavaScript', 'skill_category': 'Programming'},
        {'skill_name': 'Machine Learning', 'skill_category': 'Data Science'},
        {'skill_name': 'Data Analysis', 'skill_category': 'Data Science'},
        {'skill_name': 'Deep Learning', 'skill_category': 'Data Science'},
        {'skill_name': 'Project Management', 'skill_category': 'Business'}
    ]
    skills_list = []
    
    for skill_data in skills:
        skill = Skill(skill_name=skill_data['skill_name'], skill_category=skill_data['skill_category'])
        db.session.add(skill)
        db.session.commit()
        skills_list.append(skill)
        print(skill.to_dict())

    #mock users
    users_data = [
        {'name': 'John Doe', 'username': 'john_doe', 'bio': 'Experienced Python and Data Science teacher.', 'location': 'New York'},
        {'name': 'Jane Smith', 'username': 'jane_smith', 'bio': 'Machine Learning and Web Development expert.', 'location': 'San Francisco'},
        {'name': 'Mark Lee', 'username': 'mark_lee', 'bio': 'Project Management and Business strategist.', 'location': 'Los Angeles'}
    ]
    users = []
    for user_data in users_data:
        user = UserProfile(
            name=user_data['name'],
            username=user_data['username'],
            bio=user_data['bio'],
            location=user_data['location']
        )
        db.session.add(user)
        db.session.commit()
        users.append(user)
        # print(user.to_dict())

    db.session.commit()

    # Mock User Skills (teachable skills for each user)
    user_skills_data = [
        {'user': users[0], 'skills': [skills_list[0], skills_list[1]]},  # John Doe can teach Python and Data Science
        {'user': users[1], 'skills': [skills_list[2], skills_list[3]]},  # Jane Smith can teach Machine Learning and Web Development
        {'user': users[2], 'skills': [skills_list[4], skills_list[5]]}   # Mark Lee can teach Project Management and Business
    ]
    
    for entry in user_skills_data:
        user = entry['user']  # Get the user instance
        for skill in entry['skills']:  # Iterate over the user's skills
            user_skill = UserSkill(user_id=user.id, skill_id=skill.id, skill_level=3, skills_type='T')
            db.session.add(user_skill) 

    # Mock Classes taught by users
    classes_data = [
        {'teacher': users[0], 'title': 'Python 101', 'description': 'Learn Python programming from scratch.', 'skills': [skills_list[0], skills_list[1]], 'duration': 10.0, 'class_time': datetime(2025, 2, 1, 9, 0)},
        {'teacher': users[1], 'title': 'Machine Learning Basics', 'description': 'Introduction to Machine Learning algorithms.', 'skills': [skills_list[2]], 'duration': 12.0, 'class_time': datetime(2025, 2, 5, 9, 0)},
        {'teacher': users[1], 'title': 'Web Development for Beginners', 'description': 'Build your first website using HTML, CSS, and JavaScript.', 'skills': [skills_list[3]], 'duration': 15.0, 'class_time': datetime(2025, 2, 7, 9, 0)},
        {'teacher': users[2], 'title': 'Project Management Fundamentals', 'description': 'Learn the basics of managing projects successfully.', 'skills': [skills_list[4]], 'duration': 8.0, 'class_time': datetime(2025, 2, 10, 9, 0)},
        {'teacher': users[2], 'title': 'Business Strategies', 'description': 'Understand business strategies for long-term success.', 'skills': [skills_list[5]], 'duration': 10.0, 'class_time': datetime(2025, 2, 15, 9, 0)}
    ]
    classes_data_list = []

    # Insert classes into the database
    for class_data in classes_data:
        new_class = Class(
            teacher_id=class_data['teacher'].id,
            title=class_data['title'],
            description=class_data['description'],
            duration=class_data['duration'],
            class_time=class_data['class_time']
        )
        db.session.add(new_class)
        db.session.flush()  # Get the class ID to associate skills
        
        # Insert ClassSkills
        for skill in class_data['skills']:
            class_skill = ClassSkill(class_id=new_class.id, skill_id=skill.id, proficiency=2)
            db.session.add(class_skill)
            classes_data_list.append(new_class)

        db.session.commit()

    enrollments_data = [
        {'user': users[0], 'class': classes_data_list[0]},
        {'user': users[1], 'class': classes_data_list[1]},
        {'user': users[1], 'class': classes_data_list[2]},
        {'user': users[2], 'class': classes_data_list[3]},
        {'user': users[2], 'class': classes_data_list[4]}
    ]
    
    for enrollment_data in enrollments_data:
        enrollment = ClassEnrollment(user_id=enrollment_data['user'].id, classid=enrollment_data['class'].id)
        db.session.add(enrollment)

    db.session.commit()


    print("Mock data inserted successfully!")

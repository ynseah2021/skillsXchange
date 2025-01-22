# skillsEX

## Command to run
```
docker-compose up --build -d
```
1. Begin by posting a request to http://localhost:5000/create_profile to create a profile before continuing with other requests


## Explanation
Features included: profile creation, skills matching, classes and user classes

Profile Creation
- Upon creation, backend will store session for the user, all operations that follows after will automatically be tied to the user
- Stores user details and skills


Skills matching
- Default matching matches skills that user wants to learn to all classes available, to be shown as the default page for skills matching (without filters/search)
- Classes returned has the number of skills matched for user visibility on relevance
- Future: Filtering by various options (skills, time, etc), search bar to search by title, description - returns list of classes by match, can use recommendation system to recommend classes according to user's interests, similarity matching by semantic meaning with user's interests

User Classes
- User can add class to host
- Get all classes that user has registered for and host - intended for frontend calendar display
- Future: frontend calendar view


## API Appendix

**Endpoint**: `POST /create_profile`

- **Description**: This endpoint creates profile based on information filled in profile page

- **Path Parameters**:
  - `username` (string): The unique username for the user.
  - `name` (string): The name of the user.
  - `picture` (string): The filename of the profile picture.
  - `bio` (string): Profile description
  - `location` (string): Physical location of user
  - `teachable_skills` (int): skill_id of teachable skills and proficiency
  - `learnable_skills` (int): skill_id of learnable skills and proficiency

- **Request example**:
    ```json
    {
        "name": "John Doe",
        "username": "johndoe123",
        "bio": "Software Developer with a passion for teaching",
        "location": "New York, USA",
        "hours_taught": 100,
        "hours_learned": 50,
        "average_reviews": 4.5,
        "skills": [
            ["python", 5, "T"],
            ["java", 3, "T"],
            ["javascript", 4, "T"]
        ]
    }
    ```


- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        "message": "User created.",
        "success": true
    }
    ```

**Endpoint**: `GET /getuser/<username>`

- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        {
            "average_reviews": 4.5,
            "bio": "Software Developer with a passion for teaching",
            "hours_learned": 50,
            "hours_taught": 100,
            "id": 1,
            "learnable_skills": [
                {
                    "id": 1,
                    "skill": {
                        "id": 1,
                        "skill_category": null,
                        "skill_name": "python"
                    },
                    "skill_id": 1,
                    "skill_level": 5,
                    "user_id": 1
                },
                {
                    "id": 2,
                    "skill": {
                        "id": 2,
                        "skill_category": null,
                        "skill_name": "java"
                    },
                    "skill_id": 2,
                    "skill_level": 3,
                    "user_id": 1
                },
                {
                    "id": 3,
                    "skill": {
                        "id": 3,
                        "skill_category": null,
                        "skill_name": "javascript"
                    },
                    "skill_id": 3,
                    "skill_level": 4,
                    "user_id": 1
                }
            ],
            "location": "New York, USA",
            "name": "John Doe",
            "picture": null,
            "teachable_skills": [
                {
                    "id": 1,
                    "skill": {
                        "id": 1,
                        "skill_category": null,
                        "skill_name": "python"
                    },
                    "skill_id": 1,
                    "skill_level": 5,
                    "user_id": 1
                },
                {
                    "id": 2,
                    "skill": {
                        "id": 2,
                        "skill_category": null,
                        "skill_name": "java"
                    },
                    "skill_id": 2,
                    "skill_level": 3,
                    "user_id": 1
                },
                {
                    "id": 3,
                    "skill": {
                        "id": 3,
                        "skill_category": null,
                        "skill_name": "javascript"
                    },
                    "skill_id": 3,
                    "skill_level": 4,
                    "user_id": 1
                }
            ],
            "username": "johndoe123"
        }   
    }
    ```


**Endpoint**: `POST /create_class`

- **Request example**:
    ```json
    {
        "title": "Advanced Python Programming",
        "description": "A deep dive into Python programming for experienced developers.",
        "skills_taught": [
            {
                "skill_name": "Python",
                "proficiency": "Advanced"
            }
        ],
        "duration": 10.5,
        "class_time": "2025-02-01T14:00:00"
    }
    ```


- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        "class_time": "2025-02-01T14:00:00",
        "description": "A deep dive into Python programming for experienced developers.",
        "duration": 10.5,
        "id": 1,
        "skills_taught": [
            {
                "proficiency": "Advanced",
                "skill_name": "python"
            }
        ],
        "teacher_id": 1,
        "title": "Advanced Python Programming"
    }
    ```

**Endpoint**: `GET /get_class/<class_id>`

- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        "class_time": "2025-02-01T14:00:00",
        "description": "A deep dive into Python programming for experienced developers.",
        "duration": 10.5,
        "id": 2,
        "skills_taught": [
            {
                "proficiency": "Advanced",
                "skill_name": "python"
            }
        ],
        "teacher_id": 2,
        "title": "Advanced Python Programming"
    }
    ```

**Endpoint**: `GET /get_classes`

- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    [
        {
            "class_time": "2025-02-01T14:00:00",
            "description": "A deep dive into Python programming for experienced developers.",
            "duration": 10.5,
            "id": 1,
            "skills_taught": [
                {
                    "proficiency": "Advanced",
                    "skill_name": "python"
                }
            ],
            "teacher_id": 1,
            "title": "Advanced Python Programming"
        },
        {
            "class_time": "2025-02-01T14:00:00",
            "description": "A deep dive into Python programming for experienced developers.",
            "duration": 10.5,
            "id": 2,
            "skills_taught": [
                {
                    "proficiency": "Advanced",
                    "skill_name": "python"
                }
            ],
            "teacher_id": 1,
            "title": "Advanced Python Programming 2"
        }
    ]
    ```


**Endpoint**: `POST /enroll_class/<class_id>`

- **Request example**:
    ```json
    {}
    ```


- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        "class": {
            "class_time": "2025-02-01T14:00:00",
            "description": "A deep dive into Python programming for experienced developers.",
            "duration": 10.5,
            "id": 1,
            "skills_taught": [
                {
                    "proficiency": "Advanced",
                    "skill_name": "python"
                }
            ],
            "teacher_id": 1,
            "title": "Advanced Python Programming"
        },
        "classid": 1,
        "id": 1,
        "user": {
            "average_reviews": 4.5,
            "bio": "Software Developer with a passion for teaching",
            "hours_learned": 50,
            "hours_taught": 100,
            "id": 5,
            "learnable_skills": [
                {
                    "id": 13,
                    "skill": {
                        "id": 1,
                        "skill_category": null,
                        "skill_name": "python"
                    },
                    "skill_id": 1,
                    "skill_level": 5,
                    "user_id": 5
                },
                {
                    "id": 14,
                    "skill": {
                        "id": 2,
                        "skill_category": null,
                        "skill_name": "java"
                    },
                    "skill_id": 2,
                    "skill_level": 3,
                    "user_id": 5
                },
                {
                    "id": 15,
                    "skill": {
                        "id": 3,
                        "skill_category": null,
                        "skill_name": "javascript"
                    },
                    "skill_id": 3,
                    "skill_level": 4,
                    "user_id": 5
                }
            ],
            "location": "New York, USA",
            "name": "John Doe",
            "picture": null,
            "teachable_skills": [
                {
                    "id": 13,
                    "skill": {
                        "id": 1,
                        "skill_category": null,
                        "skill_name": "python"
                    },
                    "skill_id": 1,
                    "skill_level": 5,
                    "user_id": 5
                },
                {
                    "id": 14,
                    "skill": {
                        "id": 2,
                        "skill_category": null,
                        "skill_name": "java"
                    },
                    "skill_id": 2,
                    "skill_level": 3,
                    "user_id": 5
                },
                {
                    "id": 15,
                    "skill": {
                        "id": 3,
                        "skill_category": null,
                        "skill_name": "javascript"
                    },
                    "skill_id": 3,
                    "skill_level": 4,
                    "user_id": 5
                }
            ],
            "username": "4"
        },
        "user_id": 5
    }
    ```

**Endpoint**: `GET /get_user_classes`

- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    [
        {
            "class_time": "2025-02-01T14:00:00",
            "description": "A deep dive into Python programming for experienced developers.",
            "duration": 10.5,
            "id": 7,
            "skills_taught": [
                {
                    "proficiency": "Advanced",
                    "skill_name": "python"
                }
            ],
            "teacher_id": 5,
            "title": "Advanced Python "
        },
        {
            "class": {
                "class_time": "2025-02-01T14:00:00",
                "description": "A deep dive into Python programming for experienced developers.",
                "duration": 10.5,
                "id": 1,
                "skills_taught": [
                    {
                        "proficiency": "Advanced",
                        "skill_name": "python"
                    }
                ],
                "teacher_id": 1,
                "title": "Advanced Python Programming"
            },
            "classid": 1,
            "id": 1,
            "user": {
                "average_reviews": 4.5,
                "bio": "Software Developer with a passion for teaching",
                "hours_learned": 50,
                "hours_taught": 100,
                "id": 5,
                "learnable_skills": [
                    {
                        "id": 13,
                        "skill": {
                            "id": 1,
                            "skill_category": null,
                            "skill_name": "python"
                        },
                        "skill_id": 1,
                        "skill_level": 5,
                        "user_id": 5
                    },
                    {
                        "id": 14,
                        "skill": {
                            "id": 2,
                            "skill_category": null,
                            "skill_name": "java"
                        },
                        "skill_id": 2,
                        "skill_level": 3,
                        "user_id": 5
                    },
                    {
                        "id": 15,
                        "skill": {
                            "id": 3,
                            "skill_category": null,
                            "skill_name": "javascript"
                        },
                        "skill_id": 3,
                        "skill_level": 4,
                        "user_id": 5
                    }
                ],
                "location": "New York, USA",
                "name": "John Doe",
                "picture": null,
                "teachable_skills": [
                    {
                        "id": 13,
                        "skill": {
                            "id": 1,
                            "skill_category": null,
                            "skill_name": "python"
                        },
                        "skill_id": 1,
                        "skill_level": 5,
                        "user_id": 5
                    },
                    {
                        "id": 14,
                        "skill": {
                            "id": 2,
                            "skill_category": null,
                            "skill_name": "java"
                        },
                        "skill_id": 2,
                        "skill_level": 3,
                        "user_id": 5
                    },
                    {
                        "id": 15,
                        "skill": {
                            "id": 3,
                            "skill_category": null,
                            "skill_name": "javascript"
                        },
                        "skill_id": 3,
                        "skill_level": 4,
                        "user_id": 5
                    }
                ],
                "username": "4"
            },
            "user_id": 5
        }
    ]
    ```

**Endpoint**: `POST /add_new_skill`

- **Request example**:
    ```json
    {
        "skill_name": "Machine Learning",
        "skill_category": "Data Science"
    }
    ```


- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
    ```json
    {
        "id": 4,
        "skill_category": "Data Science",
        "skill_name": "Machine Learning"
    }
    ```
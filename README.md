Marriage Matchmaking App

This is a FastAPI application that provides matchmaking services based on user profiles. Users can register, update their information, and find compatible matches based on age, gender, location, and interests.


FEATURES
- User Registration: Create a new user with details like name, age, gender, email, city, and interests.
- User Management: Read, update, and delete user profiles.
- Matchmaking System: Find compatible matches based on:
    - Age similarity
    - Location (same city)
    - Common interests
- Email Validation: Ensures that user emails follow a valid format.
- Database Integration: Uses SQLite with SQLAlchemy ORM for data storage.


TECHNOLOGIES USED
- FastAPI: Web framework for building APIs.
- SQLAlchemy: ORM for database management.
- Pydantic: Data validation and serialization.
- SQLite: Lightweight database.
- Uvicorn: ASGI server for running FastAPI.


INSTALLATION
1. Clone the Repository
    git clone https://github.com/yourusername/marriage-matchmaking.git
    cd marriage-matchmaking
2. Create and Activate a Virtual Environment
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
3. Install Dependencies
    pip install -r requirements.txt


RUNNING the Application
    uvicorn main:app --reload
    The API will be available at: http://127.0.0.1:8000


API ENDPOINTS
- User Endpoints
    METHOD	    ENDPOINT	            DESCRIPTION
    POST	    /users/	                Create a new user
    GET	        /users/	                Get all users (with pagination)
    GET	        /users/{user_id}	    Get a user by ID
    PUT	        /users/{user_id}	    Update user details
    DELETE	    /users/{user_id}	    Delete a user

- Matchmaking Endpoint
    METHOD	    ENDPOINT	                DESCRIPTION
    GET	        /users/{user_id}/matches	Find compatible matches for a user


DATABASE SCHEMA
- The users table consists of the following fields:

    Column	    Type	    Description
    id	        Integer	    Primary Key
    name	    String	    User's name
    age	        Integer	    Age (18-100)
    gender	    String	    Male, Female, or Other
    email	    String	    Unique Email ID
    city	    String	    User's city
    interests	Text	    Comma-separated interests


Example API Requests
- Create a New User
    POST /users/
    {
    "name": "John Doe",
    "age": 28,
    "gender": "male",
    "email": "john.doe@example.com",
    "city": "New York",
    "interests": "travel,movies,cooking"
    }


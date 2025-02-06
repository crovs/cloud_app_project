# Cloud App Project

## Overview
The **Cloud App Project** is a Flask-based web application designed for user authentication and task management. Users can register, log in, and manage their tasks seamlessly. The application is containerized using Docker for easy deployment and includes PostgreSQL for data storage.
#Students Involved: Ahmet Emin Yada  , 54956

## Features
- User Registration & Login
- Task Creation and Management
- RESTful API Endpoints
- Secure Session Handling
- Dockerized for Simplified Deployment
- Unit Tests for Core Functionality

## Tech Stack
- **Backend:** Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Testing:** unittest (Python's built-in framework)

## Setup Instructions

### Prerequisites
- Python 3.x
- Docker & Docker Compose
- Virtualenv (optional but recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/cloud_app_project.git
cd cloud_app_project
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:

```
FLASK_APP=cloud_app
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/your_db_name
```

### 4. Run the Application Locally
```bash
flask run
```
The app will be accessible at `http://127.0.0.1:5000/`.

## Running Tests
To run unit tests for the app:
```bash
python test_app.py
```

## Usage

### API Endpoints
- **POST /register**: Register a new user.
  - Payload: `{ "username": "user", "password": "pass" }`
- **POST /login**: Authenticate user.
  - Payload: `{ "username": "user", "password": "pass" }`
- **POST /tasks**: Create a new task (requires login).
  - Payload: `{ "title": "New Task" }`

## Docker Deployment

### 1. Build and Run with Docker Compose
```bash
docker-compose down  # Stop previous containers if running
docker-compose build
docker-compose up -d
```

### 2. Access the Application
Visit `http://localhost:5000/` in your browser.

### 3. Stop the Application
```bash
docker-compose down
```

## License
This project is licensed under the MIT License.

---

**Happy Coding!** 🚀


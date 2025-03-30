# ESummit Backend

Backend for ESummit platform built with Flask and PostgreSQL.

## Features

- User authentication (register, login, logout)
- Dashboard for users
- Event registration system
- Hackathon registration system
- Admin panel to manage events and registrations

## Setup

1. Clone the repository
```
git clone <repository-url>
cd esummit-backend
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Set up environment variables in .env file
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://postgres:postgres@db:5432/esummit
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

5. Initialize the database
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application
```
flask run
```

Visit `http://127.0.0.1:5000/` in your browser to access the application.

import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Get database URL from environment 
db_url = os.environ.get('DATABASE_URL')

# Set path for SQLite database
sqlite_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)

# Use SQLite by default unless PostgreSQL is specifically requested
use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true'

if use_sqlite or not db_url:
    db_url = f'sqlite:///{sqlite_path}'
    logging.info(f"Using SQLite database at {sqlite_path}")
elif '-pooler' in db_url:
    # Remove pooler if present for direct connection
    db_url = db_url.replace('-pooler', '')
    logging.info("Converted pooler URL to direct connection")

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pooling settings optimized for the database type
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Check connection validity before using
        'pool_recycle': 60,     # Recycle connections after 60 seconds
        'pool_timeout': 30,     # Wait up to 30 seconds for a connection
        'max_overflow': 10,     # Allow up to 10 extra connections
        'pool_size': 5,         # Maintain 5 connections in the pool
    }
    
    # Database-specific settings
    if 'sqlite' in db_url:
        SQLALCHEMY_ENGINE_OPTIONS.update({
            'connect_args': {'check_same_thread': False},
        })
    else:
        # PostgreSQL settings
        SQLALCHEMY_ENGINE_OPTIONS.update({
            'connect_args': {
                'connect_timeout': 10,
                'application_name': 'esummit-app',
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 10,
                'keepalives_count': 5
            }
        })
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'admin@esummit.com')
    
    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC' 
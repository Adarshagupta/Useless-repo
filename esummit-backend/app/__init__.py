import os
from flask import Flask, render_template, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from datetime import datetime
from flask_mail import Mail
from .celery_config import celery, init_celery
from sqlalchemy import create_engine, event, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError, SQLAlchemyError, InterfaceError, DisconnectionError
import logging
import time
import re
from functools import wraps
from werkzeug.exceptions import HTTPException
import sqlalchemy.exc

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()

# Database retry configuration
DB_MAX_RETRIES = 3
DB_RETRY_DELAY = 0.5  # in seconds

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Database configuration with fallback
    database_url = os.environ.get('DATABASE_URL')
    use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true'

    try:
        if use_sqlite:
            # SQLite configuration
            logger.info("Using SQLite database")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')

            # Ensure the instance folder exists
            os.makedirs(app.instance_path, exist_ok=True)
        else:
            # PostgreSQL configuration
            logger.info(f"Database URL: {database_url.replace('://', '://***:***@') if database_url else None}")
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url

            # Set PostgreSQL specific options for better connections
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                'pool_pre_ping': True,
                'pool_recycle': 280,  # Neon closes connections after 5 minutes, so cycle them before that
                'pool_timeout': 30,
                'pool_size': 5,
                'max_overflow': 10
            }

            # Test PostgreSQL connection
            engine = create_engine(database_url, pool_pre_ping=True)
            connection = engine.connect()
            connection.close()
            logger.info("PostgreSQL connection successful")
    except Exception as e:
        logger.error(f"Database configuration error: {e}")
        # If specifically configured to use PostgreSQL, don't fallback
        if not use_sqlite:
            raise OperationalError(f"Could not connect to PostgreSQL database: {e}")

        # Otherwise fallback to SQLite if allowed
        logger.info("Falling back to SQLite database")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
        os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Initialize Celery
    init_celery(app)

    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Import models
    with app.app_context():
        from app.models import user, event, registration, team, activity

    # Register blueprints
    from app.routes import main, auth, dashboard, admin, staff
    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard.dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin.admin_bp, url_prefix='/admin')
    app.register_blueprint(staff.staff_bp, url_prefix='/staff')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return render_template('errors/generic.html', error=e), e.code

    @app.errorhandler(sqlalchemy.exc.OperationalError)
    def handle_db_error(e):
        return render_template('errors/db_error.html'), 500

    # Add context processors for templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    return app

def with_db_retry(f):
    """Decorator to retry database operations"""
    @wraps(f)
    def db_retry_wrapper(*args, **kwargs):
        retries = 0
        while retries < DB_MAX_RETRIES:
            try:
                return f(*args, **kwargs)
            except (OperationalError, InterfaceError, DisconnectionError) as e:
                retries += 1
                if retries >= DB_MAX_RETRIES:
                    raise
                logging.warning(f"Database error, retrying ({retries}/{DB_MAX_RETRIES}): {str(e)}")
                time.sleep(DB_RETRY_DELAY * retries)  # Exponential backoff
                db.session.rollback()
        return None
    return db_retry_wrapper

def with_transaction(f):
    """Decorator to handle database transactions"""
    @wraps(f)
    def transaction_wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise
    return transaction_wrapper

def sanitize_db_url(url):
    """Remove sensitive info from DB URL for logging"""
    if not url:
        return "None"
    # Replace password with asterisks
    return re.sub(r'://[^:]+:([^@]+)@', r'://\1:***@', url)

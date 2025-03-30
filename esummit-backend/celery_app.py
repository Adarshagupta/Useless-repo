from app import create_app
from app.celery_config import celery

flask_app = create_app()
celery.conf.update(flask_app.config) 
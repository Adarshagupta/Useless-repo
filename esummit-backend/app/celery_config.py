from celery import Celery

# Create the celery instance
celery = Celery('app')

def init_celery(app):
    # Update celery config
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery 
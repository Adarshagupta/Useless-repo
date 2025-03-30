from flask import render_template
from flask_mail import Message
from app import celery, mail

@celery.task
def send_announcement_email(user_email, title, message, sender_name):
    """Send announcement email to user."""
    msg = Message(
        subject=f"ESummit Announcement: {title}",
        sender=("ESummit Admin", "admin@esummit.com"),
        recipients=[user_email]
    )
    
    msg.html = render_template(
        'email/announcement.html',
        title=title,
        message=message,
        sender_name=sender_name
    )
    
    mail.send(msg) 
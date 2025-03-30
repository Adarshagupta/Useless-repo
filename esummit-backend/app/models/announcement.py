from datetime import datetime
from app import db

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='announcements')
    event = db.relationship('Event', foreign_keys=[event_id], backref='announcements')
    notifications = db.relationship('Notification', backref='announcement', lazy='dynamic') 
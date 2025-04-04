from app import db
from datetime import datetime

class ActivityLog(db.Model):
    """Model for activity logs"""
    __tablename__ = 'activity_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    activity_type = db.Column(db.String(50), nullable=False)  # registration, check_in, team, admin, etc.
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, warning, danger, info
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='activities')
    event = db.relationship('Event', backref='activities')
    
    def __init__(self, user_id, activity_type, description, status, event_id=None):
        self.user_id = user_id
        self.event_id = event_id
        self.activity_type = activity_type
        self.description = description
        self.status = status
    
    @property
    def status_color(self):
        if self.status == 'success':
            return 'success'
        elif self.status == 'warning':
            return 'warning'
        elif self.status == 'danger':
            return 'danger'
        elif self.status == 'info':
            return 'info'
        else:
            return 'secondary'
    
    def __repr__(self):
        return f"ActivityLog(User: {self.user_id}, Type: {self.activity_type}, Status: {self.status})"

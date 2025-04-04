from datetime import datetime
from app import db

class Event(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    registration_deadline = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    event_type = db.Column(db.String(20), nullable=False)  # 'workshop', 'hackathon', 'talk', etc.
    is_team_event = db.Column(db.Boolean, default=False)
    min_team_size = db.Column(db.Integer, nullable=True)
    max_team_size = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    prize_pool = db.Column(db.Integer, nullable=True, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('EventRegistration', backref='event', lazy=True, cascade='all, delete-orphan')
    teams = db.relationship('Team', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, name, description, start_date, end_date, venue, registration_deadline, 
                 event_type, is_team_event=False, capacity=None, min_team_size=None, 
                 max_team_size=None, image_url=None, subtitle=None):
        self.name = name
        self.description = description
        self.subtitle = subtitle
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.registration_deadline = registration_deadline
        self.capacity = capacity
        self.event_type = event_type
        self.is_team_event = is_team_event
        self.min_team_size = min_team_size
        self.max_team_size = max_team_size
        self.image_url = image_url
    
    @property
    def is_registration_open(self):
        return datetime.utcnow() < self.registration_deadline
    
    @property
    def registered_count(self):
        return len(self.registrations)
    
    @property
    def is_full(self):
        if self.capacity:
            return self.registered_count >= self.capacity
        return False
    
    @property
    def status(self):
        now = datetime.utcnow()
        if now > self.end_date:
            return 'completed'
        elif now > self.start_date:
            return 'ongoing'
        else:
            return 'upcoming'
    
    @property
    def status_color(self):
        status = self.status
        if status == 'completed':
            return 'secondary'
        elif status == 'ongoing':
            return 'success'
        else:
            return 'primary'
    
    def is_registered(self, user):
        """Check if a user is registered for this event"""
        return any(registration.user_id == user.id for registration in self.registrations)
    
    def __repr__(self):
        return f"Event('{self.name}', '{self.start_date}')"

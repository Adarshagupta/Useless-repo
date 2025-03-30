from datetime import datetime
from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, name, leader_id, event_id):
        self.name = name
        self.leader_id = leader_id
        self.event_id = event_id
    
    @property
    def member_count(self):
        return len(self.members)
    
    def __repr__(self):
        return f"Team('{self.name}', Leader: {self.leader_id}, Event: {self.event_id})"


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, team_id, user_id, role=None, joined_at=None):
        self.team_id = team_id
        self.user_id = user_id
        self.role = role
        if joined_at:
            self.joined_at = joined_at
    
    def __repr__(self):
        return f"TeamMember(Team: {self.team_id}, User: {self.user_id}, Role: {self.role})"

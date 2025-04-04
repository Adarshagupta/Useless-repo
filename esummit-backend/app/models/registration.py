from datetime import datetime
from app import db

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid
    payment_id = db.Column(db.String(100), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    # New fields for enhanced registration
    full_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    institution = db.Column(db.String(100), nullable=True)
    why_join = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    document_filename = db.Column(db.String(255), nullable=True)

    def __init__(self, user_id, event_id, status='pending', payment_status='unpaid',
                 payment_id=None, team_id=None, full_name=None, email=None, phone=None,
                 institution=None, why_join=None, experience=None, document_filename=None):
        self.user_id = user_id
        self.event_id = event_id
        self.status = status
        self.payment_status = payment_status
        self.payment_id = payment_id
        self.team_id = team_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.institution = institution
        self.why_join = why_join
        self.experience = experience
        self.document_filename = document_filename

    @property
    def status_color(self):
        if self.status == 'pending':
            return 'warning'
        elif self.status == 'confirmed' or self.status == 'approved':
            return 'success'
        elif self.status == 'rejected' or self.status == 'cancelled':
            return 'danger'
        else:
            return 'secondary'

    def __repr__(self):
        return f"EventRegistration(User: {self.user_id}, Event: {self.event_id}, Status: {self.status})"


class PitchRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, cancelled
    rejection_reason = db.Column(db.Text, nullable=True)

    # Pitch details
    pitch_title = db.Column(db.String(100), nullable=False)
    pitch_summary = db.Column(db.Text, nullable=False)
    problem_statement = db.Column(db.Text, nullable=False)
    solution_approach = db.Column(db.Text, nullable=False)
    market_analysis = db.Column(db.Text, nullable=False)
    business_model = db.Column(db.Text, nullable=False)
    team_background = db.Column(db.Text, nullable=False)

    # Document links
    pitch_deck_url = db.Column(db.String(255), nullable=False)
    additional_docs_url = db.Column(db.String(255), nullable=True)
    video_pitch_url = db.Column(db.String(255), nullable=True)

    # Relationships
    event = db.relationship('Event', backref='pitch_registrations')
    team = db.relationship('Team', backref='pitch_registrations')

    def __init__(self, team_id, event_id, pitch_title, pitch_summary, problem_statement,
                 solution_approach, market_analysis, business_model, team_background,
                 pitch_deck_url, additional_docs_url=None, video_pitch_url=None, status='pending'):
        self.team_id = team_id
        self.event_id = event_id
        self.pitch_title = pitch_title
        self.pitch_summary = pitch_summary
        self.problem_statement = problem_statement
        self.solution_approach = solution_approach
        self.market_analysis = market_analysis
        self.business_model = business_model
        self.team_background = team_background
        self.pitch_deck_url = pitch_deck_url
        self.additional_docs_url = additional_docs_url
        self.video_pitch_url = video_pitch_url
        self.status = status

    @property
    def status_color(self):
        if self.status == 'pending':
            return 'warning'
        elif self.status == 'confirmed' or self.status == 'approved':
            return 'success'
        elif self.status == 'rejected' or self.status == 'cancelled':
            return 'danger'
        else:
            return 'secondary'

    def __repr__(self):
        return f"PitchRegistration(Team: {self.team_id}, Event: {self.event_id}, Pitch: {self.pitch_title})"


class HackathonRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(255), nullable=False)
    github_url = db.Column(db.String(255), nullable=True)
    other_links = db.Column(db.Text, nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled

    # New fields for enhanced registration
    proposal_document_filename = db.Column(db.String(255), nullable=True)
    problem_statement = db.Column(db.Text, nullable=True)
    solution_approach = db.Column(db.Text, nullable=True)
    team_background = db.Column(db.Text, nullable=True)

    # Relationships
    event = db.relationship('Event', backref='hackathon_registrations')
    team = db.relationship('Team', backref='hackathon_registrations')

    def __init__(self, team_id, event_id, project_name, project_description, tech_stack,
                 github_url=None, other_links=None, status='pending', proposal_document_filename=None,
                 problem_statement=None, solution_approach=None, team_background=None):
        self.team_id = team_id
        self.event_id = event_id
        self.project_name = project_name
        self.project_description = project_description
        self.tech_stack = tech_stack
        self.github_url = github_url
        self.other_links = other_links
        self.status = status
        self.proposal_document_filename = proposal_document_filename
        self.problem_statement = problem_statement
        self.solution_approach = solution_approach
        self.team_background = team_background

    def __repr__(self):
        return f"HackathonRegistration(Team: {self.team_id}, Event: {self.event_id}, Project: {self.project_name})"

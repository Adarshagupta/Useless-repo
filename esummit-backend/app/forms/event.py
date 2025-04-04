from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional, URL, Length, NumberRange
from datetime import datetime

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    
    subtitle = StringField('Event Subtitle', validators=[
        Optional(),
        Length(max=200)
    ])
    
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=10, max=2000)
    ])
    
    event_type = SelectField('Event Type', choices=[
        ('hackathon', 'Hackathon'),
        ('workshop', 'Workshop'),
        ('competition', 'Competition'),
        ('talk', 'Talk')
    ], validators=[DataRequired()])
    
    venue = StringField('Venue', validators=[
        DataRequired(),
        Length(max=200)
    ])
    
    start_date = DateTimeLocalField(
        'Start Date',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        default=datetime.utcnow
    )
    
    end_date = DateTimeLocalField(
        'End Date',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        default=lambda: datetime.utcnow()
    )
    
    min_team_size = IntegerField('Minimum Team Size', validators=[
        Optional(),
        NumberRange(min=1, max=10)
    ])
    
    max_team_size = IntegerField('Maximum Team Size', validators=[
        Optional(),
        NumberRange(min=1, max=10)
    ])
    
    image_url = StringField('Image URL', validators=[
        Optional(),
        Length(max=500)
    ])

    capacity = IntegerField('Capacity (leave blank for unlimited)', validators=[Optional()])
    is_team_event = BooleanField('Team Event')
    registration_deadline = DateTimeLocalField(
        'Registration Deadline',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        default=lambda: datetime.utcnow()
    )
    submit = SubmitField('Create Event')


class EventRegistrationForm(FlaskForm):
    submit = SubmitField('Register for Event')

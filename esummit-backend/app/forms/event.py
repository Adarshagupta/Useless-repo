from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional, URL, Length, NumberRange, ValidationError
from datetime import datetime, timedelta

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
        ('talk', 'Talk'),
        ('pitching', 'Pitching Event')
    ], validators=[DataRequired()])

    venue = StringField('Venue', validators=[
        DataRequired(),
        Length(max=200)
    ])

    start_date = DateTimeLocalField(
        'Start Date',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        default=lambda: datetime.utcnow() + timedelta(days=1)  # Default to tomorrow
    )

    end_date = DateTimeLocalField(
        'End Date',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        default=lambda: datetime.utcnow() + timedelta(days=1, hours=3)  # Default to tomorrow + 3 hours
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
        default=lambda: datetime.utcnow() + timedelta(hours=24)  # Default to 24 hours from now
    )
    submit = SubmitField('Create Event')

    def validate_registration_deadline(self, field):
        if field.data >= self.start_date.data:
            raise ValidationError('Registration deadline must be before the event start date.')

    def validate_end_date(self, field):
        if field.data <= self.start_date.data:
            raise ValidationError('End date must be after the start date.')

class EventRegistrationForm(FlaskForm):
    submit = SubmitField('Register for Event')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, URL, Optional

class PitchingRegistrationForm(FlaskForm):
    pitch_title = StringField('Pitch Title', validators=[
        DataRequired(),
        Length(min=5, max=100, message='Pitch title must be between 5 and 100 characters')
    ])
    
    pitch_summary = TextAreaField('Executive Summary', validators=[
        DataRequired(),
        Length(min=50, max=500, message='Executive summary must be between 50 and 500 characters')
    ])
    
    problem_statement = TextAreaField('Problem Statement', validators=[
        DataRequired(),
        Length(min=50, max=1000, message='Problem statement must be between 50 and 1000 characters')
    ])
    
    solution_approach = TextAreaField('Solution Approach', validators=[
        DataRequired(),
        Length(min=50, max=1000, message='Solution approach must be between 50 and 1000 characters')
    ])
    
    market_analysis = TextAreaField('Market Analysis', validators=[
        DataRequired(),
        Length(min=50, max=1000, message='Market analysis must be between 50 and 1000 characters')
    ])
    
    business_model = TextAreaField('Business Model', validators=[
        DataRequired(),
        Length(min=50, max=1000, message='Business model must be between 50 and 1000 characters')
    ])
    
    team_background = TextAreaField('Team Background', validators=[
        DataRequired(),
        Length(min=50, max=1000, message='Team background must be between 50 and 1000 characters')
    ])
    
    pitch_deck_url = URLField('Pitch Deck URL', validators=[
        DataRequired(),
        URL(message='Please enter a valid URL for your pitch deck')
    ])
    
    additional_docs_url = URLField('Additional Documents URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL for additional documents')
    ])
    
    video_pitch_url = URLField('Video Pitch URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL for your video pitch')
    ]) 
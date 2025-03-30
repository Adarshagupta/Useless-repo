from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, URL, Length

class HackathonRegistrationForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    project_description = TextAreaField('Project Description', validators=[DataRequired()])
    tech_stack = StringField('Tech Stack (e.g., Python, React, PostgreSQL)', validators=[DataRequired(), Length(max=255)])
    github_url = URLField('GitHub Repository URL', validators=[Optional(), URL()])
    other_links = TextAreaField('Other Links (Optional)', validators=[Optional()])
    submit = SubmitField('Submit Project') 
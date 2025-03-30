from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Length, URL, Email

class TeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired(), Length(max=100)])
    member_emails = TextAreaField('Team Member Emails (one per line)', validators=[Optional()])
    submit = SubmitField('Create Team')


class TeamJoinForm(FlaskForm):
    team_code = StringField('Team Code', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Join Team')


class HackathonRegistrationForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=100)])
    project_description = TextAreaField('Project Description', validators=[DataRequired()])
    tech_stack = StringField('Technology Stack', validators=[DataRequired(), Length(max=255)])
    github_url = StringField('GitHub Repository URL', validators=[Optional(), URL()])
    other_links = TextAreaField('Other Project Links', validators=[Optional()])
    submit = SubmitField('Register for Hackathon')


class TeamMemberForm(FlaskForm):
    email = StringField('Member Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('project_manager', 'Project Manager'),
        ('other', 'Other')
    ])
    submit = SubmitField('Add Member')

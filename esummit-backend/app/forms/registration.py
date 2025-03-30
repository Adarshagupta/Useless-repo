from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, URL, Length, Email
from flask_wtf.file import FileField, FileAllowed

class EventRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    institution = StringField('Institution/Company', validators=[DataRequired(), Length(max=100)])
    why_join = TextAreaField('Why do you want to join this event?', validators=[Optional(), Length(max=500)])
    experience = TextAreaField('Relevant Experience', validators=[Optional(), Length(max=500)])
    document = FileField('Upload Document (PDF/PPT)', validators=[
        Optional(),
        FileAllowed(['pdf', 'ppt', 'pptx'], 'Please upload only PDF or PowerPoint files.')
    ])
    submit = SubmitField('Register for Event')

class HackathonParticipantForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    institution = StringField('Institution/Company', validators=[DataRequired(), Length(max=100)]) 
    skills = TextAreaField('Technical Skills', validators=[DataRequired(), Length(max=500)])
    experience = TextAreaField('Previous Hackathon Experience', validators=[Optional(), Length(max=500)])
    expectations = TextAreaField('What do you expect to achieve?', validators=[Optional(), Length(max=500)])
    proposal_document = FileField('Project Proposal (PDF/PPT)', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'ppt', 'pptx'], 'Please upload only PDF or PowerPoint files.')
    ])
    github_profile = StringField('GitHub Profile', validators=[Optional(), URL()])
    linkedin_profile = StringField('LinkedIn Profile', validators=[Optional(), URL()])
    dietary_restrictions = StringField('Dietary Restrictions', validators=[Optional(), Length(max=200)])
    tshirt_size = SelectField('T-shirt Size', choices=[
        ('', 'Select Size'),
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large')
    ], validators=[Optional()])
    submit = SubmitField('Register for Hackathon') 
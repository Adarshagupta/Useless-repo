from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from app.models.event import Event
from app.forms.event import EventRegistrationForm as SimpleEventRegistrationForm
from app.forms.registration import EventRegistrationForm, HackathonParticipantForm
from flask_login import current_user, login_required
from app import db
from datetime import datetime
import logging
import os
from werkzeug.utils import secure_filename
import uuid
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from flask_wtf import FlaskForm

main_bp = Blueprint('main', __name__)

# Decorator to handle database errors
def handle_db_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (SQLAlchemyError, OperationalError) as e:
            logging.error(f"Database error in {f.__name__}: {str(e)}")
            db.session.rollback()
            return render_template('errors/db_error.html'), 500
    return decorated_function

# Helper function to save uploaded files
def save_document(uploaded_file):
    if not uploaded_file:
        return None
        
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'documents')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate a unique filename
    filename = secure_filename(uploaded_file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Save the file
    file_path = os.path.join(upload_dir, unique_filename)
    uploaded_file.save(file_path)
    
    return unique_filename

@main_bp.route('/')
def index():
    """Homepage route"""
    events = Event.query.order_by(Event.start_date).all()
    return render_template('main/index.html', events=events)

@main_bp.route('/about')
def about():
    """About page route"""
    return render_template('main/about.html')

@main_bp.route('/events')
def events():
    """Events listing page"""
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of events per page
    
    # Get filtered events
    events_query = Event.query.order_by(Event.start_date)
    
    # Apply filters if provided
    event_type = request.args.get('type')
    status = request.args.get('status')
    search = request.args.get('search')
    
    if event_type:
        events_query = events_query.filter_by(event_type=event_type)
    if status:
        events_query = events_query.filter_by(status=status)
    if search:
        events_query = events_query.filter(Event.name.ilike(f'%{search}%'))
    
    # Get paginated results
    pagination = events_query.paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items
    
    return render_template('main/events.html', events=events, pagination=pagination)

@main_bp.route('/events/<int:event_id>')
@handle_db_errors
def event_details(event_id):
    """Event details page"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is registered
    is_registered = False
    registration = None
    if current_user.is_authenticated:
        # Get the actual registration if it exists
        from app.models.registration import EventRegistration
        registration = EventRegistration.query.filter_by(
            user_id=current_user.id,
            event_id=event_id
        ).first()
        
        is_registered = registration is not None
    
    # Create a registration form
    form = EventRegistrationForm() if event.event_type != 'hackathon' else HackathonParticipantForm()
    
    # Create team forms if it's a team event
    team_form = None
    join_form = None
    if event.is_team_event:
        from app.forms.team import TeamForm, TeamJoinForm
        team_form = TeamForm()
        join_form = TeamJoinForm()
    
    return render_template('main/event_details.html', 
                           event=event, 
                           is_registered=is_registered,
                           registration=registration,
                           form=form,
                           team_form=team_form,
                           join_form=join_form)

@main_bp.route('/hackathons')
def hackathons():
    """Hackathons listing page"""
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of hackathons per page
    
    # Get filtered hackathons
    hackathons_query = Event.query.filter_by(event_type='hackathon').order_by(Event.start_date)
    
    # Apply filters if provided
    status = request.args.get('status')
    prize = request.args.get('prize')
    search = request.args.get('search')
    
    if status:
        hackathons_query = hackathons_query.filter_by(status=status)
    if prize:
        hackathons_query = hackathons_query.filter(Event.prize_pool >= int(prize))
    if search:
        hackathons_query = hackathons_query.filter(Event.name.ilike(f'%{search}%'))
    
    # Get paginated results
    pagination = hackathons_query.paginate(page=page, per_page=per_page, error_out=False)
    hackathons = pagination.items
    
    return render_template('main/hackathons.html', hackathons=hackathons, pagination=pagination)

@main_bp.route('/contact')
def contact():
    """Contact page route"""
    return render_template('main/contact.html')

@main_bp.route('/hackathons/<int:hackathon_id>')
@handle_db_errors
def hackathon_details(hackathon_id):
    """Hackathon details page"""
    hackathon = Event.query.filter_by(id=hackathon_id, event_type='hackathon').first_or_404()
    
    # Check if user is registered
    is_registered = False
    registration = None
    if current_user.is_authenticated:
        # Get the actual registration if it exists
        from app.models.registration import EventRegistration
        registration = EventRegistration.query.filter_by(
            user_id=current_user.id,
            event_id=hackathon_id
        ).first()
        
        is_registered = registration is not None
    
    # Create registration form
    form = HackathonParticipantForm()
    
    # Create team forms since hackathons are team events
    from app.forms.team import TeamForm, TeamJoinForm
    team_form = TeamForm()
    join_form = TeamJoinForm()
    
    return render_template('main/event_details.html', 
                           event=hackathon, 
                           is_registered=is_registered,
                           registration=registration,
                           form=form,
                           team_form=team_form,
                           join_form=join_form)

@main_bp.route('/register/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def register_event(event_id):
    """Register for an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if registration is open
    if not event.is_registration_open:
        flash('Registration is closed for this event.', 'warning')
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Check if already registered
    if event.is_registered(current_user):
        flash('You are already registered for this event.', 'info')
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Get the appropriate form
    form = EventRegistrationForm() if event.event_type != 'hackathon' else HackathonParticipantForm()
    
    if form.validate_on_submit():
        try:
            # Handle document upload
            document_filename = None
            if hasattr(form, 'document') and form.document.data:
                document_filename = save_document(form.document.data)
            elif hasattr(form, 'proposal_document') and form.proposal_document.data:
                document_filename = save_document(form.proposal_document.data)
                
            # Create registration
            from app.models.registration import EventRegistration
            registration = EventRegistration(
                user_id=current_user.id,
                event_id=event_id,
                status='confirmed',
                registration_date=datetime.utcnow(),
                full_name=form.name.data if hasattr(form, 'name') else None,
                email=form.email.data if hasattr(form, 'email') else None,
                phone=form.phone.data if hasattr(form, 'phone') else None,
                institution=form.institution.data if hasattr(form, 'institution') else None,
                why_join=form.why_join.data if hasattr(form, 'why_join') else None,
                experience=form.experience.data if hasattr(form, 'experience') else None,
                document_filename=document_filename
            )
            db.session.add(registration)
            
            db.session.commit()
            flash('You have successfully registered for this event!', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')
    
    return redirect(url_for('main.event_details', event_id=event_id))

@main_bp.route('/create_team/<int:event_id>', methods=['POST'])
@login_required
def create_team(event_id):
    """Create a team for an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if the event allows teams
    if not event.is_team_event:
        flash('This event does not support team participation.', 'danger')
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Check if user is already registered
    if event.is_registered(current_user):
        flash('You are already registered for this event.', 'warning')
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Get form data
    from app.forms.team import TeamForm
    team_form = TeamForm()
    
    if team_form.validate_on_submit():
        try:
            # Create the team
            from app.models.team import Team, TeamMember
            team = Team(
                name=team_form.name.data,
                leader_id=current_user.id,
                event_id=event_id
            )
            db.session.add(team)
            db.session.flush()  # Get the team ID
            
            # Add the leader as a team member
            team_member = TeamMember(
                team_id=team.id,
                user_id=current_user.id,
                role='leader'
            )
            db.session.add(team_member)
            
            # Create event registration linked to the team
            from app.models.registration import EventRegistration
            registration = EventRegistration(
                user_id=current_user.id,
                event_id=event_id,
                status='confirmed',
                registration_date=datetime.utcnow(),
                team_id=team.id
            )
            db.session.add(registration)
            
            db.session.commit()
            flash(f'Team "{team.name}" created successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            import traceback
            error_tb = traceback.format_exc()
            logging.error(f"Team creation error: {str(e)}")
            logging.error(f"Error details: {error_tb}")
            flash('An error occurred while creating the team.', 'danger')
    else:
        for field, errors in team_form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
    
    return redirect(url_for('main.event_details', event_id=event_id))

@main_bp.route('/join_team/<int:event_id>', methods=['POST'])
@login_required
def join_team(event_id):
    """Join an existing team"""
    event = Event.query.get_or_404(event_id)
    
    # Check if the event allows teams
    if not event.is_team_event:
        flash('This event does not support team participation.', 'danger')
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Check if user is already registered
    if event.is_registered(current_user):
        flash('You are already registered for this event.', 'warning')
        return redirect(url_for('main.event_details', event_id=event_id))
    
    # Get form data
    from app.forms.team import TeamJoinForm
    join_form = TeamJoinForm()
    
    if join_form.validate_on_submit():
        try:
            team_code = join_form.team_code.data
            
            # Find the team
            from app.models.team import Team, TeamMember
            
            # Try to convert to integer for ID lookup
            try:
                team_id = int(team_code)
                team = Team.query.filter_by(id=team_id, event_id=event_id).first()
            except ValueError:
                # If not an integer, maybe it's a name
                team = Team.query.filter_by(name=team_code, event_id=event_id).first()
            
            if not team:
                flash('Team not found. Please check the code and try again.', 'warning')
                return redirect(url_for('main.event_details', event_id=event_id))
            
            # Check if team is full
            team_members = TeamMember.query.filter_by(team_id=team.id).count()
            if event.max_team_size and team_members >= event.max_team_size:
                flash('This team is already full.', 'warning')
                return redirect(url_for('main.event_details', event_id=event_id))
            
            # Add user to team
            team_member = TeamMember(
                team_id=team.id,
                user_id=current_user.id,
                role='member'
            )
            db.session.add(team_member)
            
            # Create event registration linked to the team
            from app.models.registration import EventRegistration
            registration = EventRegistration(
                user_id=current_user.id,
                event_id=event_id,
                status='confirmed',
                registration_date=datetime.utcnow(),
                team_id=team.id
            )
            db.session.add(registration)
            
            db.session.commit()
            flash(f'You have joined the team "{team.name}"!', 'success')
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Team join error: {str(e)}")
            flash('An error occurred while joining the team.', 'danger')
    else:
        for field, errors in join_form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
    
    return redirect(url_for('main.event_details', event_id=event_id))

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.event import Event
from app.models.registration import EventRegistration, HackathonRegistration
from app.models.team import Team, TeamMember
from app.forms.event import EventRegistrationForm, EventForm
from app.forms.team import TeamForm, TeamJoinForm, TeamMemberForm
from app.forms.hackathon import HackathonRegistrationForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from datetime import datetime
import psycopg2
import os
import logging

# Define the ProfileForm here since it's not in a separate file
class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    college = StringField('College/University', validators=[Optional(), Length(max=100)])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        Optional(), EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Update Profile')

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """User dashboard home"""
    # Get user's registrations
    registered_events = EventRegistration.query.filter_by(user_id=current_user.id).all()
    
    # Get user's teams
    teams = Team.query.filter_by(leader_id=current_user.id).all()
    team_memberships = TeamMember.query.filter_by(user_id=current_user.id).all()
    
    # Get upcoming events
    upcoming_events = Event.query.filter(Event.end_date > datetime.utcnow()).order_by(Event.start_date).limit(5).all()
    
    return render_template('dashboard/index.html',
                         registered_events=registered_events,
                         teams=teams,
                         team_memberships=team_memberships,
                         upcoming_events=upcoming_events)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile route"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        # Check if current password is correct
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return render_template('dashboard/profile.html', form=form)
        
        # Update the user's information
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.college = form.college.data
        
        # Update password if a new one was provided
        if form.new_password.data:
            from app.models.user import bcrypt
            current_user.password_hash = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            
        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('dashboard.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            
    return render_template('dashboard/profile.html', form=form)

@dashboard_bp.route('/faq')
@login_required
def faq():
    """FAQ and instructions page"""
    return render_template('dashboard/faq.html')

@dashboard_bp.route('/events')
@login_required
def events():
    """List all available events"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    event_type = request.args.get('event_type')
    
    events_query = Event.query.filter(Event.end_date > datetime.utcnow())
    
    # Apply filters
    if event_type:
        events_query = events_query.filter_by(event_type=event_type)
    
    # Get paginated results
    pagination = events_query.paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items
    
    return render_template('dashboard/events.html', 
                         events=events, 
                         pagination=pagination,
                         event_type=event_type)

@dashboard_bp.route('/event/<int:event_id>/register', methods=['GET', 'POST'])
@login_required
def register_event(event_id):
    """Register for an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if registration is still open
    if not event.is_registration_open:
        flash('Registration for this event is closed.', 'danger')
        return redirect(url_for('dashboard.events'))
    
    # Check if event is full
    if event.is_full:
        flash('This event is full.', 'danger')
        return redirect(url_for('dashboard.events'))
    
    # Check if already registered
    existing_reg = EventRegistration.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first()
    
    if existing_reg:
        flash('You are already registered for this event.', 'info')
        return redirect(url_for('dashboard.events'))
    
    # Create registration
    registration = EventRegistration(
        user_id=current_user.id,
        event_id=event_id
    )
    db.session.add(registration)
    db.session.commit()
    
    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('dashboard.events'))

@dashboard_bp.route('/teams')
@login_required
def teams():
    """List user's teams"""
    # Teams where user is leader
    teams_led = Team.query.filter_by(leader_id=current_user.id).all()
    
    # Teams where user is a member (but not leader)
    teams_joined = Team.query.join(TeamMember).filter(
        TeamMember.user_id == current_user.id,
        Team.leader_id != current_user.id
    ).all()
    
    return render_template('dashboard/teams.html',
                         teams_led=teams_led,
                         teams_joined=teams_joined)

@dashboard_bp.route('/team/create/<int:event_id>', methods=['GET', 'POST'])
@login_required
def create_team(event_id):
    """Create a new team"""
    event = Event.query.get_or_404(event_id)
    
    # Check if event allows teams
    if not event.is_team_event:
        flash('This event does not support team participation.', 'danger')
        return redirect(url_for('dashboard.events'))
    
    form = TeamForm()
    if form.validate_on_submit():
        try:
            # Create team
            team = Team(
                name=form.name.data,
                leader_id=current_user.id,
                event_id=event_id
            )
            db.session.add(team)
            db.session.commit()
            
            # Add leader as team member
            member = TeamMember(
                team_id=team.id,
                user_id=current_user.id,
                role='leader'
            )
            db.session.add(member)
            
            # Add other members if provided
            if form.member_emails.data:
                emails = [email.strip() for email in form.member_emails.data.split(',') if email.strip()]
                for email in emails:
                    user = User.query.filter_by(email=email).first()
                    if user:
                        member = TeamMember(
                            team_id=team.id,
                            user_id=user.id,
                            role='member'
                        )
                        db.session.add(member)
            
            db.session.commit()
            
            # Add additional message for hackathons, reminding users to complete registration
            if event.event_type == 'hackathon':
                flash('Team created successfully! Please complete your hackathon registration to finalize your participation.', 'warning')
            else:
                flash('Team created successfully!', 'success')
                
            # Redirect directly to the team details page
            return redirect(url_for('dashboard.team_details', team_id=team.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the team. Please try again.', 'danger')
            return redirect(url_for('dashboard.events'))
    
    return render_template('dashboard/create_team.html', form=form, event=event)

@dashboard_bp.route('/team/<int:team_id>/add-member', methods=['GET', 'POST'])
@login_required
def add_team_member(team_id):
    """Add a member to a team"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team leader
    if team.leader_id != current_user.id:
        flash('You do not have permission to add members to this team.', 'danger')
        return redirect(url_for('dashboard.teams'))
    
    form = TeamMemberForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                flash('User with this email not found.', 'danger')
            else:
                # Check if user is already in team
                existing_member = TeamMember.query.filter_by(
                    team_id=team.id,
                    user_id=user.id
                ).first()
                
                if existing_member:
                    flash('This user is already a team member.', 'warning')
                else:
                    member = TeamMember(
                        team_id=team.id,
                        user_id=user.id,
                        role=form.role.data
                    )
                    db.session.add(member)
                    db.session.commit()
                    flash('Team member added successfully!', 'success')
                    return redirect(url_for('dashboard.team_details', team_id=team.id))
                    
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the team member. Please try again.', 'danger')
    
    return render_template('dashboard/add_team_member.html', form=form, team=team)

@dashboard_bp.route('/team/<int:team_id>')
@login_required
def team_details(team_id):
    """View team details"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team leader or member
    is_member = TeamMember.query.filter_by(
        team_id=team.id,
        user_id=current_user.id
    ).first() is not None
    
    # Allow access if user is admin, team leader, or team member
    if not current_user.is_admin and team.leader_id != current_user.id and not is_member:
        flash('You do not have permission to view this team.', 'danger')
        return redirect(url_for('dashboard.teams'))
    
    return render_template('dashboard/team_details.html', team=team)

@dashboard_bp.route('/team/<int:team_id>/register-hackathon', methods=['GET', 'POST'])
@login_required
def register_hackathon(team_id):
    """Register team for hackathon"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team leader
    if team.leader_id != current_user.id:
        flash('Only team leaders can register for hackathons.', 'danger')
        return redirect(url_for('dashboard.team_details', team_id=team.id))
    
    # Check if event is a hackathon
    if not team.event or team.event.event_type != 'hackathon':
        flash('This event is not a hackathon.', 'danger')
        return redirect(url_for('dashboard.team_details', team_id=team.id))
    
    # Check if already registered
    existing_reg = HackathonRegistration.query.filter_by(
        team_id=team.id,
        event_id=team.event.id
    ).first()
    
    if existing_reg:
        flash('Your team is already registered for this hackathon.', 'info')
        return redirect(url_for('dashboard.team_details', team_id=team.id))
    
    form = HackathonRegistrationForm()
    if form.validate_on_submit():
        try:
            registration = HackathonRegistration(
                team_id=team.id,
                event_id=team.event.id,
                project_name=form.project_name.data,
                project_description=form.project_description.data,
                tech_stack=form.tech_stack.data,
                github_url=form.github_url.data,
                other_links=form.other_links.data
            )
            db.session.add(registration)
            db.session.commit()
            
            flash('Successfully registered for the hackathon!', 'success')
            return redirect(url_for('dashboard.team_details', team_id=team.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering for the hackathon. Please try again.', 'danger')
    
    return render_template('dashboard/register_hackathon.html', form=form, team=team, event=team.event)

@dashboard_bp.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create a new event"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to create events.', 'danger')
        return redirect(url_for('dashboard.events'))
    
    form = EventForm()
    if form.validate_on_submit():
        try:
            # Use direct SQL for event creation
            # Get database URL from environment
            db_url = os.environ.get('DATABASE_URL')
            conn_parts = db_url.split('://')[1].split('@')
            user_pass = conn_parts[0].split(':')
            host_db = conn_parts[1].split('/')
            
            username = user_pass[0]
            password = user_pass[1]
            host = host_db[0].split('?')[0]
            if '-pooler' in host:
                host = host.replace('-pooler', '')
            dbname = host_db[1].split('?')[0]
            
            # Connect directly with psycopg2
            conn = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=username,
                password=password,
                sslmode='require'
            )
            conn.autocommit = True
            
            with conn.cursor() as cursor:
                # Insert the event
                now = datetime.utcnow()
                cursor.execute("""
                    INSERT INTO event (
                        name, description, start_date, end_date, venue, 
                        registration_deadline, capacity, event_type, 
                        is_team_event, min_team_size, max_team_size, 
                        image_url, created_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, 
                        %s, %s, %s, 
                        %s, %s, %s, 
                        %s, %s
                    ) RETURNING id
                """, (
                    form.name.data, 
                    form.description.data,
                    form.start_date.data,
                    form.end_date.data,
                    form.venue.data,
                    form.registration_deadline.data,
                    form.capacity.data,
                    form.event_type.data,
                    form.is_team_event.data,
                    form.min_team_size.data if form.is_team_event.data else None,
                    form.max_team_size.data if form.is_team_event.data else None,
                    form.image_url.data if hasattr(form, 'image_url') and form.image_url.data else None,
                    now
                ))
                event_id = cursor.fetchone()[0]
                print(f"Created event with ID: {event_id}")
            
            flash('Event created successfully!', 'success')
            return redirect(url_for('dashboard.events'))
            
        except Exception as e:
            import traceback
            print(f"Error creating event: {str(e)}")
            print(traceback.format_exc())
            flash('An error occurred while creating the event. Please try again.', 'danger')
    
    return render_template('dashboard/create_event.html', form=form)

@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard home"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get counts for admin dashboard
    user_count = User.query.count()
    event_count = Event.query.count()
    team_count = Team.query.count()
    registration_count = EventRegistration.query.count()
    hackathon_count = HackathonRegistration.query.count()
    
    return render_template('dashboard/admin/index.html',
                         user_count=user_count,
                         event_count=event_count,
                         team_count=team_count,
                         registration_count=registration_count,
                         hackathon_count=hackathon_count)

@dashboard_bp.route('/admin/users')
@login_required
def admin_users():
    """Admin user management"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    search = request.args.get('search', '')
    
    # Query users with optional search
    query = User.query
    if search:
        query = query.filter(
            (User.email.ilike(f'%{search}%')) | 
            (User.full_name.ilike(f'%{search}%'))
        )
    
    pagination = query.order_by(User.id).paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    
    return render_template('dashboard/admin/users.html', 
                         users=users, 
                         pagination=pagination,
                         search=search)

@dashboard_bp.route('/admin/events')
@login_required
def admin_events():
    """Admin event management"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 15
    event_type = request.args.get('event_type')
    
    # Query events with optional filter
    query = Event.query
    if event_type:
        query = query.filter_by(event_type=event_type)
    
    pagination = query.order_by(Event.start_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items
    
    # Add current datetime for status comparisons
    now = datetime.now()
    
    return render_template('dashboard/admin/events.html', 
                         events=events, 
                         pagination=pagination,
                         event_type=event_type,
                         now=now)

@dashboard_bp.route('/admin/teams')
@login_required
def admin_teams():
    """Admin team management"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 15
    event_id = request.args.get('event_id', type=int)
    
    # Query teams with optional filter
    query = Team.query
    if event_id:
        query = query.filter_by(event_id=event_id)
    
    pagination = query.order_by(Team.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    teams = pagination.items
    
    # Get all events for filter dropdown
    events = Event.query.filter_by(is_team_event=True).all()
    
    return render_template('dashboard/admin/teams.html', 
                         teams=teams, 
                         pagination=pagination,
                         events=events,
                         selected_event_id=event_id)

@dashboard_bp.route('/admin/registrations')
@login_required
def admin_registrations():
    """Admin registration management"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    event_id = request.args.get('event_id', type=int)
    
    # Query registrations with optional filter
    query = EventRegistration.query
    if event_id:
        query = query.filter_by(event_id=event_id)
    
    pagination = query.order_by(EventRegistration.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    registrations = pagination.items
    
    # Get all events for filter dropdown
    events = Event.query.all()
    
    return render_template('dashboard/admin/registrations.html', 
                         registrations=registrations, 
                         pagination=pagination,
                         events=events,
                         selected_event_id=event_id)

@dashboard_bp.route('/admin/registrations/<int:registration_id>')
@login_required
def admin_registration_details(registration_id):
    """Admin view of registration details"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get the registration
    registration = EventRegistration.query.get_or_404(registration_id)
    
    return render_template('dashboard/admin/registration_details.html',
                         registration=registration)

@dashboard_bp.route('/admin/hackathons')
@login_required
def admin_hackathons():
    """Admin hackathon registration management"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 15
    event_id = request.args.get('event_id', type=int)
    
    # Query hackathon registrations with optional filter
    query = HackathonRegistration.query
    if event_id:
        query = query.filter_by(event_id=event_id)
    
    pagination = query.order_by(HackathonRegistration.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    hackathon_regs = pagination.items
    
    # Get hackathon events for filter dropdown
    hackathon_events = Event.query.filter_by(event_type='hackathon').all()
    
    return render_template('dashboard/admin/hackathons.html', 
                         hackathon_regs=hackathon_regs, 
                         pagination=pagination,
                         events=hackathon_events,
                         selected_event_id=event_id)

@dashboard_bp.route('/admin/user/<int:user_id>')
@login_required
def admin_user_details(user_id):
    """Admin view of user details"""
    # Check if user has admin privileges
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    user = User.query.get_or_404(user_id)
    
    # Get user's registrations
    registrations = EventRegistration.query.filter_by(user_id=user.id).all()
    
    # Get user's teams
    teams_led = Team.query.filter_by(leader_id=user.id).all()
    team_memberships = TeamMember.query.filter_by(user_id=user.id).all()
    
    return render_template('dashboard/admin/user_details.html',
                         user=user,
                         registrations=registrations,
                         teams_led=teams_led,
                         team_memberships=team_memberships)

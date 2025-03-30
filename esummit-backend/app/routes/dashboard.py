from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.event import Event
from app.models.registration import EventRegistration, HackathonRegistration
from app.models.team import Team, TeamMember
from app.forms.event import EventRegistrationForm, EventForm
from app.forms.team import TeamForm, TeamJoinForm, HackathonRegistrationForm
from app.forms.hackathon import HackathonRegistrationForm
from app.forms.team import TeamMemberForm
from datetime import datetime
import psycopg2
import os
import logging

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
    return render_template('dashboard/profile.html')

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
            flash('Team created successfully!', 'success')
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
    
    if team.leader_id != current_user.id and not is_member:
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

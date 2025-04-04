from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db, with_transaction
from app.models.user import User
from app.models.event import Event
from app.models.registration import EventRegistration, HackathonRegistration
from app.models.team import Team, TeamMember
from app.models.announcement import Announcement
from app.models.notification import Notification
from app.forms.event import EventForm
from datetime import datetime
from app.tasks import send_announcement_email
import logging
from functools import wraps
import psycopg2
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin decorator
def admin_required(f):
    def admin_check_wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    admin_check_wrapper.__name__ = f.__name__
    return login_required(admin_check_wrapper)

@admin_bp.route('/')
@admin_required
def index():
    """Admin dashboard"""
    # Get summary stats
    try:
        event_count = Event.query.count()
        user_count = User.query.count()
        active_registrations = EventRegistration.query.filter_by(status='confirmed').count()
        
        # Get upcoming events
        upcoming_events = Event.query.filter(Event.start_date > datetime.utcnow()).order_by(Event.start_date).limit(5).all()
        
        return render_template('admin/index.html', 
                             event_count=event_count,
                             user_count=user_count,
                             active_registrations=active_registrations,
                             upcoming_events=upcoming_events)
    except Exception as e:
        logging.error(f"Error loading admin dashboard: {str(e)}")
        flash('An error occurred while loading the dashboard.', 'danger')
        return render_template('admin/index.html')

@admin_bp.route('/events')
@admin_required
def events():
    """List all events"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Number of events per page
        
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
        
        return render_template('admin/events.html', 
                             events=events, 
                             pagination=pagination,
                             now=datetime.utcnow())
    except Exception as e:
        logging.error(f"Error in events list: {str(e)}")
        flash('An error occurred while loading events.', 'danger')
        return redirect(url_for('admin.index'))

@admin_bp.route('/events/create', methods=['GET', 'POST'])
@admin_required
def create_event():
    """Create a new event"""
    form = EventForm()
    if form.validate_on_submit():
        try:
            logging.info("Form data: %s", form.data)
            
            # Check if we're using SQLite
            use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true'
            
            if use_sqlite:
                # Use SQLAlchemy to create event
                event = Event(
                    name=form.name.data,
                    description=form.description.data,
                    subtitle=form.subtitle.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    venue=form.venue.data,
                    registration_deadline=form.registration_deadline.data,
                    capacity=form.capacity.data,
                    event_type=form.event_type.data,
                    is_team_event=form.is_team_event.data,
                    min_team_size=form.min_team_size.data if form.is_team_event.data else None,
                    max_team_size=form.max_team_size.data if form.is_team_event.data else None,
                    image_url=form.image_url.data
                )
                db.session.add(event)
                db.session.commit()
                logging.info(f"Event created with ID: {event.id}")
            else:
                # Use direct SQL to create event instead of SQLAlchemy
                # Get database URL from environment
                db_url = os.environ.get('DATABASE_URL')
                conn_parts = db_url.split('://')[1].split('@')
                user_pass = conn_parts[0].split(':')
                host_db = conn_parts[1].split('/')
                
                username = user_pass[0]
                password = user_pass[1]
                host = host_db[0].split('?')[0]
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
                            name, description, subtitle, start_date, end_date, venue, 
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
                        form.image_url.data,
                        now
                    ))
                    event_id = cursor.fetchone()[0]
                    logging.info(f"Event created with ID: {event_id}")
            
            flash('Event created successfully!', 'success')
            return redirect(url_for('admin.events'))
            
        except Exception as e:
            logging.error("Error creating event: %s", str(e))
            logging.error("Error type: %s", type(e))
            import traceback
            logging.error("Traceback: %s", traceback.format_exc())
            flash('An error occurred while creating the event. Please try again.', 'danger')
    elif form.errors:
        logging.warning("Form validation errors: %s", form.errors)
        flash('Please check the form for errors.', 'danger')
    
    return render_template('admin/create_event.html', form=form, title='Create Event', now=datetime.utcnow())

@admin_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
@with_transaction
def edit_event(event_id):
    """Edit an event"""
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'GET':
        # Populate form with event data
        form = EventForm(
            name=event.name,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            venue=event.venue,
            capacity=event.capacity,
            event_type=event.event_type,
            is_team_event=event.is_team_event,
            min_team_size=event.min_team_size,
            max_team_size=event.max_team_size,
            image_url=event.image_url,
            registration_deadline=event.registration_deadline
        )
    else:
        form = EventForm()
    
    if form.validate_on_submit():
        try:
            event.name = form.name.data
            event.description = form.description.data
            event.start_date = form.start_date.data
            event.end_date = form.end_date.data
            event.venue = form.venue.data
            event.capacity = form.capacity.data
            event.event_type = form.event_type.data
            event.is_team_event = form.is_team_event.data
            event.min_team_size = form.min_team_size.data if form.is_team_event.data else None
            event.max_team_size = form.max_team_size.data if form.is_team_event.data else None
            event.image_url = form.image_url.data
            event.registration_deadline = form.registration_deadline.data
            
            flash('Event updated successfully!', 'success')
            return redirect(url_for('admin.events'))
        except Exception as e:
            logging.error("Error updating event: %s", str(e))
            flash('An error occurred while updating the event. Please try again.', 'danger')
            raise
    elif request.method == 'POST':
        flash('Please check the form for errors.', 'danger')
    
    return render_template('admin/edit_event.html', form=form, event=event, title='Edit Event')

@admin_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@admin_required
@with_transaction
def delete_event(event_id):
    """Delete an event"""
    try:
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        flash('Event deleted successfully!', 'success')
        return redirect(url_for('admin.events'))
    except Exception as e:
        logging.error("Error deleting event: %s", str(e))
        flash('An error occurred while deleting the event. Please try again.', 'danger')
        raise

@admin_bp.route('/users')
@admin_required
def users():
    """List all users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Number of users per page
        
        # Get filtered users
        users_query = User.query.order_by(User.created_at.desc())
        
        # Apply filters if provided
        role = request.args.get('role')
        status = request.args.get('status')
        search = request.args.get('search')
        
        if role:
            users_query = users_query.filter_by(is_admin=(role == 'admin'))
        if status:
            users_query = users_query.filter_by(is_active=(status == 'active'))
        if search:
            users_query = users_query.filter(
                (User.username.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%')) |
                (User.full_name.ilike(f'%{search}%'))
            )
        
        # Get paginated results
        pagination = users_query.paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template('admin/users.html', 
                             users=pagination,
                             pagination=pagination)
    except Exception as e:
        logging.error("Error in users list: %s", str(e))
        flash('An error occurred while loading users.', 'danger')
        return redirect(url_for('admin.index'))

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for a user"""
    user = User.query.get_or_404(user_id)
    
    # Don't allow demoting yourself
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for {user.username}!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/registrations')
@admin_required
def registrations():
    """List all event registrations"""
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of registrations per page
    
    # Get filtered registrations
    registrations_query = EventRegistration.query.order_by(EventRegistration.registration_date.desc())
    
    # Apply filters if provided
    event_id = request.args.get('event')
    status = request.args.get('status')
    search = request.args.get('search')
    
    if event_id:
        registrations_query = registrations_query.filter_by(event_id=event_id)
    if status:
        registrations_query = registrations_query.filter_by(status=status)
    if search:
        registrations_query = registrations_query.join(User).filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    
    # Get paginated results
    pagination = registrations_query.paginate(page=page, per_page=per_page, error_out=False)
    registrations = pagination.items
    
    # Get all events for the filter dropdown
    events = Event.query.order_by(Event.start_date.desc()).all()
    
    return render_template('admin/registrations.html', 
                         registrations=registrations, 
                         pagination=pagination,
                         events=events)

@admin_bp.route('/registrations/<int:registration_id>/approve', methods=['POST'])
@admin_required
def approve_registration(registration_id):
    """Approve an event registration"""
    registration = EventRegistration.query.get_or_404(registration_id)
    registration.status = 'approved'
    db.session.commit()
    flash(f'Registration approved for {registration.user.full_name}!', 'success')
    return redirect(url_for('admin.registrations'))

@admin_bp.route('/registrations/<int:registration_id>/reject', methods=['POST'])
@admin_required
def reject_registration(registration_id):
    """Reject an event registration"""
    registration = EventRegistration.query.get_or_404(registration_id)
    registration.status = 'rejected'
    registration.rejection_reason = request.form.get('reason')
    db.session.commit()
    flash(f'Registration rejected for {registration.user.full_name}!', 'success')
    return redirect(url_for('admin.registrations'))

@admin_bp.route('/registrations/<int:registration_id>')
@admin_required
def view_registration(registration_id):
    """View registration details"""
    registration = EventRegistration.query.get_or_404(registration_id)
    return render_template('admin/view_registration.html', registration=registration)

@admin_bp.route('/hackathons')
@admin_required
def hackathons():
    """List all hackathon registrations"""
    hackathon_registrations = HackathonRegistration.query.order_by(HackathonRegistration.registration_date.desc()).all()
    return render_template('admin/hackathons.html', hackathon_registrations=hackathon_registrations)

@admin_bp.route('/teams')
@admin_required
def teams():
    """List all teams"""
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of teams per page
    
    # Get filtered teams
    teams_query = Team.query.order_by(Team.created_at.desc())
    
    # Apply filters if provided
    event_id = request.args.get('event')
    status = request.args.get('status')
    search = request.args.get('search')
    
    if event_id:
        teams_query = teams_query.filter_by(event_id=event_id)
    if status:
        teams_query = teams_query.filter_by(status=status)
    if search:
        teams_query = teams_query.filter(Team.name.ilike(f'%{search}%'))
    
    # Get paginated results
    pagination = teams_query.paginate(page=page, per_page=per_page, error_out=False)
    teams = pagination.items
    
    # Get all events for the filter dropdown
    events = Event.query.filter_by(is_team_event=True).order_by(Event.start_date.desc()).all()
    
    return render_template('admin/teams.html', 
                         teams=teams, 
                         pagination=pagination,
                         events=events)

@admin_bp.route('/teams/<int:team_id>/approve', methods=['POST'])
@admin_required
def approve_team(team_id):
    """Approve a team"""
    team = Team.query.get_or_404(team_id)
    team.status = 'approved'
    db.session.commit()
    flash(f'Team {team.name} has been approved!', 'success')
    return redirect(url_for('admin.teams'))

@admin_bp.route('/teams/<int:team_id>/reject', methods=['POST'])
@admin_required
def reject_team(team_id):
    """Reject a team"""
    team = Team.query.get_or_404(team_id)
    team.status = 'rejected'
    team.rejection_reason = request.form.get('reason')
    db.session.commit()
    flash(f'Team {team.name} has been rejected!', 'success')
    return redirect(url_for('admin.teams'))

@admin_bp.route('/teams/<int:team_id>')
@admin_required
def view_team(team_id):
    """View team details"""
    team = Team.query.get_or_404(team_id)
    return render_template('admin/view_team.html', team=team)

@admin_bp.route('/export/registrations', methods=['POST'])
@admin_required
def export_registrations():
    """Export registrations data"""
    format = request.form.get('format', 'csv')
    fields = request.form.getlist('fields')
    
    # Get all registrations
    registrations = EventRegistration.query.order_by(EventRegistration.registration_date.desc()).all()
    
    # Create CSV or Excel file
    if format == 'csv':
        # Implement CSV export
        pass
    else:
        # Implement Excel export
        pass
    
    flash('Export started! You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('admin.registrations'))

@admin_bp.route('/export/teams', methods=['POST'])
@admin_required
def export_teams():
    """Export teams data"""
    format = request.form.get('format', 'csv')
    fields = request.form.getlist('fields')
    
    # Get all teams
    teams = Team.query.order_by(Team.created_at.desc()).all()
    
    # Create CSV or Excel file
    if format == 'csv':
        # Implement CSV export
        pass
    else:
        # Implement Excel export
        pass
    
    flash('Export started! You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('admin.teams'))

@admin_bp.route('/send-announcement', methods=['GET', 'POST'])
@admin_required
def send_announcement():
    if request.method == 'GET':
        events = Event.query.all()
        return render_template('admin/send_announcement.html', events=events)
    
    title = request.form.get('title')
    message = request.form.get('message')
    target = request.form.get('target')
    event_id = request.form.get('event')
    send_email = request.form.get('send_email') == 'on'
    
    if not title or not message or not target:
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('admin.send_announcement'))
    
    users = []
    if target == 'all':
        users = User.query.filter_by(is_active=True).all()
    elif target == 'event' and event_id:
        event = Event.query.get_or_404(event_id)
        users = [reg.user for reg in event.registrations if reg.user.is_active]
    
    announcement = Announcement(
        title=title,
        message=message,
        sender_id=current_user.id,
        event_id=event_id if target == 'event' else None
    )
    db.session.add(announcement)
    
    for user in users:
        notification = Notification(
            user_id=user.id,
            announcement_id=announcement.id,
            type='announcement'
        )
        db.session.add(notification)
        if send_email:
            send_announcement_email.delay(user.email, title, message, current_user.full_name)
    
    db.session.commit()
    flash(f'Announcement sent to {len(users)} users', 'success')
    return redirect(url_for('admin.index'))

@admin_bp.route('/export-data', methods=['GET', 'POST'])
@admin_required
def export_data():
    """Export application data"""
    if request.method == 'POST':
        data_type = request.form.get('type')
        format = request.form.get('format')
        
        # Export data based on type
        if data_type == 'events':
            data = Event.query.all()
        elif data_type == 'users':
            data = User.query.all()
        elif data_type == 'teams':
            data = Team.query.all()
        elif data_type == 'registrations':
            data = EventRegistration.query.all()
        else:
            data = []
        
        # Create export file
        if format == 'csv':
            # Implement CSV export
            pass
        else:
            # Implement Excel export
            pass
        
        flash('Export started! You will receive an email when it\'s ready.', 'info')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/export_data.html')

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.event import Event
from app.models.registration import EventRegistration, HackathonRegistration, PitchRegistration
from app.models.team import Team, TeamMember
from app.models.activity import ActivityLog
from functools import wraps
from datetime import datetime, timedelta
import logging

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

# Staff required decorator
def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@staff_bp.route('/')
@login_required
@staff_required
def index():
    """Staff dashboard home"""
    # Get active events
    active_events = Event.query.filter(
        (Event.start_date <= datetime.utcnow() + timedelta(days=7)) &
        (Event.end_date >= datetime.utcnow())
    ).all()

    # Get pending registrations
    pending_registrations = EventRegistration.query.filter_by(status='pending').order_by(EventRegistration.registration_date.desc()).limit(10).all()

    # Get total participants
    total_participants = EventRegistration.query.filter_by(status='confirmed').count()

    # Get total teams
    total_teams = Team.query.count()

    # Get recent activities
    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()

    # Add activity type information for icons and colors
    for activity in recent_activities:
        if activity.activity_type == 'registration':
            activity.type_icon = 'clipboard-list'
            activity.type_color = 'primary'
        elif activity.activity_type == 'check_in':
            activity.type_icon = 'clipboard-check'
            activity.type_color = 'success'
        elif activity.activity_type == 'team':
            activity.type_icon = 'users'
            activity.type_color = 'info'
        elif activity.activity_type == 'admin':
            activity.type_icon = 'cogs'
            activity.type_color = 'danger'
        else:
            activity.type_icon = 'bell'
            activity.type_color = 'secondary'

    # Get upcoming events
    upcoming_events = Event.query.filter(Event.start_date > datetime.utcnow()).order_by(Event.start_date).limit(6).all()

    # Add event type information for icons and colors
    for event in upcoming_events:
        if event.event_type == 'hackathon':
            event.event_type_icon = 'laptop-code'
            event.event_type_color = 'danger'
        elif event.event_type == 'pitching':
            event.event_type_icon = 'lightbulb'
            event.event_type_color = 'warning'
        elif event.event_type == 'workshop':
            event.event_type_icon = 'chalkboard-teacher'
            event.event_type_color = 'info'
        elif event.event_type == 'talk':
            event.event_type_icon = 'microphone-alt'
            event.event_type_color = 'success'
        elif event.event_type == 'competition':
            event.event_type_icon = 'trophy'
            event.event_type_color = 'primary'
        else:
            event.event_type_icon = 'calendar-alt'
            event.event_type_color = 'secondary'

    return render_template('staff/index.html',
                         active_events=active_events,
                         pending_registrations=pending_registrations,
                         total_participants=total_participants,
                         total_teams=total_teams,
                         recent_activities=recent_activities,
                         upcoming_events=upcoming_events)

@staff_bp.route('/events')
@login_required
@staff_required
def events():
    """Staff events page"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Get filtered events
    events_query = Event.query

    # Apply filters if provided
    event_type = request.args.get('event_type')
    status = request.args.get('status')
    search = request.args.get('search')

    if event_type:
        events_query = events_query.filter_by(event_type=event_type)

    if status:
        if status == 'upcoming':
            events_query = events_query.filter(Event.start_date > datetime.utcnow())
        elif status == 'ongoing':
            events_query = events_query.filter(
                (Event.start_date <= datetime.utcnow()) &
                (Event.end_date >= datetime.utcnow())
            )
        elif status == 'completed':
            events_query = events_query.filter(Event.end_date < datetime.utcnow())

    if search:
        events_query = events_query.filter(Event.name.ilike(f'%{search}%'))

    # Order by start date
    events_query = events_query.order_by(Event.start_date.desc())

    # Paginate results
    pagination = events_query.paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items

    # Add event type information for icons and colors
    for event in events:
        if event.event_type == 'hackathon':
            event.event_type_icon = 'laptop-code'
            event.event_type_color = 'danger'
        elif event.event_type == 'pitching':
            event.event_type_icon = 'lightbulb'
            event.event_type_color = 'warning'
        elif event.event_type == 'workshop':
            event.event_type_icon = 'chalkboard-teacher'
            event.event_type_color = 'info'
        elif event.event_type == 'talk':
            event.event_type_icon = 'microphone-alt'
            event.event_type_color = 'success'
        elif event.event_type == 'competition':
            event.event_type_icon = 'trophy'
            event.event_type_color = 'primary'
        else:
            event.event_type_icon = 'calendar-alt'
            event.event_type_color = 'secondary'

    return render_template('staff/events.html',
                         events=events,
                         pagination=pagination)

@staff_bp.route('/events/<int:event_id>')
@login_required
@staff_required
def event_details(event_id):
    """Staff event details page"""
    event = Event.query.get_or_404(event_id)

    # Get registrations
    registrations = EventRegistration.query.filter_by(event_id=event_id).all()
    confirmed_registrations = [r for r in registrations if r.status == 'confirmed']
    pending_registrations = [r for r in registrations if r.status == 'pending']
    cancelled_registrations = [r for r in registrations if r.status == 'cancelled']

    # Get recent registrations
    recent_registrations = EventRegistration.query.filter_by(event_id=event_id).order_by(EventRegistration.registration_date.desc()).limit(5).all()

    # Get teams
    teams = Team.query.filter_by(event_id=event_id).all()

    # Calculate average team size
    avg_team_size = 0
    if teams:
        total_members = 0
        for team in teams:
            total_members += len(team.members)
        avg_team_size = total_members / len(teams)

    # Add event type information for icons and colors
    if event.event_type == 'hackathon':
        event.event_type_icon = 'laptop-code'
        event.event_type_color = 'danger'
    elif event.event_type == 'pitching':
        event.event_type_icon = 'lightbulb'
        event.event_type_color = 'warning'
    elif event.event_type == 'workshop':
        event.event_type_icon = 'chalkboard-teacher'
        event.event_type_color = 'info'
    elif event.event_type == 'talk':
        event.event_type_icon = 'microphone-alt'
        event.event_type_color = 'success'
    elif event.event_type == 'competition':
        event.event_type_icon = 'trophy'
        event.event_type_color = 'primary'
    else:
        event.event_type_icon = 'calendar-alt'
        event.event_type_color = 'secondary'

    return render_template('staff/event_details.html',
                         event=event,
                         registrations=registrations,
                         confirmed_registrations=confirmed_registrations,
                         pending_registrations=pending_registrations,
                         cancelled_registrations=cancelled_registrations,
                         recent_registrations=recent_registrations,
                         teams=teams,
                         avg_team_size=avg_team_size)

@staff_bp.route('/events/<int:event_id>/registrations')
@login_required
@staff_required
def event_registrations(event_id):
    """Staff event registrations page"""
    event = Event.query.get_or_404(event_id)

    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get filtered registrations
    registrations_query = EventRegistration.query.filter_by(event_id=event_id)

    # Apply filters if provided
    status = request.args.get('status')
    search = request.args.get('search')
    date = request.args.get('date')

    if status:
        registrations_query = registrations_query.filter_by(status=status)

    if search:
        registrations_query = registrations_query.join(User).filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )

    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        next_day = date_obj + timedelta(days=1)
        registrations_query = registrations_query.filter(
            (EventRegistration.registration_date >= date_obj) &
            (EventRegistration.registration_date < next_day)
        )

    # Order by registration date
    registrations_query = registrations_query.order_by(EventRegistration.registration_date.desc())

    # Paginate results
    pagination = registrations_query.paginate(page=page, per_page=per_page, error_out=False)
    registrations = pagination.items

    # Get counts for different statuses
    confirmed_count = EventRegistration.query.filter_by(event_id=event_id, status='confirmed').count()
    pending_count = EventRegistration.query.filter_by(event_id=event_id, status='pending').count()
    rejected_count = EventRegistration.query.filter_by(event_id=event_id, status='rejected').count()

    return render_template('staff/event_registrations.html',
                         event=event,
                         registrations=registrations,
                         pagination=pagination,
                         confirmed_count=confirmed_count,
                         pending_count=pending_count,
                         rejected_count=rejected_count)

@staff_bp.route('/registrations')
@login_required
@staff_required
def registrations():
    """Staff all registrations page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get filtered registrations
    registrations_query = EventRegistration.query

    # Apply filters if provided
    event_id = request.args.get('event_id', type=int)
    status = request.args.get('status')
    search = request.args.get('search')

    if event_id:
        registrations_query = registrations_query.filter_by(event_id=event_id)

    if status:
        registrations_query = registrations_query.filter_by(status=status)

    if search:
        registrations_query = registrations_query.join(User).filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )

    # Order by registration date
    registrations_query = registrations_query.order_by(EventRegistration.registration_date.desc())

    # Paginate results
    pagination = registrations_query.paginate(page=page, per_page=per_page, error_out=False)
    registrations = pagination.items

    # Get all events for filter dropdown
    events = Event.query.order_by(Event.start_date.desc()).all()

    return render_template('staff/registrations.html',
                         registrations=registrations,
                         pagination=pagination,
                         events=events)

@staff_bp.route('/registrations/<int:registration_id>')
@login_required
@staff_required
def registration_details(registration_id):
    """Staff registration details page"""
    registration = EventRegistration.query.get_or_404(registration_id)

    return render_template('staff/registration_details.html',
                         registration=registration)

@staff_bp.route('/registrations/<int:registration_id>/approve', methods=['POST'])
@login_required
@staff_required
def approve_registration(registration_id):
    """Approve a registration"""
    registration = EventRegistration.query.get_or_404(registration_id)

    # Check if the event has reached capacity
    event = registration.event
    confirmed_count = EventRegistration.query.filter_by(event_id=event.id, status='confirmed').count()

    if confirmed_count >= event.capacity:
        flash('This event has reached its capacity. Cannot approve more registrations.', 'warning')
        return redirect(url_for('staff.registration_details', registration_id=registration_id))

    # Update registration status
    registration.status = 'confirmed'

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=registration.event_id,
        activity_type='registration',
        description=f'Approved registration for {registration.user.full_name}',
        status='success'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Registration for {registration.user.full_name} has been approved.', 'success')

    # Redirect back to the appropriate page
    if request.referrer and 'event_registrations' in request.referrer:
        return redirect(url_for('staff.event_registrations', event_id=registration.event_id))
    elif request.referrer and 'registrations' in request.referrer:
        return redirect(url_for('staff.registrations'))
    else:
        return redirect(url_for('staff.registration_details', registration_id=registration_id))

@staff_bp.route('/registrations/<int:registration_id>/reject', methods=['POST'])
@login_required
@staff_required
def reject_registration(registration_id):
    """Reject a registration"""
    registration = EventRegistration.query.get_or_404(registration_id)

    # Get rejection reason
    reason = request.form.get('reason', '')

    # Update registration status
    registration.status = 'rejected'
    registration.rejection_reason = reason

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=registration.event_id,
        activity_type='registration',
        description=f'Rejected registration for {registration.user.full_name}',
        status='warning'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Registration for {registration.user.full_name} has been rejected.', 'success')

    # Redirect back to the appropriate page
    if request.referrer and 'event_registrations' in request.referrer:
        return redirect(url_for('staff.event_registrations', event_id=registration.event_id))
    elif request.referrer and 'registrations' in request.referrer:
        return redirect(url_for('staff.registrations'))
    else:
        return redirect(url_for('staff.registration_details', registration_id=registration_id))

@staff_bp.route('/registrations/<int:registration_id>/notes', methods=['POST'])
@login_required
@staff_required
def update_registration_notes(registration_id):
    """Update registration notes"""
    registration = EventRegistration.query.get_or_404(registration_id)

    # Update notes
    registration.notes = request.form.get('notes', '')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=registration.event_id,
        activity_type='registration',
        description=f'Updated notes for {registration.user.full_name}\'s registration',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash('Registration notes have been updated.', 'success')
    return redirect(url_for('staff.registration_details', registration_id=registration_id))

@staff_bp.route('/events/<int:event_id>/check-in')
@login_required
@staff_required
def event_check_in(event_id):
    """Staff event check-in page"""
    event = Event.query.get_or_404(event_id)

    # Get confirmed registrations
    registrations = EventRegistration.query.filter_by(event_id=event_id, status='confirmed').all()

    return render_template('staff/event_check_in.html',
                         event=event,
                         registrations=registrations)

@staff_bp.route('/events/<int:event_id>/check-in/<int:registration_id>', methods=['POST'])
@login_required
@staff_required
def check_in_participant(event_id, registration_id):
    """Check in a participant"""
    registration = EventRegistration.query.get_or_404(registration_id)

    # Ensure the registration is for the correct event
    if registration.event_id != event_id:
        flash('Invalid registration for this event.', 'danger')
        return redirect(url_for('staff.event_check_in', event_id=event_id))

    # Update check-in status
    registration.checked_in = True
    registration.check_in_time = datetime.utcnow()

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='check_in',
        description=f'Checked in {registration.user.full_name}',
        status='success'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'{registration.user.full_name} has been checked in.', 'success')
    return redirect(url_for('staff.event_check_in', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/participants')
@login_required
@staff_required
def event_participants(event_id):
    """Staff event participants page"""
    event = Event.query.get_or_404(event_id)

    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get filtered registrations
    registrations_query = EventRegistration.query.filter_by(event_id=event_id)

    # Apply filters if provided
    status = request.args.get('status')
    search = request.args.get('search')
    checked_in = request.args.get('checked_in')

    if status:
        registrations_query = registrations_query.filter_by(status=status)
    else:
        # Default to confirmed registrations
        registrations_query = registrations_query.filter_by(status='confirmed')

    if search:
        registrations_query = registrations_query.join(User).filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )

    if checked_in == 'yes':
        registrations_query = registrations_query.filter_by(checked_in=True)
    elif checked_in == 'no':
        registrations_query = registrations_query.filter_by(checked_in=False)

    # Order by registration date
    registrations_query = registrations_query.order_by(EventRegistration.registration_date.desc())

    # Paginate results
    pagination = registrations_query.paginate(page=page, per_page=per_page, error_out=False)
    registrations = pagination.items

    return render_template('staff/event_participants.html',
                         event=event,
                         registrations=registrations,
                         pagination=pagination)

@staff_bp.route('/events/<int:event_id>/teams')
@login_required
@staff_required
def event_teams(event_id):
    """Staff event teams page"""
    event = Event.query.get_or_404(event_id)

    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get filtered teams
    teams_query = Team.query.filter_by(event_id=event_id)

    # Apply filters if provided
    search = request.args.get('search')
    sort = request.args.get('sort', 'created_desc')

    if search:
        teams_query = teams_query.filter(Team.name.ilike(f'%{search}%'))

    # Apply sorting
    if sort == 'created_desc':
        teams_query = teams_query.order_by(Team.created_at.desc())
    elif sort == 'created_asc':
        teams_query = teams_query.order_by(Team.created_at.asc())
    elif sort == 'name_asc':
        teams_query = teams_query.order_by(Team.name.asc())
    elif sort == 'name_desc':
        teams_query = teams_query.order_by(Team.name.desc())
    # Note: sorting by members count would require additional logic

    # Paginate results
    pagination = teams_query.paginate(page=page, per_page=per_page, error_out=False)
    teams = pagination.items

    return render_template('staff/event_teams.html',
                         event=event,
                         teams=teams,
                         pagination=pagination)

@staff_bp.route('/teams')
@login_required
@staff_required
def teams():
    """Staff all teams page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get filtered teams
    teams_query = Team.query

    # Apply filters if provided
    event_id = request.args.get('event_id', type=int)
    event_type = request.args.get('event_type')
    search = request.args.get('search')

    if event_id:
        teams_query = teams_query.filter_by(event_id=event_id)

    if event_type:
        teams_query = teams_query.join(Event).filter(Event.event_type == event_type)

    if search:
        teams_query = teams_query.filter(Team.name.ilike(f'%{search}%'))

    # Order by creation date
    teams_query = teams_query.order_by(Team.created_at.desc())

    # Paginate results
    pagination = teams_query.paginate(page=page, per_page=per_page, error_out=False)
    teams = pagination.items

    # Get all events for filter dropdown
    events = Event.query.filter(Event.is_team_event == True).order_by(Event.start_date.desc()).all()

    return render_template('staff/teams.html',
                         teams=teams,
                         pagination=pagination,
                         events=events)

@staff_bp.route('/teams/<int:team_id>')
@login_required
@staff_required
def team_details(team_id):
    """Staff team details page"""
    team = Team.query.get_or_404(team_id)

    # Get team activities
    team_activities = ActivityLog.query.filter(
        (ActivityLog.activity_type == 'team') &
        ((ActivityLog.description.like(f'%team {team.name}%')) |
         (ActivityLog.description.like(f'%{team.name} team%')))
    ).order_by(ActivityLog.timestamp.desc()).limit(10).all()

    # Add activity type information for icons and colors
    for activity in team_activities:
        if activity.activity_type == 'registration':
            activity.type_icon = 'clipboard-list'
            activity.type_color = 'primary'
        elif activity.activity_type == 'check_in':
            activity.type_icon = 'clipboard-check'
            activity.type_color = 'success'
        elif activity.activity_type == 'team':
            activity.type_icon = 'users'
            activity.type_color = 'info'
        elif activity.activity_type == 'admin':
            activity.type_icon = 'cogs'
            activity.type_color = 'danger'
        else:
            activity.type_icon = 'bell'
            activity.type_color = 'secondary'

    return render_template('staff/team_details.html',
                         team=team,
                         team_activities=team_activities)

@staff_bp.route('/participants')
@login_required
@staff_required
def participants():
    """Staff all participants page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get filtered users
    users_query = User.query

    # Apply filters if provided
    search = request.args.get('search')
    event_id = request.args.get('event_id', type=int)
    status = request.args.get('status')

    if search:
        users_query = users_query.filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.username.ilike(f'%{search}%'))
        )

    if event_id:
        # Filter users who are registered for the specified event
        users_query = users_query.join(EventRegistration, User.id == EventRegistration.user_id)\
                              .filter(EventRegistration.event_id == event_id)

        if status:
            users_query = users_query.filter(EventRegistration.status == status)

    # Order by registration date
    users_query = users_query.order_by(User.created_at.desc())

    # Paginate results
    pagination = users_query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items

    # Get all events for filter dropdown
    events = Event.query.order_by(Event.start_date.desc()).all()

    return render_template('staff/participants.html',
                         users=users,
                         pagination=pagination,
                         events=events)

@staff_bp.route('/participants/<int:user_id>')
@login_required
@staff_required
def participant_details(user_id):
    """Staff participant details page"""
    user = User.query.get_or_404(user_id)

    # Get user activities
    user_activities = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).limit(10).all()

    # Add activity type information for icons and colors
    for activity in user_activities:
        if activity.activity_type == 'registration':
            activity.type_icon = 'clipboard-list'
            activity.type_color = 'primary'
        elif activity.activity_type == 'check_in':
            activity.type_icon = 'clipboard-check'
            activity.type_color = 'success'
        elif activity.activity_type == 'team':
            activity.type_icon = 'users'
            activity.type_color = 'info'
        elif activity.activity_type == 'admin':
            activity.type_icon = 'cogs'
            activity.type_color = 'danger'
        else:
            activity.type_icon = 'bell'
            activity.type_color = 'secondary'

    return render_template('staff/participant_details.html',
                         user=user,
                         user_activities=user_activities)

@staff_bp.route('/participants/<int:user_id>/registrations')
@login_required
@staff_required
def participant_registrations(user_id):
    """Staff participant registrations page"""
    user = User.query.get_or_404(user_id)

    return render_template('staff/participant_registrations.html',
                         user=user)

@staff_bp.route('/participants/<int:user_id>/teams')
@login_required
@staff_required
def participant_teams(user_id):
    """Staff participant teams page"""
    user = User.query.get_or_404(user_id)

    return render_template('staff/participant_teams.html',
                         user=user)

@staff_bp.route('/reports')
@login_required
@staff_required
def reports():
    """Staff reports page"""
    # Get all events
    events = Event.query.order_by(Event.start_date.desc()).all()

    return render_template('staff/reports.html',
                         events=events)

@staff_bp.route('/events/<int:event_id>/reports')
@login_required
@staff_required
def event_reports(event_id):
    """Staff event reports page"""
    event = Event.query.get_or_404(event_id)

    # Get registrations
    registrations = EventRegistration.query.filter_by(event_id=event_id).all()
    confirmed_registrations = [r for r in registrations if r.status == 'confirmed']
    pending_registrations = [r for r in registrations if r.status == 'pending']

    # Get check-in counts
    checked_in_count = EventRegistration.query.filter_by(event_id=event_id, status='confirmed', checked_in=True).count()
    not_checked_in_count = len(confirmed_registrations) - checked_in_count

    # Get teams if it's a team event
    teams = []
    avg_team_size = 0
    if event.is_team_event:
        teams = Team.query.filter_by(event_id=event_id).all()
        if teams:
            total_members = 0
            for team in teams:
                total_members += len(team.members)
            avg_team_size = total_members / len(teams)

    # Get recent reports (this would be implemented with a Report model)
    recent_reports = []  # Placeholder for actual reports

    return render_template('staff/event_reports.html',
                         event=event,
                         confirmed_count=len(confirmed_registrations),
                         pending_count=len(pending_registrations),
                         checked_in_count=checked_in_count,
                         not_checked_in_count=not_checked_in_count,
                         teams=teams,
                         avg_team_size=avg_team_size,
                         recent_reports=recent_reports)

@staff_bp.route('/events/<int:event_id>/notes', methods=['POST'])
@login_required
@staff_required
def update_event_notes(event_id):
    """Update event staff notes"""
    event = Event.query.get_or_404(event_id)

    # Update notes
    event.staff_notes = request.form.get('notes', '')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Updated staff notes for {event.name}',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash('Event notes have been updated.', 'success')
    return redirect(url_for('staff.event_details', event_id=event_id))

@staff_bp.route('/export/events', methods=['POST'])
@login_required
@staff_required
def export_events():
    """Export events data"""
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        activity_type='admin',
        description=f'Exported events data in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Events data export in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.events'))

@staff_bp.route('/export/registrations', methods=['POST'])
@login_required
@staff_required
def export_registrations():
    """Export registrations data"""
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        activity_type='admin',
        description=f'Exported registrations data in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Registrations data export in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.registrations'))

@staff_bp.route('/export/participants', methods=['POST'])
@login_required
@staff_required
def export_participants():
    """Export participants data"""
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        activity_type='admin',
        description=f'Exported participants data in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Participants data export in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.participants'))

@staff_bp.route('/export/teams', methods=['POST'])
@login_required
@staff_required
def export_teams():
    """Export teams data"""
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        activity_type='admin',
        description=f'Exported teams data in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Teams data export in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.teams'))

@staff_bp.route('/events/<int:event_id>/export/registrations', methods=['POST'])
@login_required
@staff_required
def export_event_registrations(event_id):
    """Export event registrations data"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Exported registrations data for {event.name} in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Registrations data export for {event.name} in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.event_registrations', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/export/participants', methods=['POST'])
@login_required
@staff_required
def export_event_participants(event_id):
    """Export event participants data"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Exported participants data for {event.name} in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Participants data export for {event.name} in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.event_participants', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/export/teams', methods=['POST'])
@login_required
@staff_required
def export_event_teams(event_id):
    """Export event teams data"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Exported teams data for {event.name} in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Teams data export for {event.name} in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.event_teams', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/export/checkin', methods=['POST'])
@login_required
@staff_required
def export_checkin(event_id):
    """Export check-in data"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Exported check-in data for {event.name} in {format} format',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Check-in data export for {event.name} in {format} format has been started. You will receive an email when it\'s ready.', 'info')
    return redirect(url_for('staff.event_check_in', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/generate/registration-report', methods=['POST'])
@login_required
@staff_required
def generate_event_registration_report(event_id):
    """Generate event registration report"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')
    report_name = request.form.get('report_name', f'{event.name} - Registration Report')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Generated registration report for {event.name}',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Registration report for {event.name} has been generated.', 'success')
    return redirect(url_for('staff.event_reports', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/generate/attendance-report', methods=['POST'])
@login_required
@staff_required
def generate_event_attendance_report(event_id):
    """Generate event attendance report"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')
    report_name = request.form.get('report_name', f'{event.name} - Attendance Report')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Generated attendance report for {event.name}',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Attendance report for {event.name} has been generated.', 'success')
    return redirect(url_for('staff.event_reports', event_id=event_id))

@staff_bp.route('/events/<int:event_id>/generate/team-report', methods=['POST'])
@login_required
@staff_required
def generate_event_team_report(event_id):
    """Generate event team report"""
    event = Event.query.get_or_404(event_id)
    format = request.form.get('format', 'csv')
    report_name = request.form.get('report_name', f'{event.name} - Team Report')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=event_id,
        activity_type='admin',
        description=f'Generated team report for {event.name}',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash(f'Team report for {event.name} has been generated.', 'success')
    return redirect(url_for('staff.event_reports', event_id=event_id))

@staff_bp.route('/activity-log')
@login_required
@staff_required
def activity_log():
    """Staff activity log page"""
    page = request.args.get('page', 1, type=int)
    per_page = 50

    # Get filtered activities
    activities_query = ActivityLog.query

    # Apply filters if provided
    activity_type = request.args.get('activity_type')
    event_id = request.args.get('event_id', type=int)
    user_id = request.args.get('user_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if activity_type:
        activities_query = activities_query.filter_by(activity_type=activity_type)

    if event_id:
        activities_query = activities_query.filter_by(event_id=event_id)

    if user_id:
        activities_query = activities_query.filter_by(user_id=user_id)

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        activities_query = activities_query.filter(ActivityLog.timestamp >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date + timedelta(days=1)  # Include the entire end date
        activities_query = activities_query.filter(ActivityLog.timestamp <= end_date)

    # Order by timestamp
    activities_query = activities_query.order_by(ActivityLog.timestamp.desc())

    # Paginate results
    pagination = activities_query.paginate(page=page, per_page=per_page, error_out=False)
    activities = pagination.items

    # Add activity type information for icons and colors
    for activity in activities:
        if activity.activity_type == 'registration':
            activity.type_icon = 'clipboard-list'
            activity.type_color = 'primary'
        elif activity.activity_type == 'check_in':
            activity.type_icon = 'clipboard-check'
            activity.type_color = 'success'
        elif activity.activity_type == 'team':
            activity.type_icon = 'users'
            activity.type_color = 'info'
        elif activity.activity_type == 'admin':
            activity.type_icon = 'cogs'
            activity.type_color = 'danger'
        else:
            activity.type_icon = 'bell'
            activity.type_color = 'secondary'

    # Get all events for filter dropdown
    events = Event.query.order_by(Event.start_date.desc()).all()

    # Get all staff users for filter dropdown
    staff_users = User.query.filter_by(is_staff=True).all()

    return render_template('staff/activity_log.html',
                         activities=activities,
                         pagination=pagination,
                         events=events,
                         staff_users=staff_users)

@staff_bp.route('/participants/<int:user_id>/notes', methods=['POST'])
@login_required
@staff_required
def update_participant_notes(user_id):
    """Update participant notes"""
    user = User.query.get_or_404(user_id)

    # Update notes
    user.staff_notes = request.form.get('notes', '')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        activity_type='admin',
        description=f'Updated notes for participant {user.full_name}',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash('Participant notes have been updated.', 'success')
    return redirect(url_for('staff.participant_details', user_id=user_id))

@staff_bp.route('/teams/<int:team_id>/notes', methods=['POST'])
@login_required
@staff_required
def update_team_notes(team_id):
    """Update team notes"""
    team = Team.query.get_or_404(team_id)

    # Update notes
    team.staff_notes = request.form.get('notes', '')

    # Log the activity
    activity = ActivityLog(
        user_id=current_user.id,
        event_id=team.event_id,
        activity_type='team',
        description=f'Updated notes for team {team.name}',
        status='info'
    )

    db.session.add(activity)
    db.session.commit()

    flash('Team notes have been updated.', 'success')
    return redirect(url_for('staff.team_details', team_id=team_id))

@staff_bp.route('/profile')
@login_required
@staff_required
def profile():
    """Staff profile page"""
    return render_template('staff/profile.html')

@staff_bp.route('/settings')
@login_required
@staff_required
def settings():
    """Staff settings page"""
    return render_template('staff/settings.html')

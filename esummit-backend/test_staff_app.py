from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, login_user, current_user
from app.models.user import User
from app import db
import os

app = Flask(__name__, template_folder='app/templates')
app.config['SECRET_KEY'] = 'test-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('main/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('staff_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html')

@app.route('/staff-dashboard')
@login_required
def staff_dashboard():
    if not current_user.is_staff:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    # Create dummy data for the template
    active_events = []
    pending_registrations = []
    total_participants = 0
    total_teams = 0
    recent_activities = []
    upcoming_events = []
    
    return render_template('staff/index.html',
                         active_events=active_events,
                         pending_registrations=pending_registrations,
                         total_participants=total_participants,
                         total_teams=total_teams,
                         recent_activities=recent_activities,
                         upcoming_events=upcoming_events)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

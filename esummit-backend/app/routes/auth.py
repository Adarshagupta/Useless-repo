from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt, mail
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app import with_db_retry
import os
import logging
import time

auth_bp = Blueprint('auth', __name__)

# Master OTP for testing purposes
MASTER_OTP = "425387"

# Initialize serializer for token generation
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

def send_reset_email(user):
    token = serializer.dumps(user.email, salt='password-reset-salt')
    msg = Message('Password Reset Request',
                  sender='noreply@esummit.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    try:
        if current_user.is_authenticated:
            # Redirect to admin dashboard if user is admin, otherwise to user dashboard
            return redirect(url_for('admin.index') if current_user.is_admin else url_for('dashboard.index'))
        
        form = LoginForm()
        if form.validate_on_submit():
            try:
                # Check if master OTP is being used
                if form.password.data == MASTER_OTP:
                    # Use a decorator for retry logic
                    @with_db_retry
                    def get_user_by_email():
                        return User.query.filter_by(email=form.email.data).first()
                    
                    user = get_user_by_email()
                    if user:
                        login_user(user, remember=form.remember.data)
                        next_page = request.args.get('next')
                        if next_page:
                            return redirect(next_page)
                        return redirect(url_for('admin.index') if user.is_admin else url_for('dashboard.index'))
                    else:
                        flash('Email not found. Please register first.', 'danger')
                else:
                    # Normal login process
                    @with_db_retry
                    def get_user_and_check():
                        user = User.query.filter_by(email=form.email.data).first()
                        if user and user.check_password(form.password.data):
                            return user
                        return None
                    
                    user = get_user_and_check()
                    if user:
                        login_user(user, remember=form.remember.data)
                        next_page = request.args.get('next')
                        if next_page:
                            return redirect(next_page)
                        return redirect(url_for('admin.index') if user.is_admin else url_for('dashboard.index'))
                    else:
                        flash('Login unsuccessful. Please check email and password.', 'danger')
            except Exception as e:
                current_app.logger.error(f"Error during login process: {str(e)}")
                flash('An error occurred during login. Please try again.', 'danger')
                return render_template('auth/login.html', title='Login', form=form)
        
        return render_template('auth/login.html', title='Login', form=form)
    
    except Exception as e:
        current_app.logger.error(f"Unhandled error in login route: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if master OTP is being used
            if form.password.data == MASTER_OTP:
                # Skip password hashing for master OTP
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=MASTER_OTP,  # This will be hashed in the User model
                    full_name=form.full_name.data,
                    phone=form.phone.data,
                    college=form.college.data
                )
                
                @with_db_retry
                def add_master_user():
                    db.session.add(user)
                    db.session.commit()
                
                add_master_user()
                flash('Account created with master OTP! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                # Normal registration process
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    full_name=form.full_name.data,
                    phone=form.phone.data,
                    college=form.college.data
                )
                
                @with_db_retry
                def add_user():
                    db.session.add(user)
                    db.session.commit()
                
                add_user()
                flash('Your account has been created! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        try:
            @with_db_retry
            def get_user_by_email():
                return User.query.filter_by(email=form.email.data).first()
            
            user = get_user_by_email()
            if user:
                send_reset_email(user)
            # Always show success message even if email doesn't exist (security)
            flash('If your email exists in our system, a password reset link has been sent.', 'info')
            return redirect(url_for('auth.login'))
        except Exception as e:
            current_app.logger.error(f"Error during password reset request: {str(e)}")
            flash('An error occurred. Please try again later.', 'danger')
    
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token valid for 1 hour
    except:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    
    try:
        @with_db_retry
        def get_user_by_email():
            return User.query.filter_by(email=email).first()
        
        user = get_user_by_email()
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('auth.reset_request'))
        
        form = ResetPasswordForm()
        if form.validate_on_submit():
            @with_db_retry
            def update_password():
                user.password = form.password.data
                db.session.commit()
            
            update_password()
            flash('Your password has been updated! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('auth/reset_password.html', title='Reset Password', form=form)
    except Exception as e:
        current_app.logger.error(f"Error during password reset: {str(e)}")
        flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('auth.reset_request'))

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for('main.index'))

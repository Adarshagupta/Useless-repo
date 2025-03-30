from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt, mail
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, OTPVerificationForm
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app import with_db_retry
import os
import logging
import time
import random
import string
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# Master OTP for testing purposes
MASTER_OTP = "425387"

# Initialize serializer for token generation
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user, otp, action="verification"):
    """Send OTP email to user"""
    # For development mode - just log the OTP without sending emails
    current_app.logger.info(f"[DEV MODE] OTP for {user.email}: {otp} (for {action})")
    
    # Skip actual email sending in development mode
    try:
        # Check if we're in development mode - no need to actually send emails
        if os.environ.get('FLASK_ENV') == 'development':
            flash(f'Development mode: Your OTP is {otp}', 'info')
            return
            
        subject = f"Your OTP for {action} - ESummit"
        msg = Message(subject, sender=('ESummit', 'noreply@esummit.com'), recipients=[user.email])
        msg.body = f"""Hello {user.full_name},

Your One-Time Password (OTP) for {action} is: {otp}

This OTP is valid for 10 minutes.

If you did not request this OTP, please ignore this email.

Regards,
ESummit Team
"""
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        # Just log the error but don't raise it - we'll use master OTP in dev

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
                        # Generate and send OTP
                        otp = generate_otp()
                        user.otp_secret = otp
                        user.otp_created_at = datetime.utcnow()
                        user.otp_verified = False
                        db.session.commit()
                        
                        # Save user ID in session for OTP verification
                        session['user_id_for_otp'] = user.id
                        session['remember_me'] = form.remember.data
                        session['next_page'] = request.args.get('next')
                        
                        # Send OTP email - in development, this just logs the OTP
                        try:
                            send_otp_email(user, otp, "login")
                            flash(f'For development, you can use the master OTP: {MASTER_OTP}', 'info')
                        except Exception as e:
                            current_app.logger.error(f"Error during OTP handling: {str(e)}")
                            flash(f'For development, use the master OTP: {MASTER_OTP}', 'info')
                        
                        return redirect(url_for('auth.verify_otp', action='login'))
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
                    college=form.college.data,
                    is_email_verified=True  # Auto-verify for master OTP
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
                
                # Generate and store OTP
                otp = generate_otp()
                user.otp_secret = otp
                user.otp_created_at = datetime.utcnow()
                
                @with_db_retry
                def add_user():
                    db.session.add(user)
                    db.session.commit()
                
                add_user()
                
                # Save user ID in session for OTP verification
                session['user_id_for_otp'] = user.id
                
                # Send OTP email - in development, this just logs the OTP
                try:
                    send_otp_email(user, otp, "registration")
                    flash(f'Account created! Please verify with the OTP. In development, you can also use the master OTP: {MASTER_OTP}', 'success')
                except Exception as e:
                    current_app.logger.error(f"Error during OTP handling: {str(e)}")
                    flash(f'Account created! For development, use the master OTP: {MASTER_OTP}', 'warning')
                
                return redirect(url_for('auth.verify_otp', action='registration'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/verify-otp/<action>', methods=['GET', 'POST'])
def verify_otp(action):
    """OTP verification route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    # Check if we have a user ID in session
    user_id = session.get('user_id_for_otp')
    if not user_id:
        flash('No verification in progress. Please login or register again.', 'warning')
        return redirect(url_for('auth.login'))
    
    form = OTPVerificationForm()
    
    if form.validate_on_submit():
        user = User.query.get(user_id)
        if not user:
            flash('User not found. Please try again.', 'danger')
            return redirect(url_for('auth.login'))
        
        entered_otp = form.otp.data
        
        # Check if it's the master OTP
        if entered_otp == MASTER_OTP:
            if action == 'registration':
                user.is_email_verified = True
                user.otp_verified = True
                db.session.commit()
                flash('Email verified successfully with master OTP!', 'success')
            elif action == 'login':
                remember_me = session.get('remember_me', False)
                login_user(user, remember=remember_me)
                
                # Clear session data
                session.pop('user_id_for_otp', None)
                session.pop('remember_me', None)
                
                next_page = session.pop('next_page', None)
                if next_page:
                    return redirect(next_page)
                
                return redirect(url_for('admin.index') if user.is_admin else url_for('dashboard.index'))
        
        # Check if OTP is valid and not expired (10 minutes)
        elif user.otp_secret == entered_otp and user.otp_created_at:
            otp_expiry = user.otp_created_at + timedelta(minutes=10)
            
            if datetime.utcnow() <= otp_expiry:
                if action == 'registration':
                    user.is_email_verified = True
                    user.otp_verified = True
                    db.session.commit()
                    flash('Email verified successfully!', 'success')
                    return redirect(url_for('auth.login'))
                elif action == 'login':
                    user.otp_verified = True
                    db.session.commit()
                    
                    # Login the user
                    remember_me = session.get('remember_me', False)
                    login_user(user, remember=remember_me)
                    
                    # Clear session data
                    session.pop('user_id_for_otp', None)
                    session.pop('remember_me', None)
                    
                    next_page = session.pop('next_page', None)
                    if next_page:
                        return redirect(next_page)
                    
                    return redirect(url_for('admin.index') if user.is_admin else url_for('dashboard.index'))
            else:
                flash('OTP has expired. Please request a new one.', 'danger')
                # Generate and send new OTP
                new_otp = generate_otp()
                user.otp_secret = new_otp
                user.otp_created_at = datetime.utcnow()
                db.session.commit()
                
                try:
                    send_otp_email(user, new_otp, action)
                    flash('A new OTP has been sent to your email.', 'info')
                except Exception as e:
                    current_app.logger.error(f"Error sending OTP email: {str(e)}")
                    flash('Failed to send new OTP. Please try again.', 'danger')
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    
    return render_template('auth/verify_otp.html', title='Verify OTP', form=form, action=action)

@auth_bp.route('/resend-otp/<action>', methods=['POST'])
def resend_otp(action):
    """Resend OTP"""
    user_id = session.get('user_id_for_otp')
    if not user_id:
        flash('No verification in progress. Please login or register again.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Generate new OTP
    new_otp = generate_otp()
    user.otp_secret = new_otp
    user.otp_created_at = datetime.utcnow()
    db.session.commit()
    
    try:
        send_otp_email(user, new_otp, action)
        flash('A new OTP has been sent to your email.', 'success')
    except Exception as e:
        current_app.logger.error(f"Error sending OTP email: {str(e)}")
        flash('Failed to send new OTP. Please try again.', 'danger')
    
    return redirect(url_for('auth.verify_otp', action=action))

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
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

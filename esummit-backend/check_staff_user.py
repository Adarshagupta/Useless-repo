from app import create_app, db
from app.models.user import User

def check_staff_user():
    """Check if the staff user is correctly set up"""
    app = create_app()
    with app.app_context():
        # Check if staff user exists
        staff_user = User.query.filter_by(email='staff@esummit.com').first()
        
        if staff_user:
            print(f"Staff user found: {staff_user.username} ({staff_user.email})")
            print(f"Is staff: {staff_user.is_staff}")
            print(f"Is admin: {staff_user.is_admin}")
            print(f"Password hash: {staff_user.password_hash[:20]}...")
            
            # Check if password is correct
            if staff_user.check_password('staffpassword'):
                print("Password is correct!")
            else:
                print("Password is incorrect!")
        else:
            print("Staff user not found!")

if __name__ == "__main__":
    check_staff_user()

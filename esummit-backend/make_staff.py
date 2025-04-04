from app import create_app, db
from app.models.user import User
import sys

def make_user_staff(email):
    """Make a user a staff member by email"""
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"No user found with email: {email}")
            return False
        
        user.is_staff = True
        db.session.commit()
        
        print(f"User {user.username} ({user.email}) is now a staff member!")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_staff.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    make_user_staff(email)

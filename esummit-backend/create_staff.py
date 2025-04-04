from app import create_app, db
from app.models.user import User

def create_staff_user(username, email, password, full_name):
    """Create a new staff user"""
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print(f"User with username '{username}' or email '{email}' already exists.")
            return False

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=password,  # The model will hash this
            full_name=full_name,
            is_admin=False
        )

        # Set staff flag and email verification
        new_user.is_staff = True
        new_user.is_email_verified = True  # Skip email verification for staff

        db.session.add(new_user)
        db.session.commit()

        print(f"Staff user '{username}' created successfully!")
        return True

if __name__ == "__main__":
    # Create a staff user
    create_staff_user(
        username="staff",
        email="staff@esummit.com",
        password="staffpassword",
        full_name="Staff User"
    )

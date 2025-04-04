from app import create_app, db
from app.models.user import User

def list_users():
    """List all users in the database"""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No users found in the database.")
            return
        
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"- {user.username} ({user.email}): Admin={user.is_admin}, Staff={user.is_staff}")

if __name__ == "__main__":
    list_users()

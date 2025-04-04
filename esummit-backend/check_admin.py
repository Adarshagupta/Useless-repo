from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    admin_user = User.query.filter_by(is_admin=True).first()
    print(f"Admin user: {admin_user}")
    
    # List all users
    print("\nAll users:")
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Admin: {user.is_admin}")

from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Create admin user if it doesn't exist
    try:
        admin = User.query.filter_by(email='admin@esummit.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@esummit.com',
                password='admin123',  # Change this in production!
                full_name='Admin User',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully!')
        else:
            print('Admin user already exists!')
    except Exception as e:
        db.session.rollback()
        print(f'Error: {str(e)}') 
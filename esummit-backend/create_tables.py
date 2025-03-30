from app import create_app, db
from app.models.user import User
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Close any existing transactions
    db.session.remove()
    
    # Create all tables
    try:
        # Create tables
        with db.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "user" (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(20) NOT NULL UNIQUE,
                    email VARCHAR(120) NOT NULL UNIQUE,
                    password_hash VARCHAR(128) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(15),
                    college VARCHAR(100),
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS event (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP NOT NULL,
                    venue VARCHAR(100) NOT NULL,
                    registration_deadline TIMESTAMP NOT NULL,
                    capacity INTEGER,
                    event_type VARCHAR(20) NOT NULL,
                    is_team_event BOOLEAN DEFAULT FALSE,
                    min_team_size INTEGER,
                    max_team_size INTEGER,
                    image_url VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS team (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    leader_id INTEGER NOT NULL REFERENCES "user"(id),
                    event_id INTEGER NOT NULL REFERENCES event(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS event_registration (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES "user"(id),
                    event_id INTEGER NOT NULL REFERENCES event(id),
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20),
                    payment_status VARCHAR(20),
                    payment_id VARCHAR(100),
                    team_id INTEGER REFERENCES team(id)
                );
                
                CREATE TABLE IF NOT EXISTS team_member (
                    id SERIAL PRIMARY KEY,
                    team_id INTEGER NOT NULL REFERENCES team(id),
                    user_id INTEGER NOT NULL REFERENCES "user"(id),
                    role VARCHAR(50),
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS hackathon_registration (
                    id SERIAL PRIMARY KEY,
                    team_id INTEGER NOT NULL REFERENCES team(id),
                    event_id INTEGER NOT NULL REFERENCES event(id),
                    project_name VARCHAR(100) NOT NULL,
                    project_description TEXT NOT NULL,
                    tech_stack VARCHAR(255) NOT NULL,
                    github_url VARCHAR(255),
                    other_links TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20)
                );
            """))
            conn.commit()
        print("Created all tables.")
        
        # Create admin user if it doesn't exist
        with db.engine.connect() as conn:
            result = conn.execute(text('SELECT id FROM "user" WHERE email = :email'), {'email': 'admin@esummit.com'})
            admin = result.fetchone()
            
            if not admin:
                # Create admin user
                conn.execute(text("""
                    INSERT INTO "user" (username, email, password_hash, full_name, is_admin)
                    VALUES (:username, :email, :password_hash, :full_name, :is_admin)
                """), {
                    'username': 'admin',
                    'email': 'admin@esummit.com',
                    'password_hash': User('admin', 'admin@esummit.com', 'admin123', 'Admin User').password_hash,
                    'full_name': 'Admin User',
                    'is_admin': True
                })
                conn.commit()
                print('Admin user created successfully!')
            else:
                print('Admin user already exists!')
    except Exception as e:
        print(f'Error: {str(e)}') 
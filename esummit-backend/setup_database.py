from app import create_app, db
from app.models.user import User
from sqlalchemy import text
import psycopg2
import os
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_update_schema():
    """Check if the schema is up-to-date and update it if needed"""
    # Path to SQLite database
    db_path = Path('instance/app.db')
    
    if not db_path.exists():
        print("Database file not found, it will be created during initialization")
        return
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check for missing columns and add them
        cursor.execute("PRAGMA table_info(event)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # Add prize_pool column if missing
        if 'prize_pool' not in column_names:
            print("Adding prize_pool column to event table...")
            cursor.execute("ALTER TABLE event ADD COLUMN prize_pool INTEGER")
            conn.commit()
            print("Column added successfully!")
        
        conn.close()
    except Exception as e:
        print(f"Error checking/updating schema: {e}")

def create_tables_directly():
    app = create_app()
    with app.app_context():
        try:
            # Check if we should use SQLite
            use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true'
            
            if use_sqlite:
                print("Setting up SQLite database...")
                # Check and update schema before initialization
                check_and_update_schema()
                
                # Make sure the instance directory exists
                instance_path = Path('instance')
                instance_path.mkdir(exist_ok=True)
                
                # Initialize database tables with SQLAlchemy
                db.create_all()
                
                # Check if admin user exists
                admin = User.query.filter_by(email='admin@esummit.com').first()
                if not admin:
                    print("Creating admin user...")
                    admin = User(
                        username='admin',
                        email='admin@esummit.com',
                        password='admin123',
                        full_name='Admin User',
                        is_admin=True
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print("Admin user created!")
                else:
                    print("Admin user already exists.")
                
                print("\nSQLite database setup completed successfully!")
                return
            
            # Get database URL from environment for PostgreSQL
            db_url = os.environ.get('DATABASE_URL')
            
            # Parse connection string
            conn_parts = db_url.split('://')[1].split('@')
            user_pass = conn_parts[0].split(':')
            host_db = conn_parts[1].split('/')
            
            username = user_pass[0]
            password = user_pass[1]
            host = host_db[0].split('?')[0]
            dbname = host_db[1].split('?')[0]
            
            # Connect directly with psycopg2
            conn = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=username,
                password=password,
                sslmode='require'
            )
            conn.autocommit = True
            
            with conn.cursor() as cursor:
                # Step 1: Check which tables exist
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                existing_tables = [table[0] for table in cursor.fetchall()]
                print(f"Existing tables: {existing_tables}")
                
                # Step 2: Create tables if they don't exist
                if 'user' not in existing_tables:
                    print("Creating user table...")
                    cursor.execute("""
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
                        )
                    """)
                
                if 'event' not in existing_tables:
                    print("Creating event table...")
                    cursor.execute("""
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
                        )
                    """)
                
                if 'team' not in existing_tables:
                    print("Creating team table...")
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS team (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            leader_id INTEGER NOT NULL REFERENCES "user"(id),
                            event_id INTEGER NOT NULL REFERENCES event(id),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                
                if 'event_registration' not in existing_tables:
                    print("Creating event_registration table...")
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS event_registration (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL REFERENCES "user"(id),
                            event_id INTEGER NOT NULL REFERENCES event(id),
                            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            status VARCHAR(20),
                            payment_status VARCHAR(20),
                            payment_id VARCHAR(100),
                            team_id INTEGER REFERENCES team(id)
                        )
                    """)
                
                if 'team_member' not in existing_tables:
                    print("Creating team_member table...")
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS team_member (
                            id SERIAL PRIMARY KEY,
                            team_id INTEGER NOT NULL REFERENCES team(id),
                            user_id INTEGER NOT NULL REFERENCES "user"(id),
                            role VARCHAR(50),
                            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                
                if 'hackathon_registration' not in existing_tables:
                    print("Creating hackathon_registration table...")
                    cursor.execute("""
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
                        )
                    """)
                
                # Step 3: Create alembic_version table and mark migration as completed
                print("Marking migration as completed...")
                cursor.execute("CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL, PRIMARY KEY (version_num))")
                cursor.execute("DELETE FROM alembic_version")
                cursor.execute("INSERT INTO alembic_version (version_num) VALUES ('1e171ece3db3')")
                
                # Step 4: Create admin user if it doesn't exist
                print("Checking for admin user...")
                cursor.execute('SELECT id FROM "user" WHERE email = %s', ('admin@esummit.com',))
                admin = cursor.fetchone()
                if not admin:
                    print("Creating admin user...")
                    # Create a User instance to get the password hash
                    user = User(
                        username='admin',
                        email='admin@esummit.com',
                        password='admin123',
                        full_name='Admin User',
                        is_admin=True
                    )
                    cursor.execute("""
                        INSERT INTO "user" (username, email, password_hash, full_name, is_admin)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        'admin',
                        'admin@esummit.com',
                        user.password_hash,
                        'Admin User',
                        True
                    ))
                    print("Admin user created!")
                else:
                    print("Admin user already exists.")
                
                # Step 5: Verify all tables have been created
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                tables = cursor.fetchall()
                print("\nVerifying all tables:")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM \"{table[0]}\"")
                    count = cursor.fetchone()[0]
                    print(f"  - {table[0]}: {count} rows")
                
                print("\nDatabase setup completed successfully!")
                
        except Exception as e:
            print(f"Error during database setup: {e}")
            raise

def setup_sqlite_database():
    """Set up SQLite database with initial data"""
    print("Setting up SQLite database...")
    
    # Load environment variables
    load_dotenv()
    
    # Set environment variable to use SQLite
    os.environ["USE_SQLITE"] = "true"
    
    # Define SQLite database path
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    db_path = os.path.join(instance_path, 'app.db')
    
    # Check if database already exists
    db_exists = os.path.exists(db_path)
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Explicitly set file permissions
    os.chmod(db_path, 0o666)  # Read/write for everyone
    
    if not db_exists:
        # Create basic tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            event_type TEXT NOT NULL,
            venue TEXT,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            image_url TEXT,
            capacity INTEGER,
            min_team_size INTEGER,
            max_team_size INTEGER,
            is_team_event BOOLEAN DEFAULT 0,
            registration_deadline TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            creator_id INTEGER,
            event_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES user(id),
            FOREIGN KEY (event_id) REFERENCES event(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            payment_status TEXT DEFAULT 'unpaid',
            payment_id TEXT,
            team_id INTEGER,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            institution TEXT,
            why_join TEXT,
            experience TEXT,
            document_filename TEXT,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (event_id) REFERENCES event(id),
            FOREIGN KEY (team_id) REFERENCES team(id)
        )
        ''')
        
        # Create admin user if it doesn't exist
        cursor.execute("SELECT * FROM user WHERE username = 'admin'")
        if not cursor.fetchone():
            password_hash = generate_password_hash("admin")
            cursor.execute(
                "INSERT INTO user (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
                ("admin", "admin@example.com", password_hash, True)
            )
            print("Admin user created with username 'admin' and password 'admin'")
        
        # Create sample events
        cursor.execute("SELECT * FROM event LIMIT 1")
        if not cursor.fetchone():
            # Create a workshop event
            cursor.execute('''
            INSERT INTO event (name, description, event_type, venue, start_date, end_date, image_url, capacity, is_team_event)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "Web Development Workshop", 
                "Learn the fundamentals of web development with HTML, CSS, and JavaScript.", 
                "workshop", 
                "Tech Hall A", 
                "2025-04-15 10:00:00", 
                "2025-04-15 16:00:00", 
                "https://source.unsplash.com/random/900×700/?coding", 
                30, 
                False
            ))
            
            # Create a hackathon event
            cursor.execute('''
            INSERT INTO event (name, description, event_type, venue, start_date, end_date, image_url, capacity, is_team_event, min_team_size, max_team_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "Innovate 2025 Hackathon", 
                "48-hour hackathon to build innovative solutions for real-world problems.", 
                "hackathon", 
                "Innovation Center", 
                "2025-05-20 09:00:00", 
                "2025-05-22 09:00:00", 
                "https://source.unsplash.com/random/900×700/?hackathon", 
                100, 
                True,
                2,
                4
            ))
            
            print("Sample events created")
    else:
        print("Admin user already exists.")
    
    # Commit and close connection
    conn.commit()
    conn.close()
    
    print("\nSQLite database setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_sqlite_database() 
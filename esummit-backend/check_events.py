from app import create_app, db
from app.models.event import Event
import psycopg2
import os

def check_events():
    app = create_app()
    with app.app_context():
        try:
            # Try to query events with SQLAlchemy
            events = Event.query.all()
            print(f"Found {len(events)} events using SQLAlchemy")
            for event in events:
                print(f"  - {event.id}: {event.name}")
                
            # Also check directly with SQL
            db_url = os.environ.get('DATABASE_URL')
            conn_parts = db_url.split('://')[1].split('@')
            user_pass = conn_parts[0].split(':')
            host_db = conn_parts[1].split('/')
            
            username = user_pass[0]
            password = user_pass[1]
            host = host_db[0].split('?')[0]
            if '-pooler' in host:
                host = host.replace('-pooler', '')
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
                cursor.execute("SELECT COUNT(*) FROM event")
                count = cursor.fetchone()[0]
                print(f"\nFound {count} events using direct SQL")
                
                cursor.execute("SELECT id, name, description, venue FROM event")
                events_sql = cursor.fetchall()
                for event in events_sql:
                    print(f"  - {event[0]}: {event[1]} at {event[3]}")
                    
            # Test adding a sample event
            try:
                print("\nAttempting to create a test event...")
                from datetime import datetime, timedelta
                
                # Check if test event exists
                test_event = Event.query.filter_by(name="Test Event").first()
                if test_event:
                    print(f"Test event already exists (ID: {test_event.id})")
                else:
                    # Create a new event
                    now = datetime.utcnow()
                    event = Event(
                        name="Test Event",
                        description="This is a test event created to verify event creation",
                        start_date=now + timedelta(days=7),
                        end_date=now + timedelta(days=7, hours=2),
                        venue="Test Venue",
                        registration_deadline=now + timedelta(days=5),
                        event_type="workshop",
                        is_team_event=False,
                        capacity=50
                    )
                    
                    db.session.add(event)
                    db.session.commit()
                    
                    print(f"Test event created successfully with ID: {event.id}")
                    
                    # Verify in database
                    test_event = Event.query.filter_by(name="Test Event").first()
                    if test_event:
                        print(f"Verified: Test event exists in database with ID: {test_event.id}")
                    else:
                        print("ERROR: Test event does not exist in database even after commit!")
            except Exception as e:
                print(f"Error creating test event: {e}")
                db.session.rollback()
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_events() 
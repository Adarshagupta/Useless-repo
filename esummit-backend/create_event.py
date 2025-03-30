import psycopg2
import os
from datetime import datetime, timedelta

def create_event():
    try:
        # Get database URL from environment 
        db_url = os.environ.get('DATABASE_URL')
        
        # Parse connection string
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
            # Check if we have any events
            cursor.execute("SELECT COUNT(*) FROM event")
            count = cursor.fetchone()[0]
            print(f"Current event count: {count}")
            
            # Create sample events if none exists
            if count == 0:
                # Create timestamps
                now = datetime.utcnow()
                
                # Sample events data
                events = [
                    {
                        'name': 'Hackathon 2025',
                        'description': 'A 24-hour coding competition where teams build innovative solutions.',
                        'start_date': (now + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                        'end_date': (now + timedelta(days=31)).strftime('%Y-%m-%d %H:%M:%S'),
                        'venue': 'Main Campus Auditorium',
                        'registration_deadline': (now + timedelta(days=25)).strftime('%Y-%m-%d %H:%M:%S'),
                        'capacity': 100,
                        'event_type': 'hackathon',
                        'is_team_event': True,
                        'min_team_size': 2,
                        'max_team_size': 4
                    },
                    {
                        'name': 'Workshop: Intro to AI',
                        'description': 'Learn the basics of artificial intelligence and machine learning.',
                        'start_date': (now + timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S'),
                        'end_date': (now + timedelta(days=15, hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
                        'venue': 'Tech Building Room 101',
                        'registration_deadline': (now + timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
                        'capacity': 50,
                        'event_type': 'workshop',
                        'is_team_event': False,
                        'min_team_size': None,
                        'max_team_size': None
                    },
                    {
                        'name': 'Startup Pitch Competition',
                        'description': 'Present your business ideas to investors and win funding.',
                        'start_date': (now + timedelta(days=45)).strftime('%Y-%m-%d %H:%M:%S'),
                        'end_date': (now + timedelta(days=45, hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                        'venue': 'Business School Auditorium',
                        'registration_deadline': (now + timedelta(days=40)).strftime('%Y-%m-%d %H:%M:%S'),
                        'capacity': 25,
                        'event_type': 'competition',
                        'is_team_event': True,
                        'min_team_size': 1,
                        'max_team_size': 3
                    }
                ]
                
                # Insert events
                for event in events:
                    cursor.execute("""
                        INSERT INTO event (
                            name, description, start_date, end_date, venue, 
                            registration_deadline, capacity, event_type, 
                            is_team_event, min_team_size, max_team_size, 
                            created_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, 
                            %s, %s, %s, 
                            %s, %s, %s, 
                            %s
                        ) RETURNING id
                    """, (
                        event['name'], 
                        event['description'],
                        event['start_date'],
                        event['end_date'],
                        event['venue'],
                        event['registration_deadline'],
                        event['capacity'],
                        event['event_type'],
                        event['is_team_event'],
                        event['min_team_size'],
                        event['max_team_size'],
                        now.strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    event_id = cursor.fetchone()[0]
                    print(f"Created event: {event['name']} with ID: {event_id}")
                
                # Verify events were created
                cursor.execute("SELECT COUNT(*) FROM event")
                new_count = cursor.fetchone()[0]
                print(f"New event count: {new_count}")
                
                if new_count > count:
                    print("Events created successfully!")
                else:
                    print("Failed to create events.")
            else:
                print("Events already exist in the database. No new events created.")
                
            # List all events
            cursor.execute("SELECT id, name, event_type, venue FROM event")
            events = cursor.fetchall()
            print("\nAll events in database:")
            for event in events:
                print(f"  - ID: {event[0]}, Name: {event[1]}, Type: {event[2]}, Venue: {event[3]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_event() 
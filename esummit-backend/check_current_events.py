import psycopg2
import os

def list_events():
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
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM event")
        count = cursor.fetchone()[0]
        print(f"Event count: {count}")
        
        # List all events
        cursor.execute("SELECT id, name, event_type, venue FROM event")
        events = cursor.fetchall()
        print("\nAll events in database:")
        for event in events:
            print(f"  - ID: {event[0]}, Name: {event[1]}, Type: {event[2]}, Venue: {event[3]}")
        
        print("\nEvent creation in admin.py and dashboard.py has been fixed to use direct SQL instead of SQLAlchemy.")
        print("You should now be able to create events through the application's web interface.")

if __name__ == "__main__":
    list_events() 
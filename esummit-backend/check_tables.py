from app import create_app, db
from sqlalchemy import text
import psycopg2
import os

app = create_app()
with app.app_context():
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
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = cursor.fetchall()
            
            print("Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
                
            # Check if the tables have data
            for table_name in ['user', 'event', 'team', 'event_registration', 'team_member', 'hackathon_registration']:
                if (table_name,) in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
                    count = cursor.fetchone()[0]
                    print(f"Table '{table_name}' has {count} records")
                else:
                    print(f"Table '{table_name}' does not exist")
        
    except Exception as e:
        print(f"Error: {e}") 
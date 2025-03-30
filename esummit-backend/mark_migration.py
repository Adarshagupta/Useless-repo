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
            # Check if alembic_version table exists
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'alembic_version')")
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                print("Creating alembic_version table...")
                cursor.execute("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL, PRIMARY KEY (version_num))")
                print("Table created!")
            
            # Insert migration version
            cursor.execute("DELETE FROM alembic_version")  # Remove any existing versions
            cursor.execute("INSERT INTO alembic_version (version_num) VALUES ('1e171ece3db3')")
            print("Migration marked as completed!")
            
            # Verify it was inserted
            cursor.execute("SELECT version_num FROM alembic_version")
            version = cursor.fetchone()
            print(f"Current version: {version[0]}")
    
    except Exception as e:
        print(f"Error: {e}") 
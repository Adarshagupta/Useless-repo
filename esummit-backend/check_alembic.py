from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Check if alembic_version table exists
        result = db.session.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'alembic_version')")).fetchone()
        print(f"alembic_version table exists: {result[0]}")
        
        if result[0]:
            # Check the current version
            version = db.session.execute(text("SELECT version_num FROM alembic_version")).fetchone()
            print(f"Current version: {version[0] if version else 'None'}")
        
        # Check available database schemas
        schemas = db.session.execute(text("SELECT schema_name FROM information_schema.schemata")).fetchall()
        print("Available schemas:")
        for schema in schemas:
            print(f"  - {schema[0]}")
            
        # Check if our app can create tables
        print("\nAttempting to create a test table...")
        db.session.execute(text("CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY, test_column VARCHAR(100))"))
        db.session.commit()
        print("Test table created successfully!")
        
        # Check if test table was created
        result = db.session.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'test_table')")).fetchone()
        print(f"test_table exists: {result[0]}")
        
        # Drop the test table
        if result[0]:
            db.session.execute(text("DROP TABLE test_table"))
            db.session.commit()
            print("Test table dropped.")
    except Exception as e:
        print(f"Error: {e}") 
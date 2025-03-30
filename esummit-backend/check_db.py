from app import create_app, db
from app.models.event import Event
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Get the inspector
    inspector = inspect(db.engine)
    
    # Get all table names
    tables = inspector.get_table_names()
    print("Tables in database:", tables)
    
    # Check event table columns
    if 'event' in tables:
        columns = inspector.get_columns('event')
        print("\nColumns in event table:")
        for col in columns:
            print(f"- {col['name']}: {col['type']}")
    
    # Try to query events
    try:
        events = Event.query.all()
        print(f"\nFound {len(events)} events:")
        for event in events:
            print(f"- {event.name} ({event.event_type}) - {event.start_date}")
    except Exception as e:
        print(f"\nError querying events: {str(e)}") 
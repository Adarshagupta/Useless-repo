from app import create_app, db
from app.models.event import Event
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Create a test event
    start_date = datetime.utcnow() + timedelta(days=1)
    end_date = start_date + timedelta(days=2)
    
    event = Event(
        name="Test Event",
        description="This is a test event",
        start_date=start_date,
        end_date=end_date,
        venue="Test Venue",
        registration_deadline=end_date,
        event_type="workshop",
        is_team_event=False
    )
    
    try:
        db.session.add(event)
        db.session.commit()
        print("Event created successfully!")
        
        # Verify event exists
        events = Event.query.all()
        print(f"\nFound {len(events)} events:")
        for e in events:
            print(f"- {e.name} ({e.event_type}) - {e.start_date}")
    except Exception as e:
        print(f"Error creating event: {str(e)}")
        db.session.rollback() 
from app import create_app
from flask import render_template
import os

def test_templates():
    """Test if templates exist and can be rendered"""
    app = create_app()
    
    # Check if staff templates exist
    staff_template_dir = os.path.join(app.root_path, 'templates', 'staff')
    if os.path.exists(staff_template_dir):
        print(f"Staff template directory exists: {staff_template_dir}")
        print("\nStaff templates:")
        for template in os.listdir(staff_template_dir):
            print(f"- {template}")
    else:
        print(f"Staff template directory does NOT exist: {staff_template_dir}")
    
    # Try to render the staff index template
    with app.app_context():
        try:
            # Create dummy data for the template
            active_events = []
            pending_registrations = []
            total_participants = 0
            total_teams = 0
            recent_activities = []
            upcoming_events = []
            
            # Try to render the template
            render_template('staff/index.html',
                         active_events=active_events,
                         pending_registrations=pending_registrations,
                         total_participants=total_participants,
                         total_teams=total_teams,
                         recent_activities=recent_activities,
                         upcoming_events=upcoming_events)
            print("\nSuccessfully rendered staff/index.html template!")
        except Exception as e:
            print(f"\nError rendering staff/index.html template: {str(e)}")

if __name__ == "__main__":
    test_templates()

from app import create_app
from app.routes.staff import staff_bp

def test_staff_routes():
    """Test if staff routes are registered correctly"""
    app = create_app()
    
    # Check if staff blueprint is registered
    if staff_bp.name in [bp.name for bp in app.blueprints.values()]:
        print(f"Staff blueprint is registered with URL prefix: {staff_bp.url_prefix}")
    else:
        print("Staff blueprint is NOT registered!")
    
    # List all routes in the staff blueprint
    print("\nRoutes in staff blueprint:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('staff.'):
            print(f"- {rule.rule} -> {rule.endpoint}")

if __name__ == "__main__":
    test_staff_routes()

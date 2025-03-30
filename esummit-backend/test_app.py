from app import create_app

def test_app_routes():
    app = create_app()
    with app.test_client() as client:
        # Test the index route
        response = client.get('/')
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.data.decode('utf-8')[:500]}...")  # Show first 500 chars
        
        # Try other routes
        response = client.get('/login')
        print(f"\nLogin Route Status: {response.status_code}")
        
        response = client.get('/register')
        print(f"Register Route Status: {response.status_code}")
        
        response = client.get('/events')
        print(f"Events Route Status: {response.status_code}")
        
        # Test a non-existent route
        response = client.get('/this-route-does-not-exist')
        print(f"Non-existent Route Status: {response.status_code}")

if __name__ == "__main__":
    test_app_routes() 
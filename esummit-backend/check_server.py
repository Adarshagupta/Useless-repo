import socket
import subprocess
import os

def check_server_status():
    print("Checking server status...")
    
    # Check if port 5000 is open inside the container
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", 5000))
        print("Port 5000 is NOT in use (Gunicorn might not be running)")
    except socket.error:
        print("Port 5000 is in use (Gunicorn is running)")
    finally:
        s.close()
    
    # Try a simple HTTP request to localhost within the container
    try:
        import urllib.request
        response = urllib.request.urlopen("http://localhost:5000/")
        print(f"HTTP Status: {response.getcode()}")
        print(f"Content-Type: {response.info().get('Content-Type')}")
        print(f"Content length: {len(response.read())}")
    except Exception as e:
        print(f"Error accessing http://localhost:5000/: {e}")
    
    # Print environment info
    print("\nEnvironment variables:")
    for var in ["DATABASE_URL", "FLASK_APP", "FLASK_ENV", "USE_SQLITE"]:
        print(f"  {var}: {os.environ.get(var, 'Not set')}")
    
    # Analyze processes
    try:
        print("\nRunning processes:")
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'gunicorn' in proc.info['name'] or 'python' in proc.info['name']:
                print(f"  {proc.info}")
    except ImportError:
        print("psutil not available")

if __name__ == "__main__":
    check_server_status() 
import requests
import sys

def check_server(url):
    try:
        print(f"Checking if server is responding at {url}...")
        response = requests.get(url, timeout=5)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Try multiple URLs to see if any respond
    urls = [
        "http://127.0.0.1:8008/",
        "http://127.0.0.1:8008/docs",
        "http://127.0.0.1:8006/",
        "http://127.0.0.1:8006/docs",
        "http://localhost:8008/",
        "http://localhost:8006/"
    ]
    
    for url in urls:
        if check_server(url):
            print(f"Server is responding at {url}")
            sys.exit(0)
    
    print("None of the tested URLs are responding. The server may not be running.")
    sys.exit(1) 
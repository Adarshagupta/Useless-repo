import urllib.request
import sys

def make_request():
    print("Making HTTP request to http://localhost:5001/")
    
    try:
        response = urllib.request.urlopen("http://localhost:5001/")
        print(f"Status code: {response.getcode()}")
        print(f"Content type: {response.headers.get('Content-Type')}")
        
        # Read the first 500 characters of content
        content = response.read().decode('utf-8')
        print(f"Content preview: {content[:500]}...")
        
        print("Request successful!")
        return 0
    except Exception as e:
        print(f"Error making request: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(make_request()) 
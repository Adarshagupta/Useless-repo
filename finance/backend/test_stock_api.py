import requests
import json

# Base URL
base_url = "http://127.0.0.1:8008/api/v1"  # Updated port to 8008

def test_get_stocks():
    """Test retrieving the list of stocks"""
    url = f"{base_url}/stocks/"
    try:
        response = requests.get(url, timeout=5)  # Add timeout
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} stocks")
            print(json.dumps(data[:2], indent=2))  # Print first 2 stocks
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

def test_search_stocks():
    """Test searching for stocks"""
    query = "apple"
    url = f"{base_url}/stocks/search?query={query}"
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} stocks matching '{query}'")
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

def test_stock_details():
    """Test retrieving details for a specific stock"""
    symbol = "AAPL"
    url = f"{base_url}/stocks/{symbol}"
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Details for {symbol}:")
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

def test_stock_chart():
    """Test retrieving chart data for a specific stock"""
    symbol = "AAPL"
    period = "1m"  # 1 month
    url = f"{base_url}/stocks/{symbol}/chart?period={period}"
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Chart data for {symbol} (period: {period}):")
            print(f"Found {len(data)} data points")
            print(json.dumps(data[:3], indent=2))  # Print first 3 data points
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

def test_top_gainers():
    """Test retrieving top gaining stocks"""
    url = f"{base_url}/stocks/top-gainers"
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Top gainers:")
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

def test_top_losers():
    """Test retrieving top losing stocks"""
    url = f"{base_url}/stocks/top-losers"
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Top losers:")
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

def test_most_active():
    """Test retrieving most active stocks"""
    url = f"{base_url}/stocks/most-active"
    try:
        response = requests.get(url, timeout=5)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Most active stocks:")
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    print("\n")

if __name__ == "__main__":
    print("Testing Stock API Endpoints\n")
    
    # Test all endpoints
    test_get_stocks()
    test_search_stocks()
    test_stock_details()
    test_stock_chart()
    test_top_gainers()
    test_top_losers()
    test_most_active()
    
    print("Tests completed.") 
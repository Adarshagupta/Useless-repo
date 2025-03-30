#!/usr/bin/env python3
import os
import sys
import time
import logging
import socket
import urllib.request
import psycopg2
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_internet_connectivity():
    """Check if there's a working internet connection"""
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False

def check_neon_api():
    """Check if Neon API is reachable"""
    try:
        urllib.request.urlopen('https://console.neon.tech/api/health', timeout=3)
        return True
    except:
        return False

def check_postgresql_port(host, port=5432, timeout=3):
    """Check if PostgreSQL port is reachable on the host"""
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj.settimeout(timeout)
        result = socket_obj.connect_ex((host, port))
        socket_obj.close()
        return result == 0
    except:
        return False

def test_postgresql_connection(db_url=None):
    """Test connection to PostgreSQL database with detailed diagnostics"""
    # Load environment variables
    load_dotenv()
    
    # Get database URL from argument or environment
    if not db_url:
        db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        logger.error("No database URL provided or found in environment")
        return False
    
    # Extract host from connection string
    try:
        host = db_url.split('@')[1].split('/')[0].split(':')[0]
        logger.info(f"Database host: {host}")
    except:
        logger.error("Could not extract host from database URL")
        host = None
    
    # Check internet connectivity
    print("\nChecking internet connectivity...")
    has_internet = check_internet_connectivity()
    print(f"Internet connection: {'✅ Available' if has_internet else '❌ Not available'}")
    
    if not has_internet:
        print("⚠️  No internet connection. You need internet access to connect to Neon PostgreSQL.")
        return False
    
    # Check Neon API
    print("\nChecking Neon service availability...")
    neon_available = check_neon_api()
    print(f"Neon API status: {'✅ Available' if neon_available else '❌ Not reachable'}")
    
    # Check PostgreSQL port
    if host:
        print(f"\nChecking PostgreSQL port on {host}...")
        port_open = check_postgresql_port(host)
        print(f"PostgreSQL port: {'✅ Open' if port_open else '❌ Closed or blocked'}")
    
    # Full connection test
    print("\nAttempting full PostgreSQL connection...")
    try:
        # Parse connection parameters
        connection_params = {}
        connection_params["connect_timeout"] = 10
        connection_params["application_name"] = "pg-check"
        connection_params["keepalives"] = 1
        connection_params["keepalives_idle"] = 30
        connection_params["keepalives_interval"] = 10
        connection_params["keepalives_count"] = 5
        
        # Try to connect
        start_time = time.time()
        conn = psycopg2.connect(db_url, **connection_params)
        conn.autocommit = True
        
        # Test basic query
        with conn.cursor() as cur:
            # Simple test query
            cur.execute("SELECT 1")
            result = cur.fetchone()
            
            if result and result[0] == 1:
                elapsed = time.time() - start_time
                print(f"✅ Connection successful! Query time: {elapsed:.3f}s")
                
                # Get PostgreSQL version
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                print(f"PostgreSQL version: {version}")
                
                # Get connection info
                cur.execute("SELECT current_database(), current_user")
                db_info = cur.fetchone()
                print(f"Connected to database: {db_info[0]} as user: {db_info[1]}")
                
                conn.close()
                return True
    except Exception as e:
        elapsed = time.time() - start_time if 'start_time' in locals() else 0
        print(f"❌ Connection failed after {elapsed:.3f}s: {str(e)}")
        
        # Additional diagnostics based on the error message
        error_msg = str(e).lower()
        if "password authentication failed" in error_msg:
            print("\n⚠️  Authentication failure - your username or password is incorrect.")
            print("   Check your DATABASE_URL in .env file and ensure credentials are correct.")
        elif "connection refused" in error_msg:
            print("\n⚠️  Connection refused - the database server is not accepting connections.")
            print("   Check if the Neon instance is running and not in sleep mode.")
        elif "timeout" in error_msg:
            print("\n⚠️  Connection timeout - could not reach the database server in time.")
            print("   Check your network connection and ensure there are no firewall issues.")
        elif "no route to host" in error_msg:
            print("\n⚠️  No route to host - cannot reach the database server.")
            print("   Check your network connection and DNS settings.")
        
        return False
    
    return False

def check_env_config():
    """Check environment configuration for PostgreSQL"""
    print("\nChecking environment configuration...")
    load_dotenv()
    
    db_url = os.environ.get('DATABASE_URL')
    use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true'
    
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    # Sanitize for display
    sanitized_url = db_url.replace('//', '//<username>:<password>@')
    print(f"DATABASE_URL: {sanitized_url}")
    
    if use_sqlite:
        print("⚠️  USE_SQLITE is set to 'true' but you're trying to use PostgreSQL")
        print("   Change USE_SQLITE to 'false' in .env file")
    else:
        print("✅ USE_SQLITE is set to 'false', configuration is correct for PostgreSQL")
    
    return True

if __name__ == "__main__":
    print("="*80)
    print("PostgreSQL Connection Diagnostic Tool")
    print("="*80)
    
    # Check configuration
    check_env_config()
    
    # Test connection
    success = test_postgresql_connection()
    
    print("\nSummary:")
    if success:
        print("✅ PostgreSQL connection is working correctly")
    else:
        print("❌ PostgreSQL connection failed")
        print("\nRecommendations:")
        print("1. Verify that your Neon PostgreSQL instance is active")
        print("2. Check that you have the correct connection string in .env")
        print("3. Make sure your network allows connections to port 5432")
        print("4. Set USE_SQLITE=false in .env file")
        print("5. Restart the application with: docker compose restart web")
    
    sys.exit(0 if success else 1) 
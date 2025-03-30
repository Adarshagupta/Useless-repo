#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import logging
from dotenv import load_dotenv, set_key
import requests
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_env_file(key, value, env_file='.env'):
    """Update a key in the .env file"""
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(f"{key}={value}\n")
        logger.info(f"Created {env_file} file with {key}")
    else:
        set_key(env_file, key, value)
        logger.info(f"Updated {key} in {env_file}")

def check_internet_connection():
    """Check if we can reach the internet"""
    try:
        # Try to connect to Cloudflare DNS
        requests.get("https://1.1.1.1", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

def check_neon_availability():
    """Check if Neon's service is available"""
    try:
        response = requests.get("https://console.neon.tech/api/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validate_connection_string(conn_string):
    """Validate that a connection string has the correct format"""
    if not conn_string.startswith("postgresql://"):
        return False
    
    # Very basic validation - should contain username, password, host, and database
    parts = conn_string.split("@")
    if len(parts) != 2:
        return False
    
    credentials = parts[0].split("://")[1]
    if ":" not in credentials:
        return False
    
    host_db = parts[1]
    if "/" not in host_db:
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Neon PostgreSQL Setup Tool")
    parser.add_argument("--conn-string", help="New Neon PostgreSQL connection string")
    parser.add_argument("--use-sqlite", action="store_true", help="Configure to use SQLite instead of PostgreSQL")
    parser.add_argument("--check", action="store_true", help="Check current database configuration")
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check current configuration
    if args.check or (not args.conn_string and not args.use_sqlite):
        current_url = os.environ.get('DATABASE_URL')
        use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true'
        
        print("Current Database Configuration:")
        print("------------------------------")
        if use_sqlite:
            print("Database Type: SQLite (local)")
            sqlite_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
            print(f"Database Path: {sqlite_path}")
            if os.path.exists(sqlite_path):
                print(f"Database Size: {os.path.getsize(sqlite_path) / 1024:.2f} KB")
            else:
                print("Database File: Not created yet")
        elif current_url:
            print("Database Type: PostgreSQL (Neon)")
            sanitized_url = current_url.replace('//', '//<username>:<password>@')
            print(f"Connection String: {sanitized_url}")
            
            # Check internet and Neon service
            internet = check_internet_connection()
            neon_available = check_neon_availability() if internet else False
            
            print(f"Internet Connection: {'✅ Available' if internet else '❌ Not available'}")
            print(f"Neon Service Status: {'✅ Online' if neon_available else '❌ Unknown/Offline'}")
            
            # Test connection
            print("\nTesting connection...")
            result = subprocess.run(
                ["python", "pg_diagnostic.py"],
                capture_output=True,
                text=True
            )
            
            # Get last few lines of output
            output_lines = result.stdout.strip().split('\n')[-10:]
            for line in output_lines:
                print(line)
        else:
            print("No database configuration found.")
        
        if not args.conn_string and not args.use_sqlite:
            return
    
    # Configure for SQLite
    if args.use_sqlite:
        update_env_file('USE_SQLITE', 'true')
        logger.info("Configured to use SQLite database")
        
        # Run the application to initialize the database
        print("\nInitializing SQLite database...")
        subprocess.run(
            ["python", "run.py", "--sqlite", "--debug", "--port", "5001"],
            capture_output=True
        )
        
        # Check if the database was created
        sqlite_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
        if os.path.exists(sqlite_path):
            print(f"SQLite database created at: {sqlite_path}")
            
            # Test connection
            print("\nTesting SQLite connection...")
            subprocess.run(["python", "sqlite_check.py"])
        else:
            print("Failed to create SQLite database")
    
    # Update PostgreSQL connection string
    elif args.conn_string:
        if not validate_connection_string(args.conn_string):
            logger.error("Invalid PostgreSQL connection string format")
            print("Connection string should have format: postgresql://username:password@host/database")
            return
        
        # Update the connection string
        update_env_file('DATABASE_URL', args.conn_string)
        update_env_file('USE_SQLITE', 'false')
        
        # Test the connection
        print("\nTesting new PostgreSQL connection...")
        subprocess.run(["python", "pg_diagnostic.py", args.conn_string])

if __name__ == "__main__":
    main() 
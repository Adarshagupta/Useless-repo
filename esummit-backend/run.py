#!/usr/bin/env python3
import os
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import after environment is configured
from app import create_app

# Create app instance at module level for Flask CLI to find
app = create_app()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the E-Summit application')
    parser.add_argument('--sqlite', action='store_true', help='Use SQLite database instead of PostgreSQL')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    args = parser.parse_args()
    
    # Configure SQLite usage if requested
    if args.sqlite:
        os.environ['USE_SQLITE'] = 'true'
        print("Using SQLite database for testing")
    
    # Set Flask environment
    os.environ['FLASK_ENV'] = 'development' if args.debug else 'production'
    os.environ['FLASK_DEBUG'] = '1' if args.debug else '0'
    
    # Import after environment is configured
    from app import db
    
    # Create tables if using SQLite
    if args.sqlite:
        with app.app_context():
            db.create_all()
            print("SQLite database initialized")
    
    # Run the application
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)

if __name__ == '__main__':
    main() 
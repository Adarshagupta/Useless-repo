#!/usr/bin/env python
"""
Database Connection Check Script

This script tests the connection to the database and verifies basic functionality.
"""

import os
import time
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_database_connection():
    """Test database connection and basic queries"""
    load_dotenv()
    
    # Get database URL
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        logging.error("No DATABASE_URL environment variable found")
        return False
    
    # Remove pooler from URL if present
    if '-pooler' in db_url:
        logging.info("Converting pooler URL to direct connection")
        db_url = db_url.replace('-pooler', '')
    
    # Log sanitized URL
    sanitized_url = db_url.replace('//', '//<USERNAME>:<PASSWORD>@')
    logging.info(f"Testing connection to: {sanitized_url}")
    
    # Create engine with appropriate settings
    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=1,
            max_overflow=0,
            pool_timeout=10,
            connect_args={
                'connect_timeout': 10,
                'application_name': 'db-check',
                'keepalives': 1,
                'keepalives_idle': 30
            } if 'postgresql' in db_url else {}
        )
        
        # Attempt connection and simple query
        logging.info("Attempting connection...")
        start_time = time.time()
        
        with engine.connect() as conn:
            # Simple test query
            result = conn.execute(text("SELECT 1"))
            first_row = result.fetchone()
            if first_row and first_row[0] == 1:
                elapsed = time.time() - start_time
                logging.info(f"Connection successful! Query time: {elapsed:.3f}s")
                
                # Test more complex query if connected to PostgreSQL
                if 'postgresql' in db_url:
                    logging.info("Testing PostgreSQL system query...")
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    logging.info(f"Database version: {version}")
                    
                    # Test connection parameters
                    result = conn.execute(text("SHOW max_connections"))
                    max_connections = result.fetchone()[0]
                    logging.info(f"Max connections: {max_connections}")
                
                return True
            else:
                logging.error("Connection test failed: unexpected query result")
                return False
                
    except SQLAlchemyError as e:
        elapsed = time.time() - start_time
        logging.error(f"Database connection failed after {elapsed:.3f}s: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Database Connection Check")
    print("========================")
    
    success = check_database_connection()
    
    if not success:
        print("\nConnection check FAILED! Please check database configuration.")
        sys.exit(1)
    else:
        print("\nConnection check SUCCESSFUL!")
        sys.exit(0) 
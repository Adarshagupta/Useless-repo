#!/usr/bin/env python3
import os
import sys
import logging
import sqlite3
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_sqlite_database():
    """Check if the SQLite database is working correctly"""
    
    # Set environment variable to use SQLite
    os.environ['USE_SQLITE'] = 'true'
    
    # Get the path to the SQLite database
    sqlite_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    
    logger.info(f"Checking SQLite database at: {sqlite_path}")
    
    # Check if the database file exists
    if not os.path.exists(sqlite_path):
        logger.warning(f"SQLite database file does not exist at {sqlite_path}")
        logger.info("This is normal if you haven't initialized the database yet")
        logger.info("Run 'python run.py --sqlite --debug' to create the database")
        return False
    
    # Try to connect to the database
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # Test a simple query
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        logger.info(f"Successfully connected to SQLite. Version: {version[0]}")
        
        # Check if any tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            logger.info(f"Found {len(tables)} tables in the database:")
            for table in tables:
                logger.info(f"- {table[0]}")
                
                # Get column info for each table
                cursor.execute(f"PRAGMA table_info({table[0]});")
                columns = cursor.fetchall()
                logger.debug(f"  Table {table[0]} has {len(columns)} columns")
        else:
            logger.warning("No tables found in the database")
            logger.info("This is normal if you haven't initialized the database yet")
            logger.info("Run 'python run.py --sqlite --debug' to create the database")
        
        # Close the connection
        conn.close()
        return True
        
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    if check_sqlite_database():
        logger.info("SQLite database check completed successfully")
        sys.exit(0)
    else:
        logger.error("SQLite database check failed")
        sys.exit(1) 
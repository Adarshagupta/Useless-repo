#!/usr/bin/env python3
import os
import sys
import time
import logging
import psycopg2
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_neon_connection(db_url=None, use_pooler=False):
    """Test connection to Neon PostgreSQL database"""
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL from argument or environment
    if not db_url:
        db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        logger.error("No database URL provided or found in environment")
        return False
    
    # Handle pooler configuration
    original_url = db_url
    if '-pooler' in db_url and not use_pooler:
        db_url = db_url.replace('-pooler', '')
        logger.info("Testing direct connection (removed pooler)")
    elif '-pooler' not in db_url and use_pooler:
        # Add pooler to connection string if not present
        parts = db_url.split('@')
        if len(parts) == 2:
            hostname = parts[1].split('/')[0]
            if '-pooler' not in hostname:
                new_hostname = hostname.replace('.', '-pooler.', 1)
                db_url = db_url.replace(hostname, new_hostname)
                logger.info("Testing pooler connection")
    
    # Sanitize for logging
    sanitized_url = db_url.replace('//', '//USERNAME:PASSWORD@')
    logger.info(f"Testing connection to: {sanitized_url}")
    
    try:
        # Parse connection parameters
        connection_params = {}
        
        # Add connection timeout
        connection_params["connect_timeout"] = 10
        connection_params["application_name"] = "pg-diagnostic"
        
        # Add keepalive parameters
        connection_params["keepalives"] = 1
        connection_params["keepalives_idle"] = 30
        connection_params["keepalives_interval"] = 10
        connection_params["keepalives_count"] = 5
        
        # Try to connect
        start_time = time.time()
        logger.info("Attempting connection...")
        
        conn = psycopg2.connect(db_url, **connection_params)
        conn.autocommit = True
        
        # Test basic query
        with conn.cursor() as cur:
            # Simple test query
            cur.execute("SELECT 1")
            result = cur.fetchone()
            
            if result and result[0] == 1:
                elapsed = time.time() - start_time
                logger.info(f"Connection successful! Query time: {elapsed:.3f}s")
                
                # Get PostgreSQL version
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                logger.info(f"PostgreSQL version: {version}")
                
                # Get connection info
                cur.execute("SELECT current_database(), current_user")
                db_info = cur.fetchone()
                logger.info(f"Connected to database: {db_info[0]} as user: {db_info[1]}")
                
                # Test more detailed information
                try:
                    cur.execute("SHOW max_connections")
                    max_conn = cur.fetchone()[0]
                    logger.info(f"Max connections: {max_conn}")
                    
                    cur.execute("SELECT count(*) FROM pg_stat_activity")
                    current_conn = cur.fetchone()[0]
                    logger.info(f"Current connections: {current_conn}")
                except Exception as e:
                    logger.warning(f"Could not get detailed server info: {e}")
                
                return True
            else:
                logger.error("Query returned unexpected result")
                return False
    
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Connection failed after {elapsed:.3f}s: {str(e)}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logger.info("Connection closed")

if __name__ == "__main__":
    print("Neon PostgreSQL Connection Diagnostic")
    print("====================================")
    
    # Custom connection string from command line
    custom_url = None
    if len(sys.argv) > 1:
        custom_url = sys.argv[1]
        print(f"Using provided connection string")
    
    # Test direct connection first
    print("\nTesting direct connection...")
    direct_success = test_neon_connection(custom_url, use_pooler=False)
    
    # Test pooler connection
    print("\nTesting connection pooler...")
    pooler_success = test_neon_connection(custom_url, use_pooler=True)
    
    # Show summary
    print("\nSummary:")
    print(f"Direct connection: {'✅ SUCCESS' if direct_success else '❌ FAILED'}")
    print(f"Pooler connection: {'✅ SUCCESS' if pooler_success else '❌ FAILED'}")
    
    if not direct_success and not pooler_success:
        print("\nBoth connection methods failed. Please check:")
        print("1. Your network connection to Neon's servers")
        print("2. Database credentials and permissions")
        print("3. Firewall settings that might block PostgreSQL connections")
        print("4. Neon console to see if your database is active")
        sys.exit(1)
    else:
        recommendation = "pooler" if pooler_success else "direct"
        print(f"\nRecommendation: Use the {recommendation} connection for your application")
        sys.exit(0) 
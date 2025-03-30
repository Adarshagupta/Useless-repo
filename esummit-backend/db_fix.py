#!/usr/bin/env python3
import os
import sys
import logging
import sqlite3
import time
from pathlib import Path
import shutil
import hashlib
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def diagnose_sqlite_database():
    """Diagnose SQLite database issues and attempt to fix them"""
    print("="*80)
    print("SQLite Database Diagnostic Tool")
    print("="*80)
    
    # Define database path
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    db_path = os.path.join(instance_path, 'app.db')
    
    # Check if database directory exists
    print(f"\nChecking database directory: {instance_path}")
    if not os.path.exists(instance_path):
        print(f"❌ Database directory doesn't exist. Creating it...")
        os.makedirs(instance_path, exist_ok=True)
        print(f"✅ Created database directory: {instance_path}")
    else:
        print(f"✅ Database directory exists: {instance_path}")
    
    # Check if database file exists
    print(f"\nChecking database file: {db_path}")
    if not os.path.exists(db_path):
        print("❌ Database file doesn't exist")
        run_setup_database = input("Do you want to create a new database? (y/n): ")
        if run_setup_database.lower() == 'y':
            try:
                import setup_database
                setup_database.setup_sqlite_database()
                print("✅ Database created successfully")
            except Exception as e:
                print(f"❌ Failed to create database: {e}")
                sys.exit(1)
    else:
        print(f"✅ Database file exists: {db_path}")
        
        # Check file size
        file_size = os.path.getsize(db_path) / 1024  # in KB
        print(f"   File size: {file_size:.2f} KB")
        
        # Check permissions
        permissions = oct(os.stat(db_path).st_mode)[-3:]
        print(f"   Permissions: {permissions}")
        
        if not os.access(db_path, os.R_OK | os.W_OK):
            print("❌ Insufficient permissions. Fixing permissions...")
            try:
                os.chmod(db_path, 0o666)  # Read/write for everyone
                print("✅ Fixed permissions")
            except Exception as e:
                print(f"❌ Failed to fix permissions: {e}")
    
    # Try to connect to database
    print("\nTesting database connection...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        
        print(f"✅ Successfully connected to database")
        print(f"   Found {len(tables)} tables: {', '.join(tables)}")
        
        # Check if user table exists and has data
        if 'user' in tables:
            cursor.execute("SELECT COUNT(*) FROM user")
            user_count = cursor.fetchone()[0]
            print(f"   Users in database: {user_count}")
            
            # Check admin user
            cursor.execute("SELECT COUNT(*) FROM user WHERE is_admin = 1")
            admin_count = cursor.fetchone()[0]
            print(f"   Admin users: {admin_count}")
            
            if admin_count == 0:
                print("❌ No admin user found. Creating default admin...")
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash("admin")
                cursor.execute(
                    "INSERT INTO user (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
                    ("admin", "admin@example.com", password_hash, True)
                )
                conn.commit()
                print("✅ Created admin user with username 'admin' and password 'admin'")
        
        # Check database integrity
        print("\nChecking database integrity...")
        cursor.execute("PRAGMA integrity_check")
        integrity = cursor.fetchone()[0]
        if integrity == 'ok':
            print("✅ Database integrity check passed")
        else:
            print(f"❌ Database integrity check failed: {integrity}")
            
            # Backup and repair
            backup_file = f"{db_path}.backup-{int(time.time())}"
            shutil.copy2(db_path, backup_file)
            print(f"✅ Created backup at {backup_file}")
            
            # Try vacuum to repair
            print("   Attempting to repair database...")
            cursor.execute("VACUUM")
            conn.commit()
            print("✅ Database repair completed")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        
        # Check if database is corrupt
        if "database disk image is malformed" in str(e) or "file is not a database" in str(e):
            print("\nDatabase appears to be corrupt. Attempting recovery...")
            
            # Create backup of corrupt database
            backup_file = f"{db_path}.corrupt-{int(time.time())}"
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_file)
                print(f"✅ Created backup of corrupt database at {backup_file}")
            
            # Remove corrupt database
            try:
                os.remove(db_path)
                print(f"✅ Removed corrupt database file")
                
                # Create new database
                print("   Creating new database...")
                import setup_database
                setup_database.setup_sqlite_database()
                print("✅ New database created successfully")
            except Exception as e:
                print(f"❌ Failed to fix database: {e}")
    
    print("\nDatabase Environment Configuration:")
    with open('.env', 'r') as f:
        env_content = f.readlines()
        for line in env_content:
            if 'USE_SQLITE' in line or 'DATABASE_URL' in line:
                print(f"   {line.strip()}")
    
    # Docker configuration
    print("\nDocker Configuration:")
    docker_compose_path = 'docker-compose.yml'
    if os.path.exists(docker_compose_path):
        with open(docker_compose_path, 'r') as f:
            docker_content = f.readlines()
            in_web_section = False
            in_env_section = False
            for line in docker_content:
                if 'web:' in line:
                    in_web_section = True
                elif in_web_section and 'environment:' in line:
                    in_env_section = True
                elif in_env_section and ('USE_SQLITE' in line or 'DATABASE_URL' in line):
                    print(f"   {line.strip()}")
    
    print("\nRecommendations:")
    print("1. Ensure USE_SQLITE=true is set in .env file")
    print("2. Verify that sqlite_data volume is properly mounted in Docker")
    print("3. If issues persist, restart the application with:")
    print("   docker compose down && docker compose up -d")
    print("\nDatabase diagnostics completed successfully!")

if __name__ == "__main__":
    diagnose_sqlite_database() 
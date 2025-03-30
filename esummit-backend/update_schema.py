import sqlite3
import os
from pathlib import Path

def update_database_schema():
    # Path to SQLite database
    db_path = Path('instance/app.db')
    
    if not db_path.exists():
        print(f"Database file not found at {db_path}")
        return False
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if prize_pool column exists
        cursor.execute("PRAGMA table_info(event)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'prize_pool' not in column_names:
            print("Adding prize_pool column to event table...")
            cursor.execute("ALTER TABLE event ADD COLUMN prize_pool INTEGER")
            conn.commit()
            print("Column added successfully!")
        else:
            print("prize_pool column already exists.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating database schema: {e}")
        return False

if __name__ == "__main__":
    success = update_database_schema()
    if success:
        print("Database schema updated successfully.")
    else:
        print("Failed to update database schema.") 
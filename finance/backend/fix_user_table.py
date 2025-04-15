from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)

# SQL statements to add the username column
add_username_sql = """
-- Check if the username column exists first to avoid errors
DO $$
BEGIN
    -- Check if username column already exists
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'user' AND column_name = 'username'
    ) THEN
        -- Add the username column
        ALTER TABLE "user" ADD COLUMN username VARCHAR;
        
        -- Update existing users with a default username based on their ID
        UPDATE "user" SET username = CONCAT('user_', id) WHERE username IS NULL;
        
        -- Make the column not nullable
        ALTER TABLE "user" ALTER COLUMN username SET NOT NULL;
        
        -- Add a unique index
        CREATE UNIQUE INDEX ix_user_username ON "user" (username);
    END IF;
END
$$;
"""

# Execute the SQL
with engine.connect() as conn:
    conn.execute(text(add_username_sql))
    conn.commit()
    print("Username column added to user table successfully!") 
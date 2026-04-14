#!/usr/bin/env python3
"""
Simple migration script using psycopg (no SQLAlchemy dependency)
Works with Python 3.11+ and PostgreSQL 18
"""

import os
import sys
from urllib.parse import urlparse

def migrate():
    """Execute migration to add missing columns to health_profiles table"""
    
    # Get database URL from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not set. Please configure your .env file")
        return False
    
    # Parse PostgreSQL connection URL
    try:
        parsed = urlparse(db_url)
        config = {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/'),
            'user': parsed.username,
            'password': parsed.password
        }
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False
    
    print(f"Connecting to: {config['host']}:{config['port']}/{config['database']}")
    
    # Try psycopg3
    try:
        import psycopg
        print("✅ Using psycopg (PostgreSQL driver)")
        
        with psycopg.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            sslmode='require'
        ) as conn:
            with conn.cursor() as cur:
                # Execute migration SQL
                migration_sql = """
                -- Add missing columns to health_profiles table
                ALTER TABLE health_profiles 
                ADD COLUMN IF NOT EXISTS imc FLOAT NOT NULL DEFAULT 0.0;

                ALTER TABLE health_profiles 
                ADD COLUMN IF NOT EXISTS score INTEGER NOT NULL DEFAULT 0;

                ALTER TABLE health_profiles 
                ADD COLUMN IF NOT EXISTS level VARCHAR(100) NOT NULL DEFAULT 'Sin datos';

                ALTER TABLE health_profiles 
                ADD COLUMN IF NOT EXISTS recommendation VARCHAR(500) NOT NULL DEFAULT 'Por calcular';

                -- Verify migration
                SELECT id, user_id, height_cm, weight_kg, resting_hr, imc, score, level, recommendation
                FROM health_profiles
                LIMIT 5;
                """
                
                # Execute each statement
                for statement in migration_sql.split(';'):
                    if statement.strip():
                        print(f"  Executing: {statement[:60]}...")
                        cur.execute(statement)
                
                # Commit changes
                conn.commit()
                print("✅ Migration completed successfully!")
                return True
                
    except ImportError:
        print("❌ psycopg not installed. Install with: pip install psycopg")
        return False
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    # Check if .env file exists
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"❌ {env_file} not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        sys.exit(1)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    # Run migration
    success = migrate()
    sys.exit(0 if success else 1)

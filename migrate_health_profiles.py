"""
Migration script: Add missing columns to health_profiles table
This adds: imc, score, level, recommendation columns

USAGE:
  Option 1: Run this script directly (requires network access to DB):
    python migrate_health_profiles.py
  
  Option 2 (RECOMMENDED for network issues): 
    Copy the SQL migrations from migration_add_health_columns.sql
    and execute them directly in your PostgreSQL database using psql or pgAdmin
"""
import sys
import os
from pathlib import Path

def migrate_using_sqlalchemy():
    """Try migration using SQLAlchemy (for when psycopg direct connection fails)"""
    try:
        from sqlalchemy import text
        from app.db import SessionLocal
        
        db = SessionLocal()
        try:
            print("Adding missing columns to health_profiles table using SQLAlchemy...")
            
            queries = [
                """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS imc FLOAT NOT NULL DEFAULT 0.0;""",
                """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS score INTEGER NOT NULL DEFAULT 0;""",
                """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS level VARCHAR(100) NOT NULL DEFAULT 'Sin datos';""",
                """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS recommendation VARCHAR(500) NOT NULL DEFAULT 'Por calcular';""",
            ]
            
            for query in queries:
                col_name = query.split('ADD COLUMN')[1].strip().split()[1]
                db.execute(text(query))
                print(f"✓ Column '{col_name}' processed")
            
            db.commit()
            print("\n✓ All columns added successfully!")
            return True
            
        except Exception as e:
            db.rollback()
            print(f"❌ SQLAlchemy migration failed: {e}")
            return False
        finally:
            db.close()
    except ImportError as e:
        print(f"❌ Could not import SQLAlchemy: {e}")
        return False

def migrate_using_psycopg():
    """Try migration using psycopg directly"""
    try:
        import psycopg
        from app.config import DATABASE_URL
        import re
        
        # Parse connection string
        match = re.search(r'postgresql(?:\+psycopg)?://([^:]+):(.+)@([^/]+)/(.+)', DATABASE_URL)
        if not match:
            print(f"❌ Could not parse DATABASE_URL")
            return False
        
        user, password, host, dbname = match.groups()
        
        print(f"Connecting to PostgreSQL database: {dbname}@{host}")
        
        with psycopg.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        ) as conn:
            with conn.cursor() as cur:
                print("Adding missing columns to health_profiles table...")
                
                queries = [
                    """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS imc FLOAT NOT NULL DEFAULT 0.0;""",
                    """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS score INTEGER NOT NULL DEFAULT 0;""",
                    """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS level VARCHAR(100) NOT NULL DEFAULT 'Sin datos';""",
                    """ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS recommendation VARCHAR(500) NOT NULL DEFAULT 'Por calcular';""",
                ]
                
                for query in queries:
                    col_name = query.split('ADD COLUMN')[1].strip().split()[1]
                    cur.execute(query)
                    print(f"✓ Column '{col_name}' processed")
            
            conn.commit()
        
        print("\n✓ All columns added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Psycopg migration failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Health Profiles Table Migration")
    print("=" * 60)
    print()
    
    # Try psycopg first
    if migrate_using_psycopg():
        sys.exit(0)
    
    print("\nTrying alternative method...")
    print()
    
    # Fallback to SQLAlchemy
    if migrate_using_sqlalchemy():
        sys.exit(0)
    
    # If both fail, provide instructions
    print("\n" + "=" * 60)
    print("MIGRATION FAILED - Manual Steps Required")
    print("=" * 60)
    print("""
Please run the following SQL commands manually in your PostgreSQL database:

    ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS imc FLOAT NOT NULL DEFAULT 0.0;
    ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS score INTEGER NOT NULL DEFAULT 0;
    ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS level VARCHAR(100) NOT NULL DEFAULT 'Sin datos';
    ALTER TABLE health_profiles ADD COLUMN IF NOT EXISTS recommendation VARCHAR(500) NOT NULL DEFAULT 'Por calcular';

Or use the provided SQL file:
    migration_add_health_columns.sql

You can execute it using:
    psql -U reactivate_user -h <your-host> -d reactivate -f migration_add_health_columns.sql
""")
    sys.exit(1)

if __name__ == "__main__":
    main()


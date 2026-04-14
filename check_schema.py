"""
Database Schema Checker
Compares the SQLAlchemy model definition with the actual database schema
"""
import sys
from pathlib import Path

def check_health_profile_schema():
    """Check if health_profiles table has all required columns"""
    
    print("=" * 60)
    print("Database Schema Checker - Health Profiles")
    print("=" * 60)
    print()
    
    try:
        from app.db import SessionLocal
        from sqlalchemy import text, inspect
        from app.models.health import HealthProfile
        from app.db import engine
        
        # Get expected columns from model
        inspector = inspect(HealthProfile)
        expected_columns = {col.name: col.type for col in inspector.columns}
        
        print("Expected columns from model:")
        for col_name, col_type in expected_columns.items():
            print(f"  ✓ {col_name}: {col_type}")
        
        print()
        
        # Check actual database schema
        db = SessionLocal()
        try:
            inspector = inspect(engine)
            
            if 'health_profiles' not in inspector.get_table_names():
                print("❌ Table 'health_profiles' does not exist!")
                return False
            
            actual_columns = {col['name']: col['type'] for col in inspector.get_columns('health_profiles')}
            
            print("Actual columns in database:")
            for col_name in sorted(actual_columns.keys()):
                print(f"  ✓ {col_name}: {actual_columns[col_name]}")
            
            print()
            
            # Compare
            missing_columns = set(expected_columns.keys()) - set(actual_columns.keys())
            extra_columns = set(actual_columns.keys()) - set(expected_columns.keys())
            
            if missing_columns:
                print(f"❌ Missing columns ({len(missing_columns)}):")
                for col in sorted(missing_columns):
                    print(f"  - {col}: {expected_columns[col]}")
                print()
                return False
            
            if extra_columns:
                print(f"⚠️  Extra columns in database ({len(extra_columns)}):")
                for col in sorted(extra_columns):
                    print(f"  - {col}")
                print()
            
            print("✓ All expected columns are present!")
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        print()
        print("Make sure you have:")
        print("  1. Set the DATABASE_URL environment variable")
        print("  2. Have network access to the PostgreSQL server")
        print("  3. Installed all required dependencies")
        return False

if __name__ == "__main__":
    success = check_health_profile_schema()
    
    if not success:
        print()
        print("To fix the missing columns, run:")
        print("  python migrate_health_profiles.py")
        print()
        print("Or see MIGRATION_GUIDE.md for manual SQL steps.")
        sys.exit(1)
    else:
        print()
        print("Schema check passed! Your database is correctly configured.")
        sys.exit(0)

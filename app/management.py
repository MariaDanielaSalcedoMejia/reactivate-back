"""
Management: Health Profile Schema Migration
This creates a temporary migration endpoint that runs the schema updates
Run this once on Render to add missing columns to health_profiles table
"""

from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import text
from app.db import SessionLocal

router = APIRouter(prefix="/management", tags=["management"])

ADMIN_SECRET = "health-migration-2024"

@router.post("/migrate-health-profiles")
async def migrate_health_profiles(x_admin_secret: str = Header(None)):
    """
    Migrate health_profiles table - add missing columns
    Requires admin secret header for security
    
    Usage: POST /management/migrate-health-profiles with header X-Admin-Secret
    """
    
    # Security check
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    db = SessionLocal()
    try:
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

        -- Update existing rows with calculated IMC
        UPDATE health_profiles 
        SET 
          imc = ROUND(weight_kg / POWER(height_cm / 100.0, 2), 2),
          score = 50,
          level = 'Por recalcular',
          recommendation = 'Actualizar valores en el sistema'
        WHERE imc = 0 OR score = 0;
        """
        
        # Execute migration
        statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
        
        for statement in statements:
            db.execute(text(statement))
        
        db.commit()
        
        # Verify
        result = db.execute(text("""
            SELECT id, user_id, height_cm, weight_kg, resting_hr, imc, score, level, recommendation
            FROM health_profiles
            LIMIT 5
        """)).fetchall()
        
        return {
            "status": "success",
            "message": "Health profiles migration completed",
            "rows_checked": len(result),
            "sample_data": [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "height_cm": row[2],
                    "weight_kg": row[3],
                    "resting_hr": row[4],
                    "imc": row[5],
                    "score": row[6],
                    "level": row[7],
                    "recommendation": row[8]
                }
                for row in result
            ]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")
    finally:
        db.close()

@router.get("/health-schema-check")
async def check_health_schema(x_admin_secret: str = Header(None)):
    """Check current health_profiles table schema"""
    
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    db = SessionLocal()
    try:
        # Get table schema information
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'health_profiles'
            ORDER BY ordinal_position
        """)).fetchall()
        
        return {
            "status": "success",
            "table": "health_profiles",
            "columns": [
                {
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2],
                    "default": row[3]
                }
                for row in result
            ]
        }
    finally:
        db.close()

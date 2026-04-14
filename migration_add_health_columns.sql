-- Migration: Add missing columns to health_profiles table
-- This script adds the columns that the model expects but the database is missing

-- Add individual columns with IF NOT EXISTS to prevent errors if they already exist
ALTER TABLE health_profiles 
ADD COLUMN IF NOT EXISTS imc FLOAT NOT NULL DEFAULT 0.0;

ALTER TABLE health_profiles 
ADD COLUMN IF NOT EXISTS score INTEGER NOT NULL DEFAULT 0;

ALTER TABLE health_profiles 
ADD COLUMN IF NOT EXISTS level VARCHAR(100) NOT NULL DEFAULT 'Sin datos';

ALTER TABLE health_profiles 
ADD COLUMN IF NOT EXISTS recommendation VARCHAR(500) NOT NULL DEFAULT 'Por calcular';

-- Update existing rows with calculated values (optional, for better initial data)
-- This assumes you want to recalculate these based on height_cm and weight_kg
UPDATE health_profiles 
SET 
  imc = ROUND(weight_kg / POWER(height_cm / 100.0, 2), 2),
  score = 50,
  level = 'Por recalcular',
  recommendation = 'Actualizar valores en el sistema'
WHERE imc = 0 OR score = 0;

-- Verify the migration
SELECT id, user_id, height_cm, weight_kg, resting_hr, imc, score, level, recommendation
FROM health_profiles
LIMIT 5;

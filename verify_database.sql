-- 🔍 SCRIPT DE VERIFICACIÓN - BASE DE DATOS

-- ==================================================
-- 1. VERIFICAR USUARIOS
-- ==================================================
SELECT 'USUARIOS' as "📋 TABLA";
SELECT id, email, name, age, created_at FROM users;

-- ==================================================
-- 2. VERIFICAR PERFILES DE SALUD
-- ==================================================
SELECT 'PERFILES DE SALUD' as "📋 TABLA";
SELECT id, user_id, height_cm, weight_kg, resting_hr, imc, score, level, created_at FROM health_profiles;

-- ==================================================
-- 3. VERIFICAR ANÁLISIS HISTÓRICOS
-- ==================================================
SELECT 'ANÁLISIS DE SALUD (HISTORIAL)' as "📋 TABLA";
SELECT id, user_id, imc, score, level, created_at FROM health_analysis
LIMIT 10;  -- Solo últimos 10

-- ==================================================
-- 4. CONTAR REGISTROS POR TABLA
-- ==================================================
SELECT 'RESUMEN' as "📊 ESTADÍSTICAS";
SELECT 
  (SELECT COUNT(*) FROM users) as "Usuarios",
  (SELECT COUNT(*) FROM health_profiles) as "Perfiles de Salud",
  (SELECT COUNT(*) FROM health_analysis) as "Análisis Históricos";

-- ==================================================
-- 5. VERIFICAR RELACIONES (User - HealthProfile)
-- ==================================================
SELECT 'RELACIONES' as "🔗 INTEGRIDAD";
SELECT 
  u.id,
  u.email,
  COALESCE(COUNT(h.id), 0) as "Perfiles Vinculados"
FROM users u
LEFT JOIN health_profiles h ON u.id = h.user_id
GROUP BY u.id, u.email;

-- ==================================================
-- 6. MOSTRAR ÚLTIMAS ACTUALIZACIONES
-- ==================================================
SELECT 'ÚLTIMAS ACTUALIZACIONES' as "⏰ RECIENTES";
SELECT 'Usuarios' as tabla, MAX(created_at) as última_fecha FROM users
UNION ALL
SELECT 'Salud', MAX(created_at) FROM health_profiles
UNION ALL
SELECT 'Análisis', MAX(created_at) FROM health_analysis;

-- ==================================================
-- 7 QUERY ÚTIL: Ver datos completos de un usuario
-- ==================================================
-- Descomenta y reemplaza USER_ID con el ID del usuario
-- SELECT 
--   u.id, u.email, u.name,
--   h.height_cm, h.weight_kg, h.resting_hr, h.imc, h.score, h.level,
--   h.created_at as salud_creada,
--   h.updated_at as salud_actualizada
-- FROM users u
-- LEFT JOIN health_profiles h ON u.id = h.user_id
-- WHERE u.id = 1;  -- ← CAMBIAR A USER_ID

-- ==================================================
-- INSTRUCCIONES PARA EJECUTAR:
-- ==================================================
-- 
-- SQLITE:
--   1. sqlite3 back pro/app/database.db
--   2. Copiar y pegar este script
--   3. Ver resultados
--
-- POSTGRESQL:
--   1. psql -U user -d reactivate -h localhost
--   2. Copiar y pegar este script
--   3. Ver resultados
--
-- ==================================================

# INSTRUCCIONES: Ejecutar Migración en Render

## Estado Actual
✅ Código: Todos los cambios de transacciones están en git (9 archivos modificados)
✅ Base de datos: Activa en Render (PostgreSQL 18, Oregon)
⏳ Schema: Esperando migración (falta agregar 4 columnas)

## Pasos para Completar (Python 3.11.8 en Render)

### 1. Verificar Deploy
Después que Render detecte y reconstruya código:
```
https://reactivate-api-backend.onrender.com/api/healthcheck
```
Debe mostrar: `{"status": "ok", "database": "connected"}`

### 2. Ejecutar Migración
Una vez que el sistema esté listo, ejecutar:

```bash
curl -X POST https://reactivate-api-backend.onrender.com/management/migrate-health-profiles \
  -H "X-Admin-Secret: health-migration-2024" \
  -H "Content-Type: application/json"
```

**Respuesta esperada:**
```json
{
  "status": "success",
  "message": "Health profiles migration completed",
  "rows_checked": 5,
  "sample_data": [
    {
      "id": 1,
      "user_id": 123,
      "height_cm": 175,
      "weight_kg": 75,
      "resting_hr": 60,
      "imc": 24.49,
      "score": 50,
      "level": "Por recalcular",
      "recommendation": "Actualizar valores en el sistema"
    }
  ]
}
```

### 3. Verificar Schema (Opcional)
```bash
curl -X GET https://reactivate-api-backend.onrender.com/management/health-schema-check \
  -H "X-Admin-Secret: health-migration-2024"
```

Debe mostrar todas las columnas incluyendo: `imc`, `score`, `level`, `recommendation`

## Columnas Agregadas

| Columna | Tipo | Default | Propósito |
|---------|------|---------|-----------|
| imc | FLOAT | 0.0 | Índice de Masa Corporal |
| score | INTEGER | 0 | Puntuación de salud |
| level | VARCHAR(100) | 'Sin datos' | Nivel de salud |
| recommendation | VARCHAR(500) | 'Por calcular' | Recomendación personalizada |

## Rollback (Si algo falla)
Si la migración falla, la transacción se revierte automáticamente:
```bash
# Verificar estado actual
curl -X GET https://reactivate-api-backend.onrender.com/management/health-schema-check \
  -H "X-Admin-Secret: health-migration-2024"
```

## En Local (Desarrollo)
Este proyecto tiene Python 3.11.8 en Render. Para probar localmente:

```bash
# Activar venv con Python 3.11+
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migración local
python migrate_simple.py
```

## Seguridad
⚠️ El header `X-Admin-Secret` es requerido para:
- POST /management/migrate-health-profiles
- GET /management/health-schema-check

Secret actual: `health-migration-2024`

**IMPORTANTE**: Cambiar este secret en producción después de migración.

## Timeline
- ✅ Código: Listo (f067e2f en main)
- ⏳ Render Deploy: ~2-5 mins
- ⏳ Migración: ~1-2 segundos
- ✅ Sistema listo para usar

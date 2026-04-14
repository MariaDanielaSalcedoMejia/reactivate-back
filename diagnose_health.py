#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT DE DIAGNÓSTICO - Health Data

Este script verifica:
1. Si la BD está inicializada correctamente
2. Si hay usuarios registrados
3. Si los datos se pueden guardar
4. Si hay errores en las rutas
"""

import sys
sys.path.append('.')

from app.db import SessionLocal, init_db
from app.models.user import User
from app.models.health import HealthProfile
from app.services.health_service import HealthService

print("=" * 60)
print("🔍 DIAGNÓSTICO DE SALUD - ReActivate Pro")
print("=" * 60)

# 1. Inicializar BD
print("\n1️⃣  INICIALIZANDO BASE DE DATOS...")
try:
    init_db()
    print("   ✅ Base de datos inicializada")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 2. Verificar usuarios
print("\n2️⃣  BUSCANDO USUARIOS REGISTRADOS...")
db = SessionLocal()
try:
    users = db.query(User).all()
    if users:
        print(f"   ✅ Usuarios encontrados: {len(users)}")
        for user in users:
            print(f"      • ID: {user.id} | Email: {user.email} | Nombre: {user.name}")
    else:
        print("   ⚠️  No hay usuarios registrados aún")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Ver perfiles de salud existentes
print("\n3️⃣  BUSCANDO PERFILES DE SALUD...")
try:
    profiles = db.query(HealthProfile).all()
    if profiles:
        print(f"   ✅ Perfiles de salud encontrados: {len(profiles)}")
        for profile in profiles:
            print(f"      • User ID: {profile.user_id} | IMC: {profile.imc} | Score: {profile.score}")
    else:
        print("   ⚠️  No hay perfiles de salud registrados")
        print("      → Este es el problema que ves en la screenshot")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Prueba de guardado
print("\n4️⃣  PROBANDO GUARDADO DE DATOS...")
if users:
    test_user = users[0]
    print(f"   Usando usuario: {test_user.email} (ID: {test_user.id})")
    
    try:
        # Intentar guardar un perfil
        profile = HealthService.create_or_update_profile(
            db,
            user_id=test_user.id,
            height_cm=175,
            weight_kg=75,
            resting_hr=70,
            age=35
        )
        print(f"   ✅ Perfil guardado exitosamente!")
        print(f"      • IMC: {profile.imc}")
        print(f"      • Score: {profile.score}")
        print(f"      • Level: {profile.level}")
    except Exception as e:
        print(f"   ❌ Error al guardar: {e}")
else:
    print("   ⚠️  No hay usuarios para probar")
    print("   → Necesitas registrar un usuario primero en la aplicación")

# 5. Verificar integridad de relaciones
print("\n5️⃣  VERIFICANDO INTEGRIDAD DE BASE DE DATOS...")
try:
    db.execute("SELECT 1")
    print("   ✅ Conexión a BD OK")
except Exception as e:
    print(f"   ❌ Error en conexión: {e}")

db.close()

# 6. Resumen
print("\n" + "=" * 60)
print("📋 RESUMEN Y RECOMENDACIONES:")
print("=" * 60)

print("""
Si ves perfiles vacíos en la tabla:

OPCIÓN 1: Los datos NO se están guardando
  → Verifica que el componente salga SIN ERRORES en F12 Console
  → Verifica que el backend logee el POST request
  → Prueba manualmente: curl -X POST http://localhost:8000/api/health/1 -d {...}

OPCIÓN 2: Estás usando un user_id que NO existe
  → Registrate primero en la app (/register)
  → Luego intenta guardar datos de salud
  → El user_id debe coincidir con el que registraste

OPCIÓN 3: Hay restricción UNIQUE en user_id
  → Model tiene: user_id = Column(..., unique=True)
  → Significa: Solo UN perfil por usuario
  → Si ya existe uno, se actualiza (no crea nuevo)

PRÓXIMOS PASOS:
  1. Abre F12 en el navegador
  2. Ve a Network tab
  3. Llena el form de health y clickea "Analizar"
  4. Busca request a /api/health/...
  5. ¿Es POST? ¿Cuál es el response?
  6. Manda los detalles si hay ERROR
""")

print("=" * 60)
print("✅ Diagnóstico completado")
print("=" * 60)

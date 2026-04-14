"""
Script de prueba para verificar si los datos de health se guardan correctamente
"""
import sys
import sqlite3
from datetime import datetime
from app.db import get_db, SESSION_LOCAL, init_db
from app.models.user import User
from app.models.health import HealthProfile
from app.models.health_analysis import HealthAnalysis
from app.services.health_service import HealthService
from app.repositories.health_repository import HealthRepository
from app.repositories.health_analysis_repository import HealthAnalysisRepository

def test_health_save():
    print("\n" + "="*60)
    print("🔍 TEST: Guardar datos de health")
    print("="*60)
    
    # Inicializar BD
    init_db()
    print("✅ Base de datos inicializada")
    
    # Crear sesión
    db = SESSION_LOCAL()
    
    try:
        # 1. Verificar usuarios
        users = db.query(User).all()
        print(f"\n📊 Total de usuarios: {len(users)}")
        if users:
            for user in users[:3]:
                print(f"   - {user.id}: {user.name} ({user.email})")
        else:
            print("   ⚠️ No hay usuarios. Creando usuario de prueba...")
            test_user = User(
                name="Test User",
                email="test@test.com",
                password_hash="fake_hash"
            )
            db.add(test_user)
            db.commit()
            user_id = test_user.id
            print(f"   ✅ Usuario creado: {user_id}")
        
        if users:
            user_id = users[0].id
        
        # 2. Verificar health_profiles antes
        print(f"\n📋 Health profiles ANTES:")
        counter_before = db.query(HealthProfile).count()
        print(f"   Total: {counter_before}")
        
        # 3. Intentar guardar un profile
        print(f"\n💾 Intentando guardar profile para user_id={user_id}...")
        try:
            profile = HealthService.create_or_update_profile(
                db,
                user_id=user_id,
                height_cm=175.5,
                weight_kg=70.0,
                resting_hr=65,
                age=30
            )
            print(f"✅ Profile guardado:")
            print(f"   - ID: {profile.id}")
            print(f"   - IMC: {profile.imc}")
            print(f"   - Score: {profile.score}")
            print(f"   - Level: {profile.level}")
        except Exception as e:
            print(f"❌ Error guardando profile: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # 4. Verificar health_profiles después
        print(f"\n📋 Health profiles DESPUÉS:")
        counter_after = db.query(HealthProfile).count()
        print(f"   Total: {counter_after}")
        if counter_after > counter_before:
            print(f"   ✅ Se agregó 1 registro (+{counter_after - counter_before})")
        else:
            print(f"   ⚠️ No se agregó ningún registro")
        
        # 5. Verificar health_analysis
        print(f"\n📈 Health analysis (historial):")
        analysis_count = db.query(HealthAnalysis).filter(HealthAnalysis.user_id == user_id).count()
        print(f"   Total para este usuario: {analysis_count}")
        if analysis_count > 0:
            latest = db.query(HealthAnalysis).filter(HealthAnalysis.user_id == user_id).order_by(HealthAnalysis.created_at.desc()).first()
            print(f"   Último análisis:")
            print(f"   - Score: {latest.score}")
            print(f"   - Resumen: {latest.health_summary[:50] if latest.health_summary else 'N/A'}...")
        
        print("\n✅ TEST COMPLETADO CORRECTAMENTE")
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_health_save()

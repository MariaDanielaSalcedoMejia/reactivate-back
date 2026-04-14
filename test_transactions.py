"""
Comprehensive test for transaction management and health profile saving
Tests the complete flow with proper transaction handling
"""
import sys
from datetime import date
from app.db import SessionLocal, init_db
from app.models.user import User
from app.models.health import HealthProfile
from app.models.health_analysis import HealthAnalysis
from app.services.health_service import HealthService
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository

def test_transaction_management():
    """Test complete transaction flow"""
    print("\n" + "=" * 70)
    print("🔍 TEST: Complete Transaction Management for Health Profiles")
    print("=" * 70)
    
    # Initialize database
    print("\n1️⃣  Initializing database...")
    init_db()
    print("   ✅ Database initialized\n")
    
    db = SessionLocal()
    
    try:
        # TEST 1: Create user
        print("2️⃣  Creating test user...")
        try:
            # Check if user exists
            existing_user = UserRepository.get_by_email(db, "healthtest@test.com")
            if existing_user:
                user_id = existing_user.id
                print(f"   → User already exists: {user_id}")
            else:
                user = AuthService.register(
                    db,
                    name="Test User",
                    email="healthtest@test.com",
                    password="password123",
                    birth_date=date(1990, 5, 15)
                )
                # Explicit commit since UserRepository.create() only flushes
                db.commit()
                user_id = user.id
                print(f"   ✅ User created: {user_id}")
        except Exception as e:
            db.rollback()
            print(f"   ❌ Error creating user: {e}")
            raise
        
        # TEST 2: Save health profile - TRANSACTIONAL TEST
        print(f"\n3️⃣  Saving health profile for user {user_id}...")
        print("   📋 Before save:")
        count_before = db.query(HealthProfile).count()
        analysis_before = db.query(HealthAnalysis).count()
        print(f"      - Health profiles: {count_before}")
        print(f"      - Health analyses: {analysis_before}")
        
        try:
            # This should be atomic - either both are created or nothing
            profile = HealthService.create_or_update_profile(
                db,
                user_id=user_id,
                height_cm=175.5,
                weight_kg=70.0,
                resting_hr=65,
                age=34
            )
            
            # This is the critical point - explicit commit
            print("   💾 Committing transaction...")
            db.commit()
            print("   ✅ Transaction committed successfully")
            
            # Refresh to get latest data from DB
            db.refresh(profile)
            
        except Exception as e:
            db.rollback()
            print(f"   ❌ Error saving profile: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # TEST 3: Verify data integrity
        print(f"\n4️⃣  Verifying data integrity...")
        print("   📋 After save:")
        count_after = db.query(HealthProfile).count()
        analysis_after = db.query(HealthAnalysis).count()
        print(f"      - Health profiles: {count_after}")
        print(f"      - Health analyses: {analysis_after}")
        
        if count_after > count_before:
            print(f"   ✅ Profile saved (+{count_after - count_before})")
        else:
            print(f"   ❌ Profile was not saved!")
            return False
        
        if analysis_after > analysis_before:
            print(f"   ✅ Analysis saved (+{analysis_after - analysis_before})")
        else:
            print(f"   ❌ Analysis was not saved!")
            return False
        
        # TEST 4: Verify profile data
        print(f"\n5️⃣  Verifying profile data...")
        saved_profile = db.query(HealthProfile).filter(
            HealthProfile.user_id == user_id
        ).first()
        
        if not saved_profile:
            print(f"   ❌ Profile not found in database!")
            return False
        
        print(f"   ✅ Profile data:")
        print(f"      - ID: {saved_profile.id}")
        print(f"      - Height: {saved_profile.height_cm} cm")
        print(f"      - Weight: {saved_profile.weight_kg} kg")
        print(f"      - Resting HR: {saved_profile.resting_hr} bpm")
        print(f"      - BMI: {saved_profile.imc}")
        print(f"      - Score: {saved_profile.score}")
        print(f"      - Level: {saved_profile.level}")
        print(f"      - Recommendation: {saved_profile.recommendation[:50]}...")
        
        # TEST 5: Verify analysis data
        print(f"\n6️⃣  Verifying analysis data...")
        latest_analysis = db.query(HealthAnalysis).filter(
            HealthAnalysis.user_id == user_id
        ).order_by(HealthAnalysis.created_at.desc()).first()
        
        if not latest_analysis:
            print(f"   ❌ Analysis not found in database!")
            return False
        
        print(f"   ✅ Analysis data:")
        print(f"      - ID: {latest_analysis.id}")
        print(f"      - IMC: {latest_analysis.imc}")
        print(f"      - IMC Category: {latest_analysis.imc_category}")
        print(f"      - Score: {latest_analysis.score}")
        print(f"      - Level: {latest_analysis.level}")
        print(f"      - Max HR: {latest_analysis.max_hr}")
        print(f"      - Heart Reserve: {latest_analysis.heart_reserve}")
        print(f"      - Summary: {latest_analysis.health_summary.split(chr(10))[0] if latest_analysis.health_summary else 'N/A'}...")
        
        # TEST 6: Update test
        print(f"\n7️⃣  Testing update transaction...")
        try:
            updated_profile = HealthService.create_or_update_profile(
                db,
                user_id=user_id,
                height_cm=176.0,
                weight_kg=71.5,
                resting_hr=60,
                age=34
            )
            db.commit()
            db.refresh(updated_profile)
            
            print(f"   ✅ Profile updated successfully")
            print(f"      - New weight: {updated_profile.weight_kg} kg")
            print(f"      - New HR: {updated_profile.resting_hr} bpm")
            
            # Verify new analysis was created
            analyses = db.query(HealthAnalysis).filter(
                HealthAnalysis.user_id == user_id
            ).order_by(HealthAnalysis.created_at.desc()).all()
            
            print(f"      - Total analyses now: {len(analyses)}")
            if len(analyses) >= 2:
                print(f"   ✅ New analysis was created for the update")
            
        except Exception as e:
            db.rollback()
            print(f"   ❌ Error updating profile: {e}")
            raise
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED - TRANSACTION MANAGEMENT IS WORKING CORRECTLY")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
        print()

if __name__ == "__main__":
    success = test_transaction_management()
    sys.exit(0 if success else 1)

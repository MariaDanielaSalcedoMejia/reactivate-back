"""
Script para inicializar datos de prueba en la base de datos
Ejecutar: python init_data.py
"""
from datetime import date
from app.db import SessionLocal, init_db
from app.models import Base
from app.repositories.user_repository import UserRepository
from app.repositories.blog_repository import BlogRepository
from app.repositories.exercise_repository import ExerciseRepository
from app.repositories.park_repository import ParkRepository
from app.repositories.forum_repository import ForumRepository
from app.repositories.health_repository import HealthRepository
from app.services.auth_service import AuthService
from app.db import engine

def initialize_data():
    """Inicializa la base de datos con datos de prueba"""
    
    # Crear todas las tablas
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente\n")
    
    db = SessionLocal()
    
    try:
        # 🔹 CREAR USUARIOS DE PRUEBA
        print("Creando usuarios de prueba...")
        users = []
        user_data = [
            ("Juan García", "juan@example.com", "password123", date(1990, 5, 15)),
            ("María López", "maria@example.com", "password123", date(1992, 8, 22)),
            ("Carlos Rodríguez", "carlos@example.com", "password123", date(1988, 3, 10)),
            ("Ana Martínez", "ana@example.com", "password123", date(1995, 12, 1)),
        ]
        
        for name, email, password, birth_date in user_data:
            existing = UserRepository.get_by_email(db, email)
            if not existing:
                user = AuthService.register(db, name, email, password, birth_date)
                users.append(user)
                print(f"  ✓ Usuario creado: {name}")
            else:
                users.append(existing)
                print(f"  → Usuario ya existe: {name}")
        
        print()
        
        # 🔹 CREAR POSTS DE BLOG
        print("Creando posts de blog...")
        blog_posts = [
            ("Importancia del ejercicio regular", "Texto contenido...", "juan@example.com"),
            ("Nutrición para deportistas", "El ejercicio es parte importante...", "maria@example.com"),
            ("Recuperación muscular efectiva", "Después de entrenar es crucial...", "carlos@example.com"),
        ]
        
        for title, content, author_email in blog_posts:
            posts = db.query(BlogRepository.__mapper__.entity).filter_by(title=title).first()
            if not posts:
                BlogRepository.create_post(db, title, content, 
                    UserRepository.get_by_email(db, author_email).id)
                print(f"  ✓ Post creado: {title}")
            else:
                print(f"  → Post ya existe: {title}")
        
        print()
        
        # 🔹 CREAR EJERCICIOS
        print("Creando ejercicios...")
        exercises = [
            ("Flexiones", "Cardio", "Ejercicio de resistencia corporal", "www.example.com/flexiones.jpg"),
            ("Sentadillas", "Fuerza", "Ejercicio para piernas", "www.example.com/sentadillas.jpg"),
            ("Flexiones de brazos", "Fuerza", "Fortalecimiento de brazos y pecho", "www.example.com/flexiones_brazos.jpg"),
            ("Saltos", "Cardio", "Ejercicio de saltos repetidos", "www.example.com/saltos.jpg"),
            ("Correr", "Cardio", "Trote y running", "www.example.com/correr.jpg"),
        ]
        
        created_exercises = []
        for name, tipo, desc, img in exercises:
            existing = db.query(ExerciseRepository.__mapper__.entity).filter_by(name=name).first()
            if not existing:
                ex = ExerciseRepository.create_exercise(db, name, tipo, desc, img)
                created_exercises.append(ex)
                print(f"  ✓ Ejercicio creado: {name}")
            else:
                print(f"  → Ejercicio ya existe: {name}")
                created_exercises.append(existing)
        
        print()
        
        # 🔹 CREAR PARQUES
        print("Creando parques...")
        parks_data = [
            ("Parque Central", "Calle Principal 123, Ciudad", 4.5),
            ("Parque Metropolitano", "Avenida Reforma 456, Ciudad", 4.7),
            ("Parque Rosa", "Calle Rosa 789, Ciudad", 4.3),
            ("Parque Ecológico", "Carretera Sur km 5, Ciudad", 4.6),
        ]
        
        created_parks = []
        for name, address, rating in parks_data:
            existing = db.query(ParkRepository.__mapper__.entity).filter_by(name=name).first()
            if not existing:
                park = ParkRepository.create_park(db, name, address, rating)
                created_parks.append(park)
                print(f"  ✓ Parque creado: {name}")
            else:
                print(f"  → Parque ya existe: {name}")
                created_parks.append(existing)
        
        print()
        
        # 🔹 CREAR CATEGORÍAS DE FORO
        print("Creando categorías de foro...")
        categories = [
            ("Rutinas de Ejercicio", "Comparte tus rutinas y obtén sugerencias", "💪"),
            ("Nutrición", "Discusiones sobre dieta y nutrición", "🥗"),
            ("Recuperación", "Consejos sobre recuperación y descanso", "😴"),
            ("General", "Tema general de discusión", "💬"),
        ]
        
        for name, desc, icon in categories:
            existing = ForumRepository.get_category_by_name(db, name)
            if not existing:
                ForumRepository.create_category(db, name, desc, icon)
                print(f"  ✓ Categoría creada: {name}")
            else:
                print(f"  → Categoría ya existe: {name}")
        
        print()
        
        # 🔹 CREAR POSTS DE FORO
        print("Creando posts de foro...")
        forum_posts = [
            ("¿Cuál es la mejor rutina para principiantes?", "Soy nuevo en esto...", "juan@example.com", "Rutinas de Ejercicio"),
            ("Suplementos recomendados", "¿Qué suplementos usáis?", "maria@example.com", "Nutrición"),
            ("Dolor muscular después del ejercicio", "¿Es normal?", "carlos@example.com", "Recuperación"),
        ]
        
        for title, excerpt, author, category_name in forum_posts:
            existing = db.query(ForumRepository.__mapper__.entity).filter_by(title=title).first()
            if not existing:
                category = ForumRepository.get_category_by_name(db, category_name)
                author_obj = UserRepository.get_by_email(db, author)
                
                ForumRepository.create_post(db, title, f"Contenido completo de: {excerpt}", 
                    excerpt, author_obj.id if author_obj else None, category.id)
                print(f"  ✓ Post de foro creado: {title}")
            else:
                print(f"  → Post de foro ya existe: {title}")
        
        print()
        
        # 🔹 CREAR PERFILES DE SALUD
        print("Creando perfiles de salud...")
        health_profiles = [
            (1, 175, 75, 65),
            (2, 160, 62, 72),
            (3, 180, 85, 68),
        ]
        
        for user_id, height, weight, resting_hr in health_profiles:
            existing = HealthRepository.get_by_user(db, user_id)
            if not existing:
                # Calcular métricas
                height_m = height / 100.0
                imc = weight / (height_m * height_m)
                score = 100
                
                if imc < 18.5 or imc > 30:
                    score -= 30
                elif imc > 25:
                    score -= 15
                
                if resting_hr > 80:
                    score -= 30
                elif resting_hr > 70:
                    score -= 15
                
                score = max(0, score)
                
                if score >= 85:
                    level = 'Atleta 🔥'
                    rec = 'Estás en un nivel excelente.'
                elif score >= 70:
                    level = 'Buen nivel 💪'
                    rec = 'Buen estado físico.'
                elif score >= 50:
                    level = 'Mejorable ⚡'
                    rec = 'Necesitas mejorar resistencia.'
                else:
                    level = 'Bajo rendimiento ⚠️'
                    rec = 'Enfócate en hábitos básicos.'
                
                HealthRepository.create_or_update(db, user_id, height, weight, 
                    resting_hr, round(imc, 2), score, level, rec)
                print(f"  ✓ Perfil de salud creado para usuario {user_id}")
            else:
                print(f"  → Perfil de salud ya existe para usuario {user_id}")
        
        print()
        print("=" * 50)
        print("✅ Datos iniciales cargados exitosamente!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error al inicializar: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    initialize_data()

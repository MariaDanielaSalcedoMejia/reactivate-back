"""
Script de prueba de la API
Ejecutar: python test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_healthcheck():
    print_section("🏥 Health Check")
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/api/healthcheck")
        print(f"✓ Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_auth():
    print_section("👤 Autenticación")
    
    # Registrar usuario
    print("1. Registrando usuario...")
    register_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "birth_date": "1990-01-01"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Usuario registrado")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Login
    print("\n2. Iniciando sesión...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Login exitoso")
    else:
        print(f"   ✗ Error: {response.text}")

def test_blog():
    print_section("📝 Blog")
    
    # Crear post
    print("1. Creando post...")
    post_data = {
        "title": "Mi Primer Post",
        "content": "Este es el contenido del post de prueba",
        "author_email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/blog/posts", json=post_data)
    print(f"   Status: {response.status_code}")
    
    # Listar posts
    print("\n2. Listando posts...")
    response = requests.get(f"{BASE_URL}/blog/posts")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        posts = response.json()
        print(f"   ✓ Total posts: {len(posts)}")

def test_health():
    print_section("❤️ Salud")
    
    # Crear perfil
    print("1. Creando perfil de salud para usuario 1...")
    health_data = {
        "height_cm": 175,
        "weight_kg": 75,
        "resting_hr": 65
    }
    response = requests.post(f"{BASE_URL}/health/1", json=health_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Perfil creado")
        print(f"   - IMC: {data.get('imc')}")
        print(f"   - Score: {data.get('score')}")
        print(f"   - Nivel: {data.get('level')}")
    
    # Obtener perfil
    print("\n2. Obteniendo perfil de salud...")
    response = requests.get(f"{BASE_URL}/health/1")
    print(f"   Status: {response.status_code}")

def test_exercises():
    print_section("💪 Ejercicios")
    
    # Crear ejercicio
    print("1. Creando ejercicio...")
    exercise_data = {
        "nombre": "Flexiones de Prueba",
        "tipo": "Cardio",
        "descripcion": "Ejercicio de prueba",
        "imagen": "url_test"
    }
    response = requests.post(f"{BASE_URL}/exercises", json=exercise_data)
    print(f"   Status: {response.status_code}")
    
    # Listar ejercicios
    print("\n2. Listando ejercicios...")
    response = requests.get(f"{BASE_URL}/exercises")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        exercises = response.json()
        print(f"   ✓ Total ejercicios: {len(exercises)}")

def test_parks():
    print_section("🏞️ Parques")
    
    # Crear parque
    print("1. Creando parque...")
    park_data = {
        "name": "Parque Test",
        "address": "Calle Test 123",
        "rating": 4.5
    }
    response = requests.post(f"{BASE_URL}/parks", json=park_data)
    print(f"   Status: {response.status_code}")
    
    # Listar parques
    print("\n2. Listando parques...")
    response = requests.get(f"{BASE_URL}/parks")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        parks = response.json()
        print(f"   ✓ Total parques: {len(parks)}")

def test_forum():
    print_section("💬 Foro")
    
    # Listar categorías
    print("1. Listando categorías del foro...")
    response = requests.get(f"{BASE_URL}/forum/categories")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()
        print(f"   ✓ Total categorías: {len(categories)}")
    
    # Listar posts
    print("\n2. Listando posts del foro...")
    response = requests.get(f"{BASE_URL}/forum/posts")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        posts = response.json()
        print(f"   ✓ Total posts: {len(posts)}")

def main():
    print("\n" + "🚀 " * 20)
    print("PRUEBA DE API - ReActivate Pro")
    print("🚀 " * 20)
    
    try:
        test_healthcheck()
        test_auth()
        test_blog()
        test_health()
        test_exercises()
        test_parks()
        test_forum()
        
        print_section("✅ PRUEBAS COMPLETADAS")
        
    except Exception as e:
        print(f"\n✗ Error general: {e}")
        print("\n💡 Asegúrate de que el servidor está ejecutándose en http://localhost:8000")

if __name__ == "__main__":
    main()

# API ReActivate Pro - Documentación (v1.1)

## 📋 Resumen de Endpoints

### 👤 Autenticación (`/api/auth`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/register` | Registra un nuevo usuario |
| POST | `/login` | Inicia sesión con email y contraseña |
| GET | `/me?email=...` | Obtiene datos del usuario autenticado |
| GET | `/user/{user_id}` | Obtiene datos de un usuario específico |

### 📝 Blog (`/api/blog`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/posts` | Lista todos los posts |
| POST | `/posts` | Crea un nuevo post |
| GET | `/posts/{post_id}` | Obtiene un post específico |
| PUT | `/posts/{post_id}` | Actualiza un post |
| DELETE | `/posts/{post_id}` | Elimina un post |

### 💪 Ejercicios (`/api/exercises`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Lista todos los ejercicios |
| POST | `/` | Crea un nuevo ejercicio |
| GET | `/{exercise_id}` | Obtiene un ejercicio específico |
| PUT | `/{exercise_id}` | Actualiza un ejercicio |
| DELETE | `/{exercise_id}` | Elimina un ejercicio |

### 🏞️ Parques (`/api/parks`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Lista todos los parques |
| POST | `/` | Crea un nuevo parque |
| GET | `/{park_id}` | Obtiene un parque específico |
| PUT | `/{park_id}` | Actualiza un parque |
| DELETE | `/{park_id}` | Elimina un parque |

### 💬 Foro (`/api/forum`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/categories` | Lista todas las categorías |
| POST | `/categories` | Crea una nueva categoría |
| GET | `/posts` | Lista todos los posts del foro |
| POST | `/posts` | Crea un nuevo post en el foro |
| GET | `/posts/{post_id}` | Obtiene un post específico |
| DELETE | `/posts/{post_id}` | Elimina un post |

### ❤️ Salud (`/api/health`) - **NUEVO CON HISTORIAL**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/{user_id}` | Crea o actualiza el perfil de salud (guarda en historial) |
| GET | `/{user_id}` | Obtiene el perfil de salud actual |
| GET | `/{user_id}/history` | **Obtiene el historial completo de análisis** |
| GET | `/{user_id}/history-summary` | **Obtiene resumen del historial (para gráficas)** |
| GET | `/analysis/{analysis_id}` | **Obtiene detalles de un análisis específico** |
| DELETE | `/{user_id}` | Elimina el perfil de salud |

### 🏥 Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/healthcheck` | Verifica el estado del servidor y BD |

---

## 📦 Modelos de Datos

### Usuario
```json
{
  "id": 1,
  "name": "Juan García",
  "email": "juan@example.com",
  "birth_date": "1990-05-15",
  "role": "user",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Perfil de Salud (Actual)
```json
{
  "user_id": 1,
  "height_cm": 175,
  "weight_kg": 75,
  "resting_hr": 65,
  "imc": 24.49,
  "score": 85,
  "level": "Atleta 🔥",
  "recommendation": "Estás en un nivel excelente..."
}
```

### Análisis de Salud (Historial) - **NUEVO**
```json
{
  "id": 1,
  "user_id": 1,
  "height_cm": 175,
  "weight_kg": 75,
  "resting_hr": 65,
  "age": 34,
  "imc": 24.49,
  "imc_category": "Óptimo",
  "score": 85,
  "level": "Atleta 🔥",
  "recommendation": "Estás en un nivel excelente...",
  "max_hr": 186,
  "heart_reserve": 121,
  "recovery_zone_min": 125,
  "recovery_zone_max": 138,
  "aerobic_zone_min": 138,
  "aerobic_zone_max": 151,
  "performance_zone_min": 151,
  "performance_zone_max": 175,
  "health_summary": "Resumen detallado de conclusiones...",
  "warnings": "[\"Advertencia 1\", \"Advertencia 2\"]",
  "suggestions": "[\"Sugerencia 1\", \"Sugerencia 2\"]",
  "created_at": "2024-04-14T10:30:00"
}
```

### Post de Blog
```json
{
  "id": 1,
  "title": "Título del post",
  "content": "Contenido del post",
  "author_id": 1,
  "created_at": "2024-01-01T00:00:00"
}
```

### Ejercicio
```json
{
  "nombre": "Flexiones",
  "tipo": "Cardio",
  "descripcion": "Ejercicio de resistencia corporal",
  "imagen": "url_imagen",
  "parque": "Parque Central"
}
```

### Parque
```json
{
  "name": "Parque Central",
  "address": "Calle Principal 123, Ciudad",
  "rating": 4.5,
  "distance": "2 km",
  "features": ["Bancas", "Áreas verdes", "Canchas"]
}
```

### Categoría de Foro
```json
{
  "name": "Rutinas de Ejercicio",
  "description": "Comparte tus rutinas y obtén sugerencias",
  "icon": "💪",
  "posts": 10,
  "topics": 10
}
```

### Post de Foro
```json
{
  "id": 1,
  "title": "¿Cuál es la mejor rutina para principiantes?",
  "excerpt": "Soy nuevo en esto...",
  "author": "Juan García",
  "category": "Rutinas de Ejercicio",
  "time_ago": "2 horas",
  "likes": 5,
  "replies": 3
}
```

---

## 🔐 Ejemplos de Uso

### Registrar Usuario
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan García",
    "email": "juan@example.com",
    "password": "password123",
    "birth_date": "1990-05-15"
  }'
```

### Iniciar Sesión
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "password123"
  }'
```

### Crear Análisis de Salud - **NUEVO**
```bash
curl -X POST http://localhost:8000/api/health/1 \
  -H "Content-Type: application/json" \
  -d '{
    "height_cm": 175,
    "weight_kg": 75,
    "resting_hr": 65,
    "age": 34
  }'
```

### Obtener Historial de Análisis - **NUEVO**
```bash
curl -X GET http://localhost:8000/api/health/1/history
```

### Obtener Resumen para Gráficas - **NUEVO**
```bash
curl -X GET http://localhost:8000/api/health/1/history-summary
```

### Obtener Análisis Específico - **NUEVO**
```bash
curl -X GET http://localhost:8000/api/health/analysis/5
```

### Crear Post de Blog
```bash
curl -X POST http://localhost:8000/api/blog/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Primer Post",
    "content": "Este es el contenido...",
    "author_email": "juan@example.com"
  }'
```

### Crear Ejercicio
```bash
curl -X POST http://localhost:8000/api/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Flexiones",
    "tipo": "Cardio",
    "descripcion": "Ejercicio de resistencia corporal",
    "imagen": "url_imagen"
  }'
```

---

## 🗄️ Base de Datos

### Tablas Principales
- `users` - Información de usuarios
- `health_profiles` - Perfiles de salud actuales
- `health_analysis` - **NUEVO - Histórico de análisis**
- `blog_posts` - Posts del blog
- `exercises` - Ejercicios
- `parks` - Parques
- `park_features` - Características de parques
- `exercise_park` - Relación ejercicio-parque
- `forum_categories` - Categorías del foro
- `forum_posts` - Posts del foro
- `forum_comments` - Comentarios del foro
- `likes` - Likes en posts y comentarios

### Relaciones
- `health_analysis.user_id` → `users.id` (con CASCADE delete)
- Permite múltiples análisis por usuario
- Cada análisis contiene análisis completo con zonas cardíacas, alertas y sugerencias

---

## ⚙️ Configuración

### Variables de Entorno (.env)
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/reactivate_pro
ENV=development
```

### Instalación y Ejecución

```bash
# Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos con datos de prueba
python init_data.py

# Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Cálculo de Score de Salud (v1.1)

### Métricas Incluidas

**1. IMC (Índice de Masa Corporal)**
- Óptimo (18.5-25): +0 puntos
- Sobrepeso (25-30): -15 puntos
- Bajo o sobre 30: -30 puntos

**2. Frecuencia Cardíaca en Reposo**
- < 70 bpm: Excelente, +0 puntos
- 70-80 bpm: -15 puntos
- > 80 bpm: -30 puntos

**3. Frecuencia Cardíaca Máxima** (calculada: 220 - edad)
- Base: 100 puntos
- Deducción según IMC y FC reposo

**4. Reserva Cardíaca** (max_hr - resting_hr)
- Define zonas de entrenamiento
- Rango de Karvonen

### Niveles de Score
- **85+**: Atleta 🔥 (Excelente)
- **70-84**: Buen nivel 💪 (Muy bueno)
- **50-69**: Mejorable ⚡ (Debe mejorar)
- **< 50**: Bajo rendimiento ⚠️ (Requiere atención)

### Análisis Detallado Incluido

Cada análisis ahora incluye:
- ✅ Conclusión personalizada del análisis
- ⚠️ Alertas según categoría de riesgo
- 💡 Sugerencias de mejora específicas
- 📊 Zonas cardíacas para entrenamiento
- 📈 Historial completo de análisis anteriores

---

## 🚀 Deployment

El proyecto está configurado para desplegarse en **Render** usando:
- `render.yaml` - Configuración de Render
- `runtime.txt` - Versión de Python (3.11.8)
- `requirements.txt` - Dependencias

Ver instrucciones en `README.md` para configurar DATABASE_URL en Render.

---

## 🔗 Conexión Frontend-Backend

### CORS Habilitados
El backend ahora permite CORS desde:
- `http://localhost:4200` - Desarrollo local
- `http://localhost:3000`
- `https://reactivate-pro.vercel.app` - Producción Vercel
- `https://reactivate-front.onrender.com` - Producción Render

### Configuración Frontend (Angular)
El frontend se conecta mediante:
- `ApiService` - Servicio centralizado para HTTP
- `HealthService` - Nuevos métodos para historial
- `AuthService` - Autenticación y persistencia

---

## 📝 Notas

- Todos los timestamps usan UTC
- Las contraseñas se almacenan con hash bcrypt
- Las relaciones permiten eliminación en cascada
- CORS habilitado para múltiples orígenes
- **NUEVO**: Historial de salud con análisis detallado
- **NUEVO**: Alertas y sugerencias personalizadas
- **NUEVO**: Zonas cardíacas calculadas automáticamente



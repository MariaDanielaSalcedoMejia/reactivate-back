# Backend para ReActivate Pro

Este backend en Python está diseñado para integrarse con el front-end de `reactivate-pro`.

## Características
- Autenticación de usuarios (registro y login)
- API REST para posts de blog
- API REST para foro y categorías
- Endpoints para ejercicios y parques
- Soporte de perfiles de salud
- Base de datos PostgreSQL

## Requisitos previos
- Python 3.11.8
- PostgreSQL 12+
- pip

## Configuración

### 1. Crear un entorno virtual:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Actualizar herramientas e instalar dependencias:
```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Configurar DATABASE_URL

#### Opción A: Desarrollo local con PostgreSQL
1. Crea un archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/reactivate_pro
ENV=development
```

2. Reemplaza `usuario`, `contraseña` y `reactivate_pro` con tus datos.

#### Opción B: En Render
1. Ve a tu servicio en Render
2. En la sección "Environment" → "Environment Variables"
3. Añade:
   - Key: `DATABASE_URL`
   - Value: obtén la URL desde tu base de datos PostgreSQL en Render (ej: `postgresql://user:pass@hostname:5432/db`)

### 4. Iniciar el servidor:
```powershell
uvicorn main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`

## Endpoints principales
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Login de usuario
- `GET /api/auth/me` - Obtener datos del usuario
- `GET /api/blog/posts` - Listar posts del blog
- `POST /api/blog/posts` - Crear post del blog
- `GET /api/forum/categories` - Listar categorías del foro
- `GET /api/forum/posts` - Listar posts del foro
- `POST /api/forum/posts` - Crear post del foro
- `GET /api/parks` - Listar parques
- `GET /api/exercises` - Listar ejercicios
- `GET /api/health/{user_id}` - Obtener perfil de salud
- `POST /api/health/{user_id}` - Actualizar perfil de salud

## Base de datos

### Inicialización automática
La base de datos se crea automáticamente al iniciar el servidor si no existe. Los modelos en `/app/models/` definen el esquema.

### Estructura de tablas
- `users` - Perfiles de usuario
- `health_profiles` - Perfiles de salud
- `blog_posts` - Posts del blog
- `forum_categories` - Categorías del foro
- `forum_posts` - Posts del foro
- `forum_comments` - Comentarios del foro
- `likes` - Sistema de likes
- `exercises` - Ejercicios disponibles
- `parks` - Parques de ejercicio
- `park_features` - Características de parques
- `exercise_park` - Relación many-to-many

## Notas de desarrollo
- El proyecto usa SQLAlchemy ORM con PostgreSQL
- Pydantic para validación de datos
- FastAPI para el framework web
- La variable de entorno `DATABASE_URL` es requerida en producción
- En desarrollo local, si no existe `.env`, se usa SQLite como fallback

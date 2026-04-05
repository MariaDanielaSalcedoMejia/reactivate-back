# Backend para ReActivate Pro

Este backend en Python está diseñado para integrarse con el front-end de `reactivate-pro`.

## Características
- Autenticación de usuarios (registro y login)
- API REST para posts de blog
- API REST para foro y categorías
- Endpoints para ejercicios y parques
- Soporte de perfiles de salud
- Base de datos SQLite local

## Ejecutar
1. Crear un entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. Iniciar el servidor:
   ```powershell
   uvicorn main:app --reload
   ```

## Endpoints principales
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/blog/posts`
- `POST /api/blog/posts`
- `GET /api/forum/categories`
- `GET /api/forum/posts`
- `POST /api/forum/posts`
- `GET /api/parks`
- `GET /api/exercises`
- `GET /api/health/{user_id}`
- `POST /api/health/{user_id}`

## Notas
El frontend actual de Angular aún no está integrado con la API. Actualmente usa `localStorage` para auth y datos temporales.
Este backend se puede conectar luego con servicios HTTP del front.

> Nota: en Python 3.14 algunos paquetes como `pydantic-core` pueden requerir Rust para compilar. Si no tienes Rust instalado, es más sencillo usar Python 3.11 o 3.12.

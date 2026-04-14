from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.controllers.auth_controller import router as auth_router
from app.controllers.blog_controller import router as blog_router
from app.controllers.forum_controller import router as forum_router
from app.controllers.park_controller import router as park_router
from app.controllers.exercise_controller import router as exercise_router
from app.controllers.health_controller import router as health_router
from app.management import router as management_router
from app.db import init_db, get_db
from app.config import DATABASE_URL

app = FastAPI(
    title="ReActivate Pro API",
    description="Backend Python para la app de ReActivate Pro",
    version="1.1.0"  # Version con historial de salud
)

# Initialize database tables on startup
@app.on_event("startup")
def startup():
    try:
        print("🔧 Initializing database tables (create_all)...")
        init_db()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"❌ ERROR during startup: {str(e)}")
        raise

# CORS Configuration - Permite conexiones desde frontend
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://reactivate-pro.vercel.app",
    "https://reactivate-front.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(blog_router, prefix="/api/blog", tags=["blog"])
app.include_router(forum_router, prefix="/api/forum", tags=["forum"])
app.include_router(park_router, prefix="/api/parks", tags=["parks"])
app.include_router(exercise_router, prefix="/api/exercises", tags=["exercises"])
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(management_router)

@app.get("/api/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        # Test database connection
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        return {
            "status": "ok",
            "database": "connected",
            "version": "1.1.0"
        }
    except Exception as e:
        print(f"❌ Healthcheck error: {str(e)}")
        return {
            "status": "error",
            "database": f"connection failed: {str(e)}",
            "version": "1.1.0"
        }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

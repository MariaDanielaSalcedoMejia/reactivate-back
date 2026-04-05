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
from app.db import init_db, get_db
from app.config import DATABASE_URL

app = FastAPI(
    title="ReActivate Pro API",
    description="Backend Python para la app de ReActivate Pro",
    version="1.0.1"  # Updated version to force redeploy
)

# Initialize database tables on startup (only for SQLite development)
@app.on_event("startup")
def startup():
    # Only initialize DB for SQLite (local development)
    # PostgreSQL (production) already has the schema
    if DATABASE_URL.startswith('sqlite'):
        init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(blog_router, prefix="/api/blog", tags=["blog"])
app.include_router(forum_router, prefix="/api/forum", tags=["forum"])
app.include_router(park_router, prefix="/api/parks", tags=["parks"])
app.include_router(exercise_router, prefix="/api/exercises", tags=["exercises"])
app.include_router(health_router, prefix="/api/health", tags=["health"])

@app.get("/api/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

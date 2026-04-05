from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.auth_controller import router as auth_router
from app.controllers.blog_controller import router as blog_router
from app.controllers.forum_controller import router as forum_router
from app.controllers.park_controller import router as park_router
from app.controllers.exercise_controller import router as exercise_router
from app.controllers.health_controller import router as health_router

app = FastAPI(
    title="ReActivate Pro API",
    description="Backend Python para la app de ReActivate Pro",
    version="1.0.0"
)

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
def healthcheck():
    return {"status": "ok"}

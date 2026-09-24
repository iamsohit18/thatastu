"""RoboTeleop Data Platform Main FastAPI Server."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.health import router as health_router
from backend.api.robots import router as robots_router
from backend.api.leader import router as leader_router
from backend.api.cameras import router as cameras_router
from backend.api.episodes import router as episodes_router
from backend.api.datasets import router as datasets_router

app = FastAPI(
    title="RoboTeleop Data Platform API",
    description="Backend API for robot teleoperation, safety monitoring, and synchronized demonstration recording.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(robots_router)
app.include_router(leader_router)
app.include_router(cameras_router)
app.include_router(episodes_router)
app.include_router(datasets_router)


@app.get("/")
def root():
    return {
        "name": "RoboTeleop Data Platform",
        "status": "online",
        "documentation": "/docs",
    }

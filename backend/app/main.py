from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.services.model_loader import load_models


app = FastAPI(
    title="DriveGuard-X AI Backend",
    version="0.1.0",
    description=(
        "Inference backend for the DriveGuard-X research prototype. "
        "The current implementation exposes the Battery AI model; "
        "IMU, Road, Fusion, Attribution and Protection modules will be added later."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
def startup_event() -> None:
    load_models()


@app.get("/", tags=["system"])
def root():
    return {
        "project": "DriveGuard-X",
        "service": "AI Backend",
        "status": "running",
        "version": app.version,
    }

"""FastAPI application entry point."""

from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

@app.get("/")
async def root():
    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

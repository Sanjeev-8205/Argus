"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.routes.retrieval_route import router as retrieval_router
from app.services.retrieval_service import RetrievalService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.retrieval_service = RetrievalService()
    yield

app = FastAPI(lifespan=lifespan, title=settings.app_name, version=settings.app_version)

app.include_router(retrieval_router)

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

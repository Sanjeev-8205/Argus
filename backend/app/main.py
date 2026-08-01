"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="Cadastre", version="0.1.0")

@app.get("/")
async def root():
    return {
        "project": "Cadastre",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

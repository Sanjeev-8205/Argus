"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="Cadastre")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

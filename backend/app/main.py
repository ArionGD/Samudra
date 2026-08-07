"""Samudra Shastra API entrypoint.

Run locally with: uv run uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import ContactBase, ResearchBase, contact_engine, research_engine
from app.routers import admin, session, withdraw


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Dev convenience only: create tables directly from models on SQLite.
    # Production (Postgres) is migration-managed via Alembic — see
    # database/README.md — and should NOT rely on this create_all.
    if settings.research_database_url.startswith("sqlite"):
        ResearchBase.metadata.create_all(bind=research_engine)
    if settings.contact_database_url.startswith("sqlite"):
        ContactBase.metadata.create_all(bind=contact_engine)
    yield


app = FastAPI(
    title="Samudra Shastra API",
    description=(
        "Session, condition-assignment, and response-ingest API for the "
        "faking-resistant assessment battery. Research use only — see "
        "docs/00-project-charter.md and docs/02-ethics-and-consent.md."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(session.router)
app.include_router(withdraw.router)
app.include_router(admin.router)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "environment": settings.environment}

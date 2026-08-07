"""Two separate SQLAlchemy engines/sessions — one per store.

This module intentionally does NOT provide a single shared `engine`. The
research store (responses, timings, banded demographics) and the contact
store (email addresses) are different trust domains and must stay on
physically separate connections/databases in both dev and prod, so the
separation is structural rather than a convention someone can forget.
See ARCHITECTURE.md #4.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings


def _engine_kwargs(url: str) -> dict:
    if not url.startswith("sqlite"):
        return {}
    # SQLite: no thread-affinity check (server is multithreaded), and no
    # pooled/idle connections (NullPool) so file handles are released
    # immediately after each use rather than held indefinitely — otherwise
    # the dev .db file can't be deleted/replaced while the app is running,
    # and on Windows specifically, temp-dir test cleanup fails with
    # WinError 32 ("used by another process").
    return {"connect_args": {"check_same_thread": False}, "poolclass": NullPool}


research_engine = create_engine(settings.research_database_url, **_engine_kwargs(settings.research_database_url))
contact_engine = create_engine(settings.contact_database_url, **_engine_kwargs(settings.contact_database_url))

ResearchSession = sessionmaker(bind=research_engine, autoflush=False, expire_on_commit=False)
ContactSession = sessionmaker(bind=contact_engine, autoflush=False, expire_on_commit=False)


class ResearchBase(DeclarativeBase):
    """Declarative base for research-store models (participants, sessions, responses)."""


class ContactBase(DeclarativeBase):
    """Declarative base for contact-store models (email delivery only)."""


def get_research_db() -> Generator[Session, None, None]:
    db = ResearchSession()
    try:
        yield db
    finally:
        db.close()


def get_contact_db() -> Generator[Session, None, None]:
    db = ContactSession()
    try:
        yield db
    finally:
        db.close()

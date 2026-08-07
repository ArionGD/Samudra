"""Application settings.

Both database URLs default to local SQLite files under `database/dev/` so the
project runs with zero external setup. In production, override
`RESEARCH_DATABASE_URL` and `CONTACT_DATABASE_URL` via environment variables
(or a `.env` file, not committed) to point at the two separate Neon Postgres
instances. See ARCHITECTURE.md #4 and #8 for why these two stores are never
allowed to be the same database.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/config.py -> backend/ -> Samudra_Shastra/ -> database/dev/
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEV_DB_DIR = _PROJECT_ROOT / "database" / "dev"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    environment: str = "development"

    # Two physically separate stores. Never point these at the same database —
    # see ARCHITECTURE.md #4 (two-store privacy separation).
    research_database_url: str = f"sqlite:///{(_DEV_DB_DIR / 'research.db').as_posix()}"
    contact_database_url: str = f"sqlite:///{(_DEV_DB_DIR / 'contact.db').as_posix()}"

    # Item banks live in git as versioned YAML, not in the database.
    # See docs/04-data-schema.md.
    items_dir: str = str(_PROJECT_ROOT / "items")

    admin_api_key: str = "change-me-in-.env"

    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()

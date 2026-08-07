# Database

Two physically separate stores, always. See [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
§4 for why — the short version: a breach of the research store must never be
able to reveal who gave which answers, so response data and contact data never
share a database, in dev or in production.

```
database/
├── README.md          # this file
└── dev/                # local SQLite files — gitignored, created automatically
    ├── research.db     # participants, sessions, responses, reading baseline, quality flags
    └── contact.db      # email delivery only
```

## Development: SQLite

Nothing to install. The backend creates both SQLite files automatically on
first run (see `backend/app/main.py`'s startup lifecycle) at
`database/dev/research.db` and `database/dev/contact.db`. Delete either file
to reset that store to empty.

This works because the SQLAlchemy models (`backend/app/models/`) avoid
Postgres-only syntax — JSONB columns are declared with SQLAlchemy's dialect-
agnostic `JSON` type, which degrades to SQLite's `JSON1` extension locally and
gets full JSONB + GIN indexing in Postgres. Swapping environments is a
connection-string change, not a rewrite.

## Production: PostgreSQL via Neon

Two **separate Neon projects** (stronger isolation than two databases inside
one project — see `../ARCHITECTURE.md` §11):

1. **`samudra-shastra-research`** — the research store. Backs `RESEARCH_DATABASE_URL`.
2. **`samudra-shastra-contact`** — the contact store. Backs `CONTACT_DATABASE_URL`.

### Setting up a Neon project

1. Create the project at [neon.tech](https://neon.tech) (free tier).
2. Copy the pooled connection string it gives you.
3. Convert it to the `postgresql+psycopg://` scheme SQLAlchemy expects, e.g.:

   ```
   postgresql+psycopg://<user>:<password>@<host>/<dbname>?sslmode=require
   ```

4. Set it as `RESEARCH_DATABASE_URL` (or `CONTACT_DATABASE_URL`) in the
   backend's `.env` — see `backend/.env.example`.
5. **Verify encryption at rest is enabled** in the Neon project settings before
   asserting it in any consent material — most managed providers default to
   this, but confirm rather than assume (docs/10, §7).

### Running migrations against Postgres

```bash
cd backend
uv run alembic upgrade head
```

Alembic is configured (`backend/alembic/env.py`) to read `RESEARCH_DATABASE_URL`
from the same settings object the app uses, so whatever's in `.env` or the
deployed environment is what gets migrated — no separate URL to keep in sync.

**The contact store's schema is one small table** (`backend/app/models/contact.py`).
It does not yet have its own Alembic setup because a single table rarely
needs migration history — if that stops being true, mirror the research
store's Alembic config with a second `alembic.ini`/`env.py` pointed at
`ContactBase.metadata` and `CONTACT_DATABASE_URL`.

### Backups

Neon takes automated backups on paid tiers; confirm what the free tier
actually retains before relying on it. Per docs/10 §7, also keep a periodic
manual export to encrypted local storage independent of the provider.

## What never happens here

- The two stores are never queried in a way that joins them.
- Production data is never analysed in place — see `docs/10-tech-stack-and-system-design.md`
  §7: "Never analyse on production data. Export the de-identified extract and
  work on that."
- Item bank content does **not** live in either database — it's versioned YAML
  under `../items/`, loaded into memory at API startup. See
  `docs/04-data-schema.md`.

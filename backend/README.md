# Backend

FastAPI service: session lifecycle, server-side condition assignment, response
ingest, withdrawal, and admin monitoring. See [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
for the full system design and why these responsibilities live server-side.

## Setup

Requires Python 3.13+ and [`uv`](https://docs.astral.sh/uv/).

```bash
cd backend
uv sync                 # installs dependencies into a local .venv
cp .env.example .env    # edit as needed; defaults work for local dev
uv run alembic upgrade head   # creates/updates the research-store schema
```

No setup is needed for the databases themselves in dev — both SQLite files are
created automatically under `../database/dev/` the first time the app starts,
and the command above applies the same schema via Alembic (recommended, since
it's the same path production uses).

## Run

```bash
uv run uvicorn app.main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for the auto-generated OpenAPI docs.

## Test

```bash
uv run pytest
```

## Structure

```
backend/
├── app/
│   ├── main.py            # FastAPI app, CORS, router wiring
│   ├── config.py          # Settings (env-driven), dev DB paths
│   ├── database.py        # Two engines/sessions — research store + contact store
│   ├── schemas.py         # Pydantic request/response models (API boundary)
│   ├── models/
│   │   ├── research.py    # Participant, Session, Response, ReadingBaseline, QualityFlag
│   │   └── contact.py     # Contact (email delivery only)
│   ├── routers/
│   │   ├── session.py     # POST /session, /session/{id}/responses, /session/{id}/complete
│   │   ├── withdraw.py    # POST /withdraw — real delete, not a flag
│   │   └── admin.py       # GET /admin/monitor (API-key auth)
│   ├── randomisation/
│   │   └── condition.py   # Server-side stratified condition assignment (minimisation)
│   └── items/
│       └── loader.py      # Loads versioned YAML item banks; desirability-spread validator
├── alembic/                # Migrations for the research store
├── tests/
└── pyproject.toml
```

## Endpoints (current)

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/health` | GET | none | Liveness check |
| `/session` | POST | none | Create participant + session, assign condition server-side |
| `/session/{id}/responses` | POST | none | Batched response ingest |
| `/session/{id}/complete` | POST | none | Mark session complete/abandoned |
| `/withdraw` | POST | none | **Real delete** of a participant's data |
| `/admin/monitor` | GET | `x-admin-key` header | N per channel/condition, completion rate |

Not yet built: `/feedback/{id}` (Stage A/B reports) and `/admin/export`
(de-identified extract) — see `../docs/11-implementation-plan.md` §4 for the
intended build order. Both are meant to exist **before** real participant data
does, not after.

## Environment variables

See `.env.example`. The two that matter most:

- `RESEARCH_DATABASE_URL` — defaults to a local SQLite file; set to a Neon
  Postgres URL in production.
- `CONTACT_DATABASE_URL` — same, but **must point at a different physical
  database** than `RESEARCH_DATABASE_URL`, always. See `../database/README.md`.

## Notes for whoever picks this up next

- The item-bank YAML loader (`app/items/loader.py`) expects
  `items/<MODULE>/<VERSION>/{statements,blocks}.yaml` under the path in
  `ITEMS_DIR` (defaults to `../items`). No real item content exists yet —
  see `../items/README.md`.
- `validate_desirability_spread()` in that same file is meant to run as a CI
  step that fails the build if it returns any violations — not wired into CI
  yet, since there's no CI pipeline configured at this stage.
- Table creation via `Base.metadata.create_all()` only runs automatically for
  SQLite (dev convenience). Postgres is migration-managed only — never rely on
  `create_all()` there.

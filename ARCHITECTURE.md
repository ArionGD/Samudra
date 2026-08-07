# Architecture

**Status:** v0.1 — initial scaffold
**Companion to:** [`README.md`](README.md), [`docs/10-tech-stack-and-system-design.md`](docs/10-tech-stack-and-system-design.md)

This document describes how the system fits together and why. Full per-decision
reasoning already exists in `docs/10-tech-stack-and-system-design.md`; this file
is the living, code-adjacent version of it — update this one as the system
actually evolves, treat the numbered doc as the historical decision record.

---

## 1. Constraints that shape every decision below

| Constraint | Consequence |
|---|---|
| Millisecond-accurate response timing | Timing measured client-side only; nothing in the critical timing path may touch the network; no server-side rendering |
| Mobile-first, unreliable Indian mobile networks | Offline queue required; small bundles; 360px viewport is the primary design target, not an edge case |
| Solo maintainer, near-zero budget | Boring, well-understood technology over clever technology; free tiers until N outgrows them |
| Randomisation and item-bank version must be trustworthy | Cannot live client-side — this alone rules out a client-writes-direct backend-as-a-service |
| Analysis requires Thurstonian IRT | R is a hard dependency (`thurstonianIRT` has no mature equivalent elsewhere), kept fully offline from the live system |
| Participant data is sensitive, consent-governed | Two physically separate data stores; deletion must actually work, not just be flagged |

---

## 2. System diagram

```
┌──────────────────────────────────────────────────────────┐
│  FRONTEND  (frontend/)                                    │
│  React 18 + Vite + TypeScript + Tailwind                  │
│                                                             │
│  ├─ timing/     performance.now() + rAF double-anchor      │
│  ├─ modules/    M1..M5 delivery components                 │
│  ├─ offline/    IndexedDB response queue                   │
│  ├─ consent/    layered consent flow                       │
│  └─ api/        typed client for the backend                │
│                                                             │
│  Dev:  Vite dev server, localhost                          │
│  Prod: static build → Cloudflare Pages (CDN)                │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS / JSON
┌───────────────────────┴─────────────────────────────────────┐
│  BACKEND  (backend/)                                         │
│  FastAPI (Python) + SQLAlchemy 2.0 + Pydantic v2              │
│                                                               │
│  ├─ routers/        /session /responses /feedback /withdraw │
│  │                  /admin/export /admin/monitor              │
│  ├─ models/         SQLAlchemy ORM models                    │
│  ├─ randomisation/  server-side stratified condition assign  │
│  ├─ items/           loads versioned YAML item banks at boot │
│  └─ export/          de-identified extract generation         │
│                                                               │
│  Dev:  uvicorn, localhost                                     │
│  Prod: container → Fly.io                                     │
└──────────┬────────────────────────────┬───────────────────────┘
           │                            │
┌──────────┴─────────────┐   ┌──────────┴──────────────────────┐
│  RESEARCH STORE          │   │  CONTACT STORE                   │
│  (database/)             │ ✗ │  (database/)                     │
│  no direct identifiers    │  │  emails only, short-lived         │
│                           │no│                                   │
│  Dev:  SQLite file         │join│  Dev:  SQLite file              │
│  Prod: Postgres (Neon A)   │  │  Prod: Postgres (Neon B)          │
└──────────┬─────────────────┘   └──────────────────────────────────┘
           │ de-identified CSV export (one-way, manual/scripted)
┌──────────┴───────────────────────────────────────────────────┐
│  ANALYSIS (offline — separate from the live system entirely)   │
│  Python: cleaning, exclusions, descriptives, semantic scoring   │
│  R: thurstonianIRT (calibration), lavaan (CFA), lme4 (latency)  │
└──────────────────────────────────────────────────────────────┘
```

**Item banks live in git**, not in either database — versioned YAML under
`items/`, loaded into memory by the backend at startup. Content changes are
reviewable in pull requests and diffable; a CI check enforces the
desirability-spread rule (≤ 0.5 within a block) before merge, so a bad block
can't reach participants silently.

---

## 3. Why three separate top-level folders

`frontend/`, `backend/`, `database/` are kept as distinct top-level concerns,
each independently deployable and independently replaceable:

- **`frontend/`** owns nothing about correctness or trust. It renders items,
  measures timing precisely, queues responses offline, and talks to the backend
  over a typed HTTP client. It never decides condition assignment, never scores
  anything, and never holds the item bank as a source of truth (it receives a
  served, versioned payload).
- **`backend/`** is the only trusted party. It assigns experimental condition,
  serves the correct item-bank version, validates and stores responses, and is
  the only thing with credentials to either database. All research-validity-critical
  logic lives here specifically because it cannot live in the client.
- **`database/`** is treated as its own concern (rather than "part of the
  backend") because of the two-store separation: response data and contact data
  are different trust domains with different lifetimes, different access
  patterns, and — in production — different physical database instances that
  are deliberately never joinable without a key held outside both systems. That
  split is a data-protection control, not an implementation detail, and keeping
  it a first-class folder keeps it visible.

---

## 4. The two-store privacy separation

```
RESEARCH STORE                         CONTACT STORE
────────────────                       ──────────────
participant_code (UUID, random)   ✗    contact_id
sessions, responses, timings     no    email
banded demographics             join   delivery_flag
quality_flags
```

**Threat model:** a breach of the research store must not reveal who said what.
If a participant wants results emailed, the link between `participant_code` and
their email should ideally not persist at all — send the feedback at session end
and store only a delivery flag against the contact record. If a persistent link
is genuinely required, it lives in a third, minimal, access-restricted store —
never inside either primary database.

In **dev**, this is simulated with two separate SQLite files (not one file with
two tables) so the separation is structural from day one, not something that gets
enforced only in production and forgotten locally. In **production**, these are
two separate Neon Postgres instances/projects.

---

## 5. Timing subsystem (frontend, non-negotiable design)

This is the most technically load-bearing part of the codebase. It cannot be
retrofitted, because retrofitting means re-collecting data.

Rules, in order of importance:

1. **`performance.now()`, never `Date.now()`.** Wall-clock time is subject to
   NTP correction mid-session and is only millisecond-resolution at best.
   `performance.now()` is monotonic and sub-millisecond.
2. **Anchor the clock to paint, not to state change.** The first
   `requestAnimationFrame` callback fires before paint; the second fires after.
   Capture the timestamp in the second.
3. **Preload the entire module payload before presentation begins.** No network
   request may occur between items — a slow connection must never contaminate
   latency data.
4. **Always capture the confounds alongside latency:** device type, input method,
   viewport width, `visibilitychange` (tab backgrounded mid-item), and a
   reading-speed baseline task completed once per session. Latency without the
   reading-speed baseline is not analysable later — there is no way to add it
   retroactively.
5. **Verify against an external clock before every pilot.** A scripted responder
   firing at known intervals must produce recorded latencies that match, within
   tolerance, before real participant data is trusted.

## 6. Offline resilience (frontend)

Indian mobile connectivity makes disconnection an expected event, not an
exception path.

- Queue responses in **IndexedDB** (`idb-keyval`) as they occur.
- Flush to the backend in small batches or on module completion.
- Retry with exponential backoff on failure.
- Never hold a full module purely in memory awaiting a single end-of-module
  submit — backgrounded mobile tabs get killed by the OS and in-memory state is
  lost with them.

## 7. Condition assignment (backend, non-negotiable design)

Random assignment to experimental condition (honest/faking × timed/untimed) is
the thing the whole faking experiment depends on being trustworthy. It is
**assigned server-side at session creation, stratified by recruitment channel,
and immutable once assigned.** A minimisation strategy (assign to whichever
condition currently has the fewest participants within that channel, breaking
ties randomly) keeps cells balanced without becoming predictable. This cannot
happen client-side — a client is not a trusted party, and unbalanced or gameable
cells silently destroy the experiment's validity.

## 8. Environments: SQLite now, Postgres/Neon later

| | Development | Production |
|---|---|---|
| Research store | SQLite file, `database/dev/research.db` | Postgres, Neon project A |
| Contact store | SQLite file, `database/dev/contact.db` | Postgres, Neon project B |
| Why | Zero setup, fast iteration, no network dependency while building | Managed backups, encryption at rest, concurrent-write safety for real participant traffic |
| Migration path | SQLAlchemy models + Alembic migrations are written to be dialect-agnostic from the start | Same migrations run against Postgres; SQLite-only syntax is avoided deliberately so switching is a config change, not a rewrite |

The application code targets SQLAlchemy's ORM layer rather than
dialect-specific SQL, specifically so that swapping the `DATABASE_URL` (and
`CONTACT_DATABASE_URL`) environment variables is the entire migration from dev
to prod. JSONB (Postgres) vs JSON (SQLite fallback) is the one place this needs
explicit handling — SQLAlchemy's `JSON` type variant is used in models so it
degrades correctly on SQLite and gets full JSONB/GIN behaviour on Postgres.

## 9. What's deliberately not here yet

This scaffold stands up structure, not the full participant-facing product.
Explicitly out of scope for the initial commit:

- Any real item content beyond a small placeholder set for wiring/testing
- Deployment configuration (Fly.io/Cloudflare Pages configs) — added when there's
  something worth deploying
- The R analysis pipeline — lives entirely offline against exported CSVs, has no
  dependency on the live system, and is built separately per `docs/09-calibration-methodology.md`
- Modules M2–M5 — M1 first, end-to-end, per `docs/11-implementation-plan.md`

## 10. Rejected alternatives (kept from doc 10, for continuity)

| Rejected | Reason |
|---|---|
| Next.js / any SSR framework | Hydration timing is incompatible with the timing subsystem's paint-anchoring requirement |
| Firebase / Supabase with client-side writes | Condition assignment and item-bank version must be server-authoritative |
| MongoDB | Data is genuinely relational (participants → sessions → responses); JSONB columns cover the flexibility need without giving up referential integrity |
| Qualtrics / Google Forms / Typeform | No millisecond timing, no native forced-choice triplet support, third-party US hosting complicates data-protection position |
| Redux / Zustand | A session is short-lived and linear; no cross-cutting state exists to justify it |
| `reticulate` / `rpy2` for Python↔R interop | Fragile, hard to debug, hostile to independent reproduction — a CSV export boundary is used instead |

---

## 11. Open architectural questions

- **Auth for the admin endpoints** — single hardcoded admin credential is fine at
  N=0; needs a real decision (even if still simple) before any production deploy.
- **Exact Neon project/branch topology** — one project with two databases, or two
  fully separate Neon projects? Two separate projects is the stronger isolation
  guarantee and is the current default assumption; revisit if it becomes operationally painful.

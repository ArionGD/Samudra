# Samudra Shastra

**An open, time-pressured, faking-resistant psychometric assessment battery — validated on an Indian sample.**

**Status:** early build. Research-only. Not a hiring tool. No data collected yet.

---

## What this is

Most personality assessments used in hiring — the adjective-checklist family in
particular (Myers-Briggs-style tools, PI-style behavioural questionnaires) — share
a structural weakness: each item has an obviously "correct" or socially desirable
answer, so anyone motivated to make a good impression can shift their profile
toward whatever the job seems to reward. This is well documented in the
faking/social-desirability literature and is not a controversial claim.

Samudra Shastra is a research project (and the platform that runs it) that builds
an instrument designed to resist that specific failure, and tests a genuinely
open question about how to resist it further.

**The core mechanism — multidimensional forced choice.** Instead of rating single
statements ("I am organised" — agree/disagree, where agreeing is always the safe
answer), participants see blocks of three statements drawn from *different*
underlying dimensions, all pre-matched on social desirability by an independent
rating sample. They pick the one **most** like them and the one **least** like
them. Because no statement in the block is more flattering than the others, there
is no uniformly "good" answer to fake toward. Scores are recovered from these
forced comparisons using **Thurstonian Item Response Theory**, which solves the
classical problem that naively-scored forced-choice data isn't comparable across
people (ipsativity).

**The open research question — does time pressure help further?** The instrument
is administered under experimentally varied conditions: untimed vs. timed, and
honest vs. instructed-to-fake. If deliberate distortion takes cognitive effort —
suppressing an honest response and constructing a strategic one — then tight time
limits should constrain how much distortion is achievable, on top of whatever the
forced-choice format already removes. The published evidence for this is thin and
mixed. A clean experiment is a real contribution regardless of which way it comes
out, and a null result gets reported as a null result, not buried.

**Why India specifically.** Almost all forced-choice and faking research to date
runs on Western, English-speaking samples. Whether the same factor structure and
the same fakability advantages hold in an Indian sample is an open, publishable
question in its own right — not an afterthought to a Western-designed instrument.

## What this is explicitly not

- **Not a hiring tool.** No criterion validation (linking scores to actual job
  performance) exists or is in scope for this phase. Terms of use prohibit using
  results for any selection, admission, or benefit decision.
- **Not a clinical instrument.** No mental-health constructs, no diagnosis.
- **Not an IQ test.** The reasoning module measures reasoning quality under
  specific conditions, not general intelligence, and is never reported as an IQ score.
- **Not collecting from minors** without a specific, separately reviewed protocol.

See [`docs/00-project-charter.md`](docs/00-project-charter.md) for the full scope
statement, and [`docs/02-ethics-and-consent.md`](docs/02-ethics-and-consent.md)
before touching anything participant-facing.

## The five modules

| Code | Module | Construct | Format | Status |
|---|---|---|---|---|
| **M1** | Rapid Trait | 4 work-relevant traits (Conscientious Reliability, Stress Tolerance, Cooperative Orientation, Assertive Drive) | Forced-choice triplets, 12s/block | **Build priority 1** |
| M3 | Critical Reasoning | Reasoning quality, not IQ | Timed multiple choice | Build priority 2 (cheap; validity anchor for M1) |
| M2 | Divergent Thinking | Ideational fluency/flexibility/originality | Timed open-text generation | Build priority 3 |
| M4 | Judgement | Practical/interpersonal judgement | Situational judgement test, knowledge-keyed | Build priority 4 (needs SME item development) |
| M5 | Ethical Judgement | *Consistency* of moral reasoning, never "moral quality" | Forced-choice trade-offs | Build priority 5 (highest ethics sensitivity) |

M1 alone, fully calibrated with the honest-vs-faking × timed-vs-untimed experiment,
is a complete, publishable study on its own. Nothing else gets built until M1 works
end-to-end with real participants. See [`docs/11-implementation-plan.md`](docs/11-implementation-plan.md).

## Repository layout

```
Samudra_Shastra/
├── README.md                 # this file
├── ARCHITECTURE.md           # system design, data flow, and the reasoning behind every choice
├── docs/                     # full project documentation (charter, ethics, schema, analysis plan...)
├── frontend/                 # React + Vite + TypeScript — participant-facing delivery
├── backend/                  # FastAPI — session, condition assignment, ingest, export
├── database/                 # schema, migrations, local SQLite for dev
└── items/                    # versioned item banks (YAML), reviewed like code
```

Frontend, backend, and database are kept as separate top-level concerns
deliberately — see `ARCHITECTURE.md` for why, particularly around the two-store
privacy separation and why item content lives in git rather than the database.

## Tech stack at a glance

| Layer | Choice |
|---|---|
| Frontend | React 18 + Vite + TypeScript + Tailwind |
| Backend | FastAPI (Python) + SQLAlchemy 2.0 + Pydantic v2 |
| Database (dev) | SQLite |
| Database (production) | PostgreSQL via Neon, two separate instances |
| IRT / statistical calibration | R (`thurstonianIRT`, `lavaan`, `lme4`) — offline, not in the request path |
| Hosting | Cloudflare Pages (frontend) + Fly.io (backend) + Neon (database) — free tiers |

Full reasoning for every choice — and what was rejected and why — is in
[`ARCHITECTURE.md`](ARCHITECTURE.md).

## Getting started (local dev)

```bash
# Backend — FastAPI on http://127.0.0.1:8000
cd backend
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload

# Frontend — Vite dev server on http://127.0.0.1:5173, in a second terminal
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Both halves are verified to install, boot, and talk to each other as of this
scaffold — `backend/` has a passing pytest suite (`uv run pytest`) covering
the full session→respond→complete→withdraw lifecycle, and `frontend/` builds
clean with `npm run build`. Each subfolder's README has the full detail;
this file stays high-level on purpose.

## Current status

This is a **scaffold**, not the participant-facing product. What exists:
server-side condition assignment, response ingest, a working (tested) real
delete on withdrawal, the timing subsystem's paint-anchoring, an offline
response queue, a layered-consent pattern, and one wired-up placeholder M1
block proving the whole loop end-to-end. What doesn't exist yet: real M1
item content (`items/README.md` explains what's needed), modules M2–M5,
the Stage A/B feedback screens, the de-identified export pipeline, and any
deployment config. See [`docs/11-implementation-plan.md`](docs/11-implementation-plan.md)
§4 for the intended build order from here.

## Related documentation

The `docs/` folder carries the full project record: research questions, ethics
and consent architecture, data schema, recruitment plan, pre-registered analysis
plan, calibration methodology, and participant feedback design. Read
`docs/02-ethics-and-consent.md` before doing anything that touches real
participants, and `docs/00-project-charter.md` for the research questions this
whole platform exists to answer.

# Implementation Plan (Consolidated)

**Status:** Draft v0.1 — synthesised from documents 00–10 and the PI/ companion set
**Purpose:** a single actionable plan that ties the charter, ethics, architecture,
schema, recruitment, analysis, calibration, and feedback documents into one
build sequence, with the open decisions surfaced up front.

---

## 0. Housekeeping note on the source files

Before the plan: two things found while reading everything in `d:\ANTI-GRAVITY\PI`.

1. **The five `.zip` files are redundant.** `files.zip`, `filesk.zip`, `idea.zip`,
   `pi.zip`, and `pi tech stack and idea.zip` all unpack to copies of the same
   markdown documents already sitting unzipped in this folder and in `PI/`
   (00–07 at top level, 08–09 plus `AUDIT.md`/`ROADMAP.md`/the patch file inside
   `PI/`, and 10 at top level). Nothing in the zips is unique. Safe to delete
   the zips and `New Text Document.txt` once you've confirmed the same.
2. **`PI/AUDIT.md`, `PI/ROADMAP.md`, and `PI/selection-engine-docs.patch` belong
   to a different, unrelated project** — a stock-market "ALTAIR / Phoenix"
   short-selling fragility-ranking engine (`VulnerabilityRanker`, sector
   scorers, `astra_strike_score`). They describe factor-engine bugs, peer-relative
   normalisation, and a backtest roadmap for a financial ranking system, not the
   assessment battery. They appear to have been dropped into this folder by
   mistake. **Recommendation: move them out of this project's folder** (into
   whatever repo the ALTAIR/Phoenix engine actually lives in) so they don't
   confuse future readers or get committed into the assessment-platform repo.
   Flagging rather than deleting, since I can't tell if you still need the copy.

Everything below concerns the actual project: the **Multi-Module Faking-Resistant
Assessment Battery**.

---

## 1. The idea, in one paragraph

Adjective-checklist personality tools (the PI/MBTI family) are easy to fake because
each item has an obviously "good" answer. This project builds a research-grade,
open, five-module assessment battery that resists that by (a) using multidimensional
forced-choice items matched on social desirability so no answer is transparently
better, (b) testing whether **time pressure** further suppresses deliberate
distortion — a thin and mixed evidence base, and the project's most original
contribution — and (c) validating the whole thing on an **Indian sample**, where
almost no forced-choice/faking research currently exists. It is explicitly a
research project first and a portfolio artefact second, not a hiring product:
no criterion validation exists or is planned in-scope, and the terms of use must
say so.

The five modules (`01-instrument-design.md`), in build priority order:

| Priority | Module | Construct | Format | Why this order |
|---|---|---|---|---|
| 1 | **M1 Rapid Trait** | 4 work-relevant traits (CON/STR/COO/DRV) | Forced-choice triplets, 12s/block, timed | Carries the core research question; needs the most calibration N; highest engineering complexity |
| 2 | **M3 Critical Reasoning** | Reasoning quality (not IQ) | MCQ, 45s/item | Cheap to build; inherently fake-resistant; serves as a validity anchor for M1 |
| 3 | **M2 Divergent Thinking** | Fluency/flexibility/originality | Open text generation, 3 min/prompt | Interesting scoring problem (semantic-distance originality); peripheral to core RQ |
| 4 | **M4 Judgement (SJT)** | Practical/interpersonal judgement | Scenario ranking, knowledge-keyed | Needs critical-incident interviews + SME keying — expensive item development |
| 5 | **M5 Ethical Judgement** | Consistency of moral reasoning (not "morality") | Forced-choice trade-offs | Highest ethics sensitivity; least essential to the core RQ |

**Minimum viable version** (from `07-roadmap.md`, §"Minimum viable version"): M1
alone, fully calibrated, with the honest-vs-faking and timed-vs-untimed experiment,
is a complete, publishable study — roughly 8 months. Cut M5 → M4 → NGO channel →
M2 → H6(invariance), in that order, if time runs out. **Do not start building M2–M5
before M1 works end-to-end with real participants.**

---

## 2. Tech stack (already specified in `10-tech-stack-and-system-design.md` — summarised here as the decision record)

| Layer | Choice | Non-negotiable reason |
|---|---|---|
| Frontend | React 18 + Vite + TypeScript + Tailwind | Client-side control over the render/measure cycle; **no Next.js** — SSR hydration timing is incompatible with millisecond-accurate latency capture |
| Timing | `performance.now()` + double `requestAnimationFrame` anchor | `Date.now()` is wall-clock and coarse; must anchor to *paint*, not to React state change |
| Offline queue | IndexedDB via `idb-keyval` | Indian mobile connectivity drops are the normal case, not an edge case |
| State | Plain React state + context (no Redux/Zustand) | Session is short-lived and linear; a state library adds complexity with no payoff |
| Backend | FastAPI (Python 3.12) + SQLAlchemy 2.0 + Pydantic v2 | Condition assignment and item-bank version **must** be server-authoritative — rules out a client-writes-direct BaaS (Supabase/Firebase) |
| Database | PostgreSQL ×2 (Neon free tier), never joined | Relational structure (participants→sessions→responses) + JSONB for module-varying payloads; **two physically separate stores** so a breach of response data can't reveal identity |
| Migrations | Alembic from table 1 | Hand-editing schema against consented human-subjects data is how it gets destroyed |
| Hosting | Cloudflare Pages (frontend, free/global CDN) + Fly.io (backend, free tier) | ₹0 baseline cost; ~₹1,000/yr for a domain is the only real spend |
| Item banks | Versioned YAML in git, loaded at API startup | Reviewable in PRs, diffable, CI-enforced desirability-spread ≤ 0.5 check |
| IRT / CFA / mixed models | **R**: `thurstonianIRT`, `lavaan`, `lme4` | Only mature Thurstonian IRT implementation exists in R — not a preference, a hard dependency |
| Cleaning / descriptives / ML scoring | Python: pandas/polars, `sentence-transformers` for M2 semantic-distance originality | Shares code with the API; ML ecosystem lives here |
| Python↔R boundary | De-identified CSV export, **not** `reticulate`/`rpy2` | In-process cross-language interop is fragile and hostile to reproduction |
| Reproducibility | `uv` + lockfile (Python), `renv` (R), seeds set explicitly | A reviewer must reproduce every number from two commands |

Rejected alternatives and why (full table in doc 10 §10): Next.js, Firebase/Supabase-only,
MongoDB, Qualtrics/Google Forms/Typeform, Redux/Zustand, pure-Python IRT, `reticulate`/`rpy2`,
single shared database. All ruled out by a specific hard constraint, not preference — worth
keeping that framing if anyone questions the stack later.

**Cost ceiling at this scale: ~₹0–1,000/year.** Free tiers throughout until N (and therefore
traffic/storage) outgrows them.

---

## 3. What "done" looks like for each subsystem

Pulling the acceptance bar out of the gates in `07-roadmap.md` so it reads as a checklist:

- **Consent flow**: layered (summary → expandable detail → downloadable full sheet),
  granular unchecked-by-default checkboxes, open-data consent separated from research
  consent, no dark patterns. Reviewed by someone other than you before Gate 0.
- **Timing subsystem**: latency verified against an external scripted-responder clock
  before pilot; confounds captured every time (device, input method, viewport, reading-speed
  baseline, focus-loss flag).
- **Data model**: two-store separation with no joinable key held inside either system;
  participant codes are random UUIDs with zero derivation; quasi-identifiers banded
  (age band, state not city, education band).
- **Withdrawal/deletion**: a real delete, tested to actually work, before any real
  participant's data exists — not a "flag" and not deferred to "later."
- **De-identified export**: k-anonymity check (collapse categories until k ≥ 5), fresh
  sequential public IDs (never reuse internal `participant_code`), free-text (M2) screened
  for re-identifying content.
- **Item bank**: desirability spread ≤ 0.5 enforced as a CI build check, not a manual review step.

---

## 4. Consolidated build order

Merging the sequencing from `03-platform-architecture.md` §"What to build first",
`10-tech-stack-and-system-design.md` §9, and `07-roadmap.md` Phase 0–1 into one
concrete list. Strictly sequential — each step depends on the ones above it.

1. Repo, CI, item-bank validation (desirability-spread check wired in from commit 1)
2. Data model + Alembic migrations, both Postgres instances
3. Consent flow (nothing may be collected before this exists)
4. Timing subsystem + reading-speed baseline task (verify against external clock)
5. Session creation + server-side stratified condition assignment
6. M1 item pool (~120 statements) + desirability rating study (n=30–50) run in parallel
7. M1 delivery UI, with the offline IndexedDB queue
8. Response ingest and storage
9. Withdrawal/deletion endpoint — **test before any real participant exists**
10. De-identified export pipeline — **before there is data to export**
11. Stage A feedback screen (descriptive only — no trait scores; see doc 08)
12. Admin monitoring dashboard (N per channel/condition, completion, dropout, timeout rate)
13. → **Pilot** (N 40–80): calibrate the 12s timing, trim dead items, freeze item bank v1.0
14. Then, and only after M1 works end-to-end: M3, then M2, then M4/M5

---

## 5. Open decisions that block later phases

Carried forward from `PI/README.md` §"Open questions to resolve before Phase 1" —
these are yours to decide, not engineering choices:

1. **Ethics oversight** — which institution/department, or constitute the 3–5 person
   independent panel? This has the longest lead time in the whole project (Gate 0);
   start it now regardless of anything else.
2. **Within-sample Likert comparison** — worth the extra cost? It would materially
   strengthen H1 (currently a comparison against literature benchmarks, which is
   weaker evidence than a same-sample format comparison).
3. **NGO channel regional language** — which language, and who does forward/back
   translation? Needed before Wave 2 recruitment (`05-recruitment-plan.md`).
4. **External marker inventory for H5 convergent validity** — which established
   Big-Five-type instrument, and on what subsample size? Without this, there is no
   evidence the four M1 dimensions measure what they claim.

I'd suggest resolving #1 first since it gates everything else — want me to draft
outreach material for faculty/IRB contact, or help scope the independent-panel
fallback instead?

---

## 6. Risks worth restating (from the charter's risk register)

The two with **High** likelihood and **High** impact both concern the NGO channel:
consent quality being challenged, and the temptation to relax recruitment standards
if N stalls short of target. Both have concrete mitigations already written
(`02-ethics-and-consent.md`) — the discipline required is procedural, not technical.
The single most avoidable failure mode named across every document is the same one,
restated in different words each time: **do not collect data before consent, timing
verification, and deletion capability are all actually working**, not "will be added later."

---

## 7. Related documents (full detail lives here, this plan only summarises)

- `00-project-charter.md` — scope, research questions, success criteria
- `01-instrument-design.md` — module-by-module item design
- `02-ethics-and-consent.md` — **read first if touching recruitment**
- `03-platform-architecture.md` — original architecture draft (superseded by 10 on stack specifics)
- `04-data-schema.md` — storage model, item bank versioning, export pipeline
- `05-recruitment-plan.md` — channel strategy, sampling, bias analysis
- `06-analysis-plan.md` — pre-registration draft, H1–H6, statistical spec
- `07-roadmap.md` — phased execution, gates, decision triggers
- `PI/08-participant-feedback.md` — report design, Barnum-effect controls
- `PI/09-calibration-methodology.md` — TIRT calibration, anchor linking
- `10-tech-stack-and-system-design.md` — full architecture decision record (source for §2 above)

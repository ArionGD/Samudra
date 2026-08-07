# Technical Stack and System Design

**Status:** Draft v0.1
**Supersedes the stack table in:** `03-platform-architecture.md`
**Companion to:** `04-data-schema.md`, `06-analysis-plan.md`, `09-calibration-methodology.md`

---

## 1. What the architecture has to survive

Before choosing anything, the constraints that actually determine the design:

| Constraint | Consequence |
|---|---|
| **Millisecond timing accuracy** | Client-side measurement, no network in the critical path, no SSR |
| **Mobile-first, Indian network conditions** | Offline tolerance, small bundles, no assumption of stable connectivity |
| **Zero/near-zero budget** | Free tiers, and the ability to migrate when you outgrow them |
| **Solo maintainer** | Every dependency is one you maintain alone. Boring beats clever |
| **Data protection obligations** | Encryption, deletion capability, store separation |
| **Condition assignment must be trustworthy** | Randomisation cannot live in the client |
| **Analysis needs Thurstonian IRT** | R is mandatory, not a preference |

The last two are the ones that actually eliminate otherwise-attractive options.

---

## 2. Stack at a glance

```
┌─────────────────────────────────────────────────────────┐
│  CLIENT                                                  │
│  React 18 + Vite + TypeScript + Tailwind                │
│  ├─ timing/     performance.now(), rAF anchoring        │
│  ├─ modules/    M1–M5 delivery                          │
│  ├─ offline/    IndexedDB queue                         │
│  └─ consent/    layered consent flow                    │
│  Hosted: Cloudflare Pages (static)                      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS / JSON
┌────────────────────────┴────────────────────────────────┐
│  API                                                     │
│  FastAPI (Python 3.12) + SQLAlchemy 2.0 + Pydantic v2   │
│  ├─ /session      create, assign condition (server-side)│
│  ├─ /responses    batched ingest                        │
│  ├─ /feedback     Stage A/B report generation           │
│  ├─ /withdraw     deletion on request                   │
│  └─ /admin        export, monitoring (auth required)    │
│  Hosted: Fly.io (container)                             │
└──────────┬──────────────────────────┬───────────────────┘
           │                          │
┌──────────┴───────────┐   ┌──────────┴───────────────────┐
│  RESEARCH STORE      │   │  CONTACT STORE               │
│  PostgreSQL (Neon)   │ ✗ │  PostgreSQL (separate)       │
│  no identifiers      │   │  emails only, short-lived    │
└──────────┬───────────┘   └──────────────────────────────┘
           │ de-identified CSV export
┌──────────┴──────────────────────────────────────────────┐
│  ANALYSIS (offline, local or Colab)                      │
│  Python: cleaning, descriptives, semantic scoring        │
│  R: thurstonianIRT (Stan/lavaan), lavaan CFA, lme4       │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Frontend

### Choice: React 18 + Vite + TypeScript

**Why React:** you know the ecosystem, the component model fits a module-based assessment, and the hooks API gives you clean control over the render/measure cycle that timing depends on.

**Why Vite, not Next.js.** This is a deliberate rejection worth explaining, because Next is the default answer for React projects in 2026 and it's wrong here.

- **SSR buys nothing.** There's no content to index, no SEO surface, no shared state to hydrate. Every participant session is a private interactive experience.
- **SSR actively harms the core requirement.** Hydration timing is unpredictable, and the moment an item becomes visible versus interactive can diverge. Your entire timing subsystem depends on knowing exactly when a participant could first respond.
- **Static output is free to host and trivially fast.** Cloudflare Pages serves the whole bundle from edge locations, which matters for consistent load times across an Indian sample on varied connections.

**Why TypeScript:** you're encoding item bank structures, response payload shapes that differ per module, and condition enums. Getting these wrong produces data corruption you discover at analysis time. Types catch it at compile time.

### The timing subsystem — the technically critical component

Build this first. It cannot be retrofitted, and two of your four hypotheses depend on it.

**Rules:**

1. **`performance.now()`, never `Date.now()`.** Wall-clock time is subject to NTP correction mid-session and has coarser resolution. `performance.now()` is monotonic and sub-millisecond.

2. **Anchor to paint, not to state change.** The clock starts when the participant could actually see the item.

```typescript
// timing/useItemTimer.ts
export function useItemTimer(itemId: string) {
  const shownAtRef = useRef<number | null>(null);
  const focusLostRef = useRef(false);

  useEffect(() => {
    shownAtRef.current = null;
    focusLostRef.current = false;

    // First rAF fires before paint; second fires after.
    const raf1 = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        shownAtRef.current = performance.now();
      });
    });

    const onVisibility = () => {
      if (document.hidden) focusLostRef.current = true;
    };
    document.addEventListener('visibilitychange', onVisibility);

    return () => {
      cancelAnimationFrame(raf1);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, [itemId]);

  const capture = useCallback(() => ({
    latencyMs: shownAtRef.current
      ? Math.round(performance.now() - shownAtRef.current)
      : null,
    focusLost: focusLostRef.current,
  }), []);

  return { capture };
}
```

3. **Preload the entire module before it starts.** No network request may occur between items. A participant on a slow connection must not have their latency contaminated by a fetch.

4. **Capture the confounds, always.** Device type, input method, viewport width, focus-loss flag, and the reading-speed baseline. Without the baseline, latency data is uninterpretable — see `06-analysis-plan.md`, H3.

5. **Verify against an external clock.** During development, run a scripted responder at known intervals and confirm recorded latencies match. Do this before the pilot, not after.

### Offline resilience

Indian mobile connectivity makes disconnection a normal case, not an edge case.

- Queue responses in **IndexedDB** as they occur
- Flush to the API in batches of ~5, or on module completion
- Retry with exponential backoff
- Never hold a full module in memory awaiting a single submit — mobile browsers kill backgrounded tabs and you will lose sessions

Use `idb-keyval` rather than raw IndexedDB. The native API is unpleasant and you don't need its power.

### State management

Plain React state plus context. **Do not add Redux, Zustand, or similar.** A session is short-lived, linear, and has no cross-cutting state. Adding a state library here is complexity with no payoff.

### Styling

Tailwind, mobile-first by default. Design for a **360px viewport** as the primary target — that's where most of your sample will be.

Accessibility is not optional for a research instrument: keyboard navigable, screen-reader labelled, sufficient contrast, and a countdown timer that is visible without being alarming. A timer that induces panic is measuring anxiety, not the construct.

---

## 4. Backend

### Choice: FastAPI + SQLAlchemy 2.0 + Pydantic v2

**Why FastAPI:** you're already in Python, so the analysis code and the API share a language and you can reuse scoring logic. Async handles concurrent submissions without thread pools. Pydantic validation at the boundary catches malformed payloads before they hit the database. OpenAPI docs generate themselves.

**Why not a serverless BaaS with no backend at all.** Supabase or Firebase with client-side writes is genuinely tempting — less to build, less to host, less to maintain. Two things kill it:

- **Condition assignment must be server-side.** If randomisation runs in the client it is manipulable, and you will get unbalanced cells with no explanation. This is a research-validity issue, not an engineering preference.
- **Item bank version must be server-controlled.** The server decides what a participant sees and records it immutably. Client-declared version is not evidence.

There is enough trusted logic here to justify a small API. It's perhaps 800 lines.

### Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/session` | POST | Create session, assign condition (stratified by channel), return module payload |
| `/session/{id}/responses` | POST | Batched response ingest |
| `/session/{id}/complete` | POST | Mark complete, trigger feedback generation |
| `/feedback/{id}` | GET | Stage A or B report |
| `/withdraw` | POST | Delete participant data on request |
| `/admin/export` | GET | De-identified extract (authenticated) |
| `/admin/monitor` | GET | N per channel per condition, completion rates |

### Condition assignment

Stratified randomisation, server-side, immutable once assigned:

```python
async def assign_condition(channel: str, session: AsyncSession) -> Condition:
    """Assign to the least-populated cell within this channel."""
    counts = await session.execute(
        select(Session.condition, func.count())
        .join(Participant)
        .where(Participant.recruitment_channel == channel)
        .group_by(Session.condition)
    )
    tally = {c: 0 for c in Condition}
    tally.update(dict(counts.all()))
    fewest = min(tally.values())
    candidates = [c for c, n in tally.items() if n == fewest]
    return random.choice(candidates)
```

Simple randomisation with unequal channel yields produces imbalanced cells. Minimisation like this keeps them even without introducing predictability, since ties are broken randomly.

### Item bank loading

Item banks live as **versioned YAML in git**, not in the database. Loaded into memory at startup and served from there.

Reasons this matters: item content is reviewable in pull requests, changes are diffable and attributable, and the desirability-spread validation runs as a CI check that fails the build if any block exceeds threshold. Item content in a database drifts silently; item content in git does not.

```yaml
# items/M1/v1.0.0/blocks.yaml
- block_id: blk_003
  statements: [stmt_047, stmt_112, stmt_088]
  dimensions: [CON, COO, STR]
  desirability_spread: 0.4   # computed and CI-enforced ≤ 0.5
  time_limit_ms: 12000
```

---

## 5. Database

### Choice: PostgreSQL, two separate instances

**Why Postgres over the alternatives:**

- **vs. MongoDB** — your data is relational. Participants have sessions, sessions have responses, responses reference items and item versions. That's a join-heavy structure. Mongo would give you schema flexibility you partly need and cost you the referential integrity you fully need.
- **vs. SQLite** — fine at your scale technically, but makes the two-store separation awkward, complicates concurrent writes from a hosted API, and gives you no managed backups.
- **vs. a spreadsheet or CSV accumulation** — no integrity, no concurrent write safety, no deletion guarantees. Not viable for consented human-subjects data.

**The JSONB argument.** Response payloads differ fundamentally by module — a forced-choice triplet is `{most, least}`, a divergent-thinking response is a list of strings with a keystroke count. Three bad options and one good one:

| Approach | Problem |
|---|---|
| Five separate response tables | Every cross-module query becomes a five-way union |
| One wide sparse table | Mostly nulls, painful to extend |
| Serialise to a text blob | Unqueryable |
| **JSONB column** | ✅ Queryable, indexable with GIN, schema-flexible where it should be |

You get relational structure where structure is real, and document flexibility exactly where the data genuinely varies. This is the case Postgres's JSONB was built for.

### The two-store separation

```
RESEARCH STORE                    CONTACT STORE
(Neon instance A)          ✗      (Neon instance B, or none)
participant_code (UUID)   no      contact_id
responses, timings       join     email
demographics (banded)             delivery_flag
```

**Never joinable without a key held outside both systems.** Ideally, don't hold the link at all: send the feedback email at session end and store only a delivery flag, so the association never persists.

The threat model is simple — a breach of the research store must not reveal who gave which answers.

### Hosting

**Neon** free tier for both. Reasons: managed Postgres with no platform lock-in, branching (a genuinely useful feature — branch the database to test a migration), autosuspend so the free tier lasts, and standard Postgres so migration elsewhere is trivial.

Supabase is the alternative and its free tier is generous, but you'd be adopting a whole platform when you need one component.

**Verify encryption at rest is enabled.** Most managed providers do this by default; confirm rather than assume, because you'll be asserting it in your consent materials.

### Migrations

**Alembic**, from the first table. Not optional. You will change the schema mid-project, and doing it by hand against a database containing consented participant data is how data gets destroyed.

### Indexing

```sql
CREATE INDEX idx_responses_session   ON responses(session_id);
CREATE INDEX idx_responses_item      ON responses(item_id, item_bank_version);
CREATE INDEX idx_sessions_condition  ON sessions(condition);
CREATE INDEX idx_participants_channel ON participants(recruitment_channel);
CREATE INDEX idx_responses_payload   ON responses USING GIN (response_payload);
```

The GIN index only earns its cost if you query into the JSONB. Add it when you need it.

---

## 6. Analytics

### The split: Python for everything except IRT, R for IRT

This is not a preference. `thurstonianIRT` is the only mature implementation of the model your entire design depends on, and `lavaan` is the standard for the confirmatory work. Trying to stay in one language would cost months and produce a worse result.

| Job | Tool | Why |
|---|---|---|
| Cleaning, exclusions, descriptives | Python (pandas, polars) | Shares code with the API |
| Semantic-distance originality (M2) | Python (sentence-transformers) | The ML ecosystem lives here |
| **TIRT calibration** | **R (`thurstonianIRT`)** | Only mature implementation |
| CFA, invariance testing | **R (`lavaan`)** | Standard in the field |
| Mixed-effects latency models | R (`lme4`) or Python (`statsmodels`) | R has better random-effects tooling |
| Simulation study | R (`sim_TIRT_data`) | Built into the package |
| Visualisation | Either | `ggplot2` if you're already in R |

### The boundary: export, don't interop

Resist `reticulate` or `rpy2`. Cross-language in-process interop is fragile, hard to debug, and hostile to reproduction by anyone else.

Instead, make the boundary a **de-identified CSV extract**:

```
export/
├── participants.csv       # banded demographics, channel, consent flags
├── sessions.csv           # condition, device, order, completion
├── responses.csv          # item-level, with latency and flags
├── reading_baseline.csv   # chars/sec per participant
└── data_dictionary.md
```

Python produces it. R consumes it. Anyone can reproduce either half independently. This is also exactly the artefact you'd publish as an open dataset, so building it early costs nothing extra.

### Analysis pipeline

```
analysis/
├── python/
│   ├── 01_load_extract.py
│   ├── 02_apply_exclusions.py      # pre-specified, condition-blind
│   ├── 03_descriptives.py
│   ├── 04_m2_semantic_scoring.py
│   └── out/clean_extract.csv
├── R/
│   ├── 00_simulation_study.R       # run BEFORE collection
│   ├── 01_tirt_calibration.R
│   ├── 02_cfa_structure.R
│   ├── 03_invariance.R
│   ├── 04_hypothesis_tests.R
│   └── renv.lock
└── notebooks/                       # exploratory only, clearly labelled
```

**Run `00_simulation_study.R` before collecting anything.** It tells you your real sample-size requirement rather than a borrowed rule of thumb. See `09-calibration-methodology.md`.

### Reproducibility

- **`renv`** for R, **`uv`** with a lockfile for Python
- Seeds set explicitly in every script that randomises
- Raw extract never modified in place — every transformation produces a new file
- Analysis code public; data public only for the consented subset

A reviewer should be able to clone the repo, run two commands, and reproduce every number in the write-up. That is the difference between publishable and merely finished.

---

## 7. Security and operations

| Area | Implementation |
|---|---|
| Transport | TLS enforced, HSTS enabled |
| At rest | Provider encryption on both stores — verify, don't assume |
| Secrets | Environment variables only; pre-commit hook to block accidental commits |
| Admin auth | Single admin account, strong credentials, rate-limited. No user accounts exist for participants |
| Rate limiting | Per-IP on session creation; IPs held only for the rate-limit window, never stored with responses |
| Dependencies | Dependabot enabled — you're solo and won't notice CVEs otherwise |
| Backups | Neon automated backups; periodic manual export to encrypted local storage |
| Deletion | `/withdraw` performs a real delete, not a flag. Test this before launch |
| Monitoring | Simple uptime check plus weekly N-per-cell report |

**Never analyse on production data.** Export the de-identified extract and work on that. This is both a security control and a discipline that keeps you honest about what the published dataset actually contains.

---

## 8. Cost

| Component | Tier | Cost |
|---|---|---|
| Cloudflare Pages | Free | ₹0 |
| Fly.io (1 shared CPU, 256MB) | Free allowance | ₹0 |
| Neon × 2 | Free | ₹0 |
| Domain | — | ~₹1,000/yr |
| Analysis | Local machine or Colab | ₹0 |

The whole thing runs at essentially the cost of a domain, which it should at this scale. If you outgrow the free tiers you've succeeded beyond projection, and paid tiers start around ₹500–800/month.

---

## 9. Build order

Strictly sequential. Each item depends on the ones before it.

1. **Repo, CI, item-bank validation** — including the desirability-spread build check
2. **Data model and Alembic migrations** — both stores
3. **Consent flow** — nothing may be collected before this exists
4. **Timing subsystem + reading-speed baseline** — the hard part, verified against an external clock
5. **Session creation and condition assignment** — server-side
6. **M1 delivery** — with offline queue
7. **Response ingest and storage**
8. **Withdrawal/deletion endpoint** — test it works before any real participant exists
9. **De-identified export** — before there is data to export
10. **Stage A feedback screen**
11. **Admin monitoring**
12. *Then* pilot

Items 8 and 9 look like they belong later. They don't. If you cannot delete a participant's data on request, you are not compliant with what your own consent form promises — and discovering that at N=300 is an expensive problem.

---

## 10. Rejected alternatives, and why

Recording these so the reasoning survives:

| Rejected | Reason |
|---|---|
| Next.js | SSR harms timing precision, provides nothing this project needs |
| Firebase / Supabase-only (no backend) | Condition assignment must be server-side and trustworthy |
| MongoDB | Data is relational; JSONB covers the flexibility need |
| Qualtrics / Google Forms / Typeform | No millisecond timing, no forced-choice triplets, third-party data hosting complicates DPDP position |
| Redux / Zustand | Session state is linear and short-lived |
| Pure-Python IRT | No mature Thurstonian implementation exists |
| `reticulate` / `rpy2` | Fragile interop; a CSV boundary is more reproducible |
| Single database for all data | Breach of responses would reveal identities |

---

## 11. What makes this a portfolio artefact

Since one purpose of the project is demonstrating capability, the parts worth documenting well:

- **The timing subsystem.** Genuinely non-trivial, rarely done correctly, and explaining rAF double-anchoring shows you understand the render pipeline rather than just using it.
- **The two-store privacy architecture.** Most projects handling personal data don't think this hard about breach consequences.
- **Server-side stratified randomisation.** Shows you understand why research validity is an engineering concern.
- **The Python/R boundary via reproducible extract.** Demonstrates analytical range and reproducibility discipline.
- **Item bank as versioned, CI-validated config.** Treating research content as code is an unusual and defensible choice.

Write the README for a technically literate reader who has never heard of Thurstonian IRT. If it explains why the design is what it is, it is worth more than the code.

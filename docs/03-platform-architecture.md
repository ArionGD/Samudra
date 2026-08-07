# Platform Architecture

**Status:** Draft v0.1

---

## Constraints that shape everything

- **Zero or near-zero hosting budget.** Free tiers only, at least until N justifies spending.
- **Solo developer.** Every dependency is something you maintain alone.
- **Millisecond-accurate timing required.** This is the hard technical constraint and it drives several decisions.
- **Mobile-first.** In an Indian sample, most participants will be on phones. Design for a 360px viewport and unreliable connectivity.
- **Data protection obligations.** Encryption, access control, deletion capability are requirements, not nice-to-haves.

---

## Stack recommendation

| Layer | Choice | Why |
|---|---|---|
| Frontend | **React + Vite**, TypeScript | Timing precision requires client-side control; you know the ecosystem |
| Styling | Tailwind | Fast, mobile-first by default |
| Backend | **FastAPI** (Python) | You're already in Python; async handles concurrent submissions; auto-generated API docs |
| Database | **PostgreSQL** (Supabase or Neon free tier) | Relational fits the schema; JSONB for flexible response payloads |
| Hosting — frontend | Cloudflare Pages or Vercel | Free, global CDN, matters for latency consistency |
| Hosting — backend | Fly.io or Railway free tier | Container-based, easy to move |
| Analysis | **R** for TIRT (`thurstonianIRT`), **Python** for everything else | The IRT tooling lives in R; don't fight it |

**Deliberately avoided:** any managed survey platform (Qualtrics, Google Forms, Typeform). They cannot deliver reliable millisecond timing, they don't support forced-choice triplets natively, and hosting participant data on a third-party US service complicates your DPDP position.

---

## The timing problem — read this carefully

This is where most home-built assessment platforms silently fail. Your RQ3 and RQ4 both depend on timing data being trustworthy.

### Rules

**Measure client-side, always.** Server round-trip time is dominated by network variance and tells you nothing about the participant.

**Use `performance.now()`, never `Date.now()`.** `Date.now()` is wall-clock time, subject to NTP adjustment mid-session and only millisecond-resolution at best. `performance.now()` is monotonic and sub-millisecond.

**Anchor to render, not to state change.** The clock starts when the item is actually painted, not when React sets state. Use `requestAnimationFrame` to capture the post-paint timestamp.

```typescript
const [shownAt, setShownAt] = useState<number | null>(null);

useEffect(() => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => setShownAt(performance.now()));
  });
}, [itemId]);

const handleResponse = (choice: string) => {
  const latencyMs = shownAt ? performance.now() - shownAt : null;
  recordResponse({ itemId, choice, latencyMs });
};
```

The double `requestAnimationFrame` is deliberate — the first fires before paint, the second after.

**Preload everything.** No network request between items. Fetch the entire module payload up front. A participant on a slow connection must not have their latency data contaminated by loading delays.

**Capture the confounds** — these are as important as the latency itself:
- Device type and input method (touch vs. mouse)
- Viewport width
- A reading-speed baseline task (present neutral sentences, measure read time)
- Whether the tab lost focus mid-item (`visibilitychange`) — flag and exclude these responses

Without the reading-speed baseline, your latency analysis is uninterpretable. Build it in from the start; it cannot be added retroactively.

---

## Application flow

```
Landing → Consent (layered) → Age gate → Demographics (minimal)
   → Reading-speed baseline → Practice block
   → [Randomised module subset] → Optional continue
   → Feedback screen → Optional email capture (separate store)
```

### Design notes

**No account required.** Registration kills completion rates and creates identifiable data you don't need. Use an anonymous session token in localStorage so a participant can resume, but never require login.

**Randomise condition assignment server-side.** Client-side randomisation is manipulable and produces unbalanced cells. The server assigns condition on session creation and records it immutably.

**Save incrementally.** Post each item response as it happens, or batch every few items. Do not hold a full module in memory and submit at the end — mobile browsers kill backgrounded tabs and you will lose data.

**Handle disconnection.** Queue responses in IndexedDB when offline, flush on reconnect. In Indian mobile conditions this is not an edge case.

---

## Anti-abuse

An open, unauthenticated research site attracts junk data. Minimum viable defences:

- **Rate limiting** per IP (but don't store IPs beyond the rate-limit window)
- **Attention checks** — one or two per module, e.g. an item that instructs "select the third option." Flag but don't auto-delete; decide exclusion rules in the analysis plan, in advance.
- **Latency floor** — responses under ~300ms on a reading-required item indicate non-engagement
- **Straight-lining detection** — identical response patterns across a module
- **Duplicate detection** — same session token, same device fingerprint hash (a coarse one; don't build an actual fingerprinting system)

Log these as quality flags in the data, and pre-specify exclusion criteria. Deciding exclusions after seeing results is p-hacking.

---

## Security baseline

- **TLS everywhere**, HSTS enabled
- **Encryption at rest** on the database (most managed Postgres providers do this by default — verify it)
- **Separate stores** for response data and any contact data. Different databases, ideally different providers. They should not be joinable without a key you hold outside both systems.
- **No production data locally.** Analyse on exported, de-identified extracts.
- **Access logging** on the admin interface
- **No secrets in the repo.** Environment variables only, and add a pre-commit hook to catch accidents.
- **Dependency scanning** — Dependabot or equivalent, since you're solo and won't notice CVEs otherwise

---

## Repository structure

```
assessment-platform/
├── frontend/
│   ├── src/
│   │   ├── modules/          # M1..M5, one directory each
│   │   ├── timing/           # performance.now wrappers, baseline task
│   │   ├── consent/          # layered consent components
│   │   └── api/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/           # SQLAlchemy
│   │   ├── randomisation/    # condition assignment
│   │   └── export/           # de-identified extract generation
│   └── migrations/
├── analysis/
│   ├── R/                    # thurstonianIRT calibration
│   ├── python/               # cleaning, descriptives, semantic scoring
│   └── notebooks/
├── items/                    # item banks as versioned YAML/JSON
├── docs/                     # these documents
└── README.md
```

**Version the item banks in git.** You need to know exactly which item text each participant saw. Item wording changes mid-study are a real threat to data integrity, and if you must change something, treat it as a new instrument version.

---

## Portfolio angle

Since one purpose here is demonstrating capability, a few things are worth doing well because they show well:

- **The timing subsystem** is genuinely non-trivial engineering. Document it properly; it's the most technically interesting part.
- **Semantic-distance originality scoring** for M2 is a nice self-contained ML component.
- **The TIRT calibration pipeline** — R called from a reproducible Python workflow — demonstrates real analytical range.
- **Open-source the platform** (not the data). A working, documented assessment platform is a much stronger portfolio artefact than a CLI utility.

Write the README as if a hiring manager will read it, because one might.

---

## What to build first

1. Consent flow and data model — nothing else can be collected legitimately without it
2. Timing subsystem and reading-speed baseline
3. M1 delivery and storage
4. Admin export to de-identified extract
5. Feedback screen
6. Everything else

Resist building all five modules before validating that one works end to end with real participants.

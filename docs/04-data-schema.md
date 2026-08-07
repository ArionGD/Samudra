# Data Schema

**Status:** Draft v0.1

---

## Principle: two separate worlds

The single most important structural decision is that **response data and contact data never live in the same database.**

```
┌─────────────────────────┐        ┌──────────────────────────┐
│   RESEARCH STORE        │        │   CONTACT STORE          │
│   (no identifiers)      │   ✗    │   (emails only)          │
│                         │ ←────→ │                          │
│   participant_code      │  no    │   contact_id             │
│   responses, timings    │  join  │   email, consent flags   │
└─────────────────────────┘        └──────────────────────────┘
```

If a participant asks for results by email, the link between their `participant_code` and their email is held in a **third, minimal store** with restricted access — or, better, not held at all: send results immediately at session end and store only the email against a delivery flag.

The reason this matters: a breach of the research store should not expose who said what. Design for the breach you hope never happens.

---

## Research store — core tables

### `participants`

| Column | Type | Notes |
|---|---|---|
| `participant_code` | UUID (PK) | Randomly generated, no derivation from anything |
| `created_at` | timestamptz | |
| `recruitment_channel` | enum | `dev_community` / `college` / `ngo` / `professional` / `other` |
| `consent_version` | text | Which consent text version they saw |
| `consent_research` | boolean | Required |
| `consent_open_data` | boolean | Optional, separate |
| `age_band` | enum | `18-24` / `25-34` / `35-44` / `45-54` / `55+` — bands, not exact age |
| `education_band` | enum | Coarse |
| `state` | text | State level only, never city |
| `primary_language` | text | |
| `work_status` | enum | `student` / `employed` / `self_employed` / `not_working` / `prefer_not_to_say` |
| `withdrawn` | boolean | Soft-delete flag |
| `withdrawn_at` | timestamptz | |

**Deliberately absent:** name, email, phone, exact date of birth, city, employer, job title, IP address, gender at first launch.

On gender: you may want it for demographic reporting, and it is defensible to collect with a `prefer_not_to_say` option. But be clear what analysis needs it. If the answer is "completeness," don't collect it.

On quasi-identifiers: `age_band` + `state` + `education_band` + `recruitment_channel` could still identify someone in a small NGO subsample. Check k-anonymity before any release.

### `sessions`

| Column | Type | Notes |
|---|---|---|
| `session_id` | UUID (PK) | |
| `participant_code` | UUID (FK) | |
| `started_at` / `completed_at` | timestamptz | |
| `condition` | enum | `honest_untimed` / `honest_timed` / `fake_timed` / `fake_untimed` |
| `module_order` | text[] | Actual presentation order |
| `device_type` | enum | `mobile` / `tablet` / `desktop` |
| `input_method` | enum | `touch` / `mouse_keyboard` |
| `viewport_width` | int | |
| `user_agent_family` | text | Parsed family only — not the full UA string |
| `completed` | boolean | |
| `abandoned_at_module` | text | Nullable — dropout analysis |

Condition is assigned **server-side at session creation** and never changes.

### `reading_baseline`

Critical for latency analysis. Do not treat as optional.

| Column | Type | Notes |
|---|---|---|
| `session_id` | UUID (FK) | |
| `sentence_id` | text | |
| `char_count` | int | |
| `read_time_ms` | int | |

Derive `chars_per_second` per participant and use it as a covariate in every latency model.

### `responses`

The main table. One row per item response.

| Column | Type | Notes |
|---|---|---|
| `response_id` | UUID (PK) | |
| `session_id` | UUID (FK) | |
| `module_code` | enum | `M1`..`M5` |
| `item_id` | text | References versioned item bank |
| `item_bank_version` | text | **Essential** — which wording they saw |
| `position_in_module` | int | Order effects |
| `response_payload` | JSONB | Format varies by module — see below |
| `latency_ms` | int | From paint to response |
| `timed_out` | boolean | |
| `focus_lost` | boolean | Tab was backgrounded during item |
| `revisions` | int | How many times they changed their answer before confirming |
| `created_at` | timestamptz | |

`revisions` is worth capturing and rarely is. Changing your answer is plausibly related to deliberation and possibly to distortion — it's a free variable that might turn out interesting.

### `response_payload` shapes

```jsonc
// M1 — forced-choice triplet
{ "most": "stmt_047", "least": "stmt_112" }

// M2 — divergent thinking
{ "prompt": "brick",
  "responses": ["build a wall", "paperweight", "break a window"],
  "keystroke_count": 84 }

// M3 — critical reasoning
{ "selected": "c", "correct": "c" }

// M4 — SJT
{ "most_effective": "b", "least_effective": "a" }

// M5 — ethical judgement
{ "selected": "a", "scenario_pair_id": "pair_09" }
```

Use JSONB rather than a wide sparse table. Query with GIN indexes where needed.

### `quality_flags`

| Column | Type | Notes |
|---|---|---|
| `session_id` | UUID (FK) | |
| `flag_type` | enum | `attention_check_failed` / `straight_lining` / `latency_floor` / `excessive_timeouts` / `duplicate_suspected` |
| `detail` | JSONB | |
| `created_at` | timestamptz | |

**Flags are recorded, not acted on.** Exclusion happens at analysis time, using rules specified in the pre-registration. Never delete flagged data from the store.

---

## Item bank — versioned, in git

Item banks live as YAML in the repository, not in the database. They're versioned, reviewable, and diffable.

```yaml
# items/M1/v1.2.0/statements.yaml
- id: stmt_047
  dimension: CON
  text: "I keep a written plan for the week ahead."
  desirability_mean: 5.2
  desirability_sd: 0.9
  desirability_n: 41
  keyed: positive

- id: stmt_112
  dimension: COO
  text: "I let others take the lead in group decisions."
  desirability_mean: 4.9
  desirability_sd: 1.1
  desirability_n: 41
  keyed: positive
```

```yaml
# items/M1/v1.2.0/blocks.yaml
- block_id: blk_003
  statements: [stmt_047, stmt_112, stmt_088]
  dimensions: [CON, COO, STR]
  desirability_spread: 0.4      # max - min; keep under 0.5
  time_limit_ms: 12000
```

Compute `desirability_spread` automatically and **fail the build** if any block exceeds threshold. That's a validation rule worth enforcing in CI — it's the design constraint most likely to erode silently as you add items.

---

## Derived tables (analysis outputs)

Keep these separate from raw data. Regenerable, never authoritative.

- `m1_trait_estimates` — TIRT theta estimates per participant per dimension, with standard errors
- `m2_scores` — fluency, flexibility, originality (both frequency-based and semantic)
- `m3_scores` — total correct, by item family
- `m5_orientation` — orientation scores plus consistency index

---

## Export pipeline

The de-identified extract for analysis and possible release:

1. Filter to `withdrawn = false` and `consent_research = true`
2. For public release, additionally filter to `consent_open_data = true`
3. Drop `participant_code`, replace with a fresh sequential ID generated at export time — so the public ID cannot be linked back
4. Screen all free text (M2 responses) for anything identifying
5. Check k-anonymity on the demographic combination; collapse categories until k ≥ 5
6. Emit CSV plus a data dictionary
7. Record the export in an audit log

Step 3 is easy to skip and important. If the public dataset uses the same participant codes as your internal store, the two are joinable by anyone who obtains both.

---

## Retention

- **Raw response data:** retain for the research period plus a defined archive window; state the figure in the consent form and honour it
- **Contact data:** delete immediately after results are sent
- **Quality flag detail:** same lifetime as responses
- **Withdrawn participants:** hard-delete on request within a stated window; keep only a tombstone record of the deletion event

Write the retention periods into the consent text. Vague retention language ("as long as necessary") is weak under DPDP and weak ethically.

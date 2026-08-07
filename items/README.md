# Item banks

Versioned, reviewable item content — YAML in git, not database rows. See
[`../docs/04-data-schema.md`](../docs/04-data-schema.md) and
[`../ARCHITECTURE.md`](../ARCHITECTURE.md) for why.

```
items/
└── M1/
    └── v0.1.0-placeholder/
        ├── statements.yaml   # individual statements, with desirability ratings
        └── blocks.yaml       # triplets referencing statement IDs, with time limits
```

## Rules that CI should eventually enforce

`backend/app/items/loader.py` exposes `validate_desirability_spread()`,
which computes, for every block, the spread between its three statements'
`desirability_mean` values and flags any block exceeding **0.5**. This is
the single design constraint most likely to erode silently as items get
added — see `../docs/01-instrument-design.md` §"The critical design
constraint". Wire this into CI as a required check before merging any
change under `items/` — not done yet, since there's no CI pipeline
configured at this stage (see `../docs/11-implementation-plan.md`).

## Current status: placeholder only

`M1/v0.1.0-placeholder/` exists so the loader and the frontend wiring demo
have something real to load — it is **not** a reviewed item pool. Real M1
content requires, in order (`../docs/01-instrument-design.md`,
`../docs/09-calibration-methodology.md`):

1. Write ~120 candidate statements, 30 per dimension (CON/STR/COO/DRV).
2. Run a desirability rating study (n=30–50): *"How favourably would an
   employer view someone who agreed with this?"*, 1–7 scale.
3. Assemble triplets within ±0.5 desirability spread; expect to discard
   30–40% of candidate statements.
4. Pilot (N 40–80), cut dead statements, freeze as `v1.0.0` — an anchor
   set that never changes across future recalibrations.

## Versioning

Each participant's response records exactly which `item_bank_version` they
saw (`backend/app/models/research.py`, `Response.item_bank_version`). Once
`v1.0.0` is frozen after piloting (`../docs/07-roadmap.md`, Gate 2), item
wording changes require a new version — never edit a frozen version's YAML
in place.

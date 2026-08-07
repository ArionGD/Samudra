# Frontend

React 18 (via React 19-compatible Vite template) + Vite + TypeScript + Tailwind
v4. Participant-facing delivery: consent, timing, module rendering, offline
queueing. See [`../ARCHITECTURE.md`](../ARCHITECTURE.md) for why this stack
and not Next.js, Redux, or a BaaS.

## Setup

Requires Node 20+.

```bash
cd frontend
npm install
cp .env.example .env.local   # points at the local backend by default
npm run dev
```

The backend must be running (see `../backend/README.md`) for anything past
the consent screen to work — condition assignment happens server-side.

## Build

```bash
npm run build   # tsc -b && vite build
```

Static output only — no SSR, deliberately. See `../ARCHITECTURE.md` §2/§10.

## Structure

```
frontend/
├── src/
│   ├── App.tsx           # Current wiring demo: consent → session → one M1 block → complete
│   ├── timing/
│   │   ├── useItemTimer.ts    # performance.now() + double-rAF paint anchor — read before touching
│   │   └── deviceInfo.ts      # device/input/viewport confound capture
│   ├── modules/
│   │   └── m1/
│   │       └── ForcedChoiceBlock.tsx   # M1 triplet UI (placeholder statements only)
│   ├── offline/
│   │   └── responseQueue.ts   # IndexedDB queue + batched flush with backoff
│   ├── consent/
│   │   └── ConsentScreen.tsx  # Layered consent pattern (placeholder copy — needs ethics review)
│   └── api/
│       ├── client.ts          # Typed fetch wrapper for the backend
│       └── types.ts           # Mirrors backend/app/schemas.py
```

## What's real vs. placeholder right now

- **Real, and not to be casually changed:** the timing hook's double-rAF
  paint-anchoring, the offline queue's persist-then-flush order, the
  consent screen's unchecked-by-default / separate-open-data-checkbox
  pattern.
- **Placeholder, expected to be replaced:** the M1 statements in `App.tsx`
  (`DEMO_BLOCK`), the consent copy (needs ethics-panel review first — see
  `../docs/02-ethics-and-consent.md`), and `App.tsx` itself as a whole,
  which exists to prove the wiring works end-to-end, not as the real
  participant flow (no practice blocks, no countdown, no reading-speed
  baseline yet).

## Environment variables

- `VITE_API_BASE_URL` — backend origin. Defaults to `http://127.0.0.1:8000` if unset.

## Verifying timing before trusting any real data

Per `../ARCHITECTURE.md` §5, rule 5: before the pilot, verify recorded
latencies against an external scripted-responder clock at known intervals.
Not automated yet — do this manually before Gate 2 in
`../docs/07-roadmap.md`.

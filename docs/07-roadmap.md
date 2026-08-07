# Execution Roadmap

**Status:** Draft v0.1

---

## Structure: five phases with hard gates

Each phase ends with a gate. **Do not pass a gate that hasn't been met** — the most common failure mode for solo research projects is accumulating momentum past unmet prerequisites and discovering the problem when the data is already collected and unusable.

---

## Phase 0 — Foundations (Weeks 1–6)

**Nothing here involves participants.** This phase is entirely preparation, and it is the phase most likely to be rushed.

| Task | Notes |
|---|---|
| Approach faculty for ethics affiliation | Start immediately — this has the longest lead time of anything in the project |
| Draft protocol document | Needed for ethics submission |
| Write M1 item pool (~120 statements) | The main creative work; expect to discard 30–40% |
| Draft consent materials, layered | See `02-ethics-and-consent.md` |
| Set up repository, CI, item-bank validation | Including the desirability-spread build check |
| Register OSF account, draft pre-registration | Not submitted yet |

**Gate 0:** ethics arrangement confirmed (institutional or panel constituted, in writing) AND item pool complete AND consent materials reviewed by someone other than you.

*If ethics is still pending at week 6:* continue building the platform, do not collect anything. Building is fine without approval; collecting is not.

---

## Phase 1 — Item calibration and platform (Weeks 7–14)

| Task | Notes |
|---|---|
| Desirability rating study (n=30–50) | Separate, low-risk, minimal consent burden. Can run early |
| Assemble blocks with matched desirability | Automated, with the CI check enforcing spread ≤ 0.5 |
| Build consent flow and data model | First code that touches participants |
| Build timing subsystem | The technically hard part — do it properly, see `03-platform-architecture.md` |
| Build reading-speed baseline task | Not optional; latency analysis is uninterpretable without it |
| Build M1 delivery | |
| Build feedback screen | |
| Build de-identified export | Needed before any data exists, not after |

**Gate 1:** M1 runs end-to-end on a mobile device; timing verified against an external stopwatch; export produces a clean de-identified extract; a full session can be completed and deleted on request.

The deletion test matters. If you can't delete a participant's data on demand, you're not compliant, and finding that out at week 30 is expensive.

---

## Phase 2 — Pilot (Weeks 15–18)

**N target: 40–80**, drawn from the developer channel and personal network. Full consent applies — pilot participants are participants.

What you are looking for:

- **Timing calibration.** Is 12 seconds right for a triplet? Timeout rate above 10% means lengthen; mean response under 5 seconds means you can shorten and strengthen the manipulation.
- **Comprehension.** Do people understand the most/least format? Watch for systematic errors.
- **Dropout points.** Where exactly do people quit?
- **Item behaviour.** Any statement that nobody ever picks, or everybody picks, is dead weight.
- **Desirability matching in practice.** Did the matching actually work, or do some blocks have an obvious "good" answer despite the ratings?
- **Bugs.** There will be many. Mobile Safari especially.

**Gate 2:** timing calibrated with timeout rate under 10%; no critical bugs; item pool trimmed and finalised; **item bank frozen and version-tagged**.

**Freezing the item bank is the point of this gate.** After this, item wording changes require a new instrument version and cannot be pooled with prior data. Take the freeze seriously.

Finalise and submit the OSF pre-registration at the end of this phase — after piloting has informed the design, before main collection begins.

---

## Phase 3 — Main collection (Weeks 19–42)

Roughly six months. Run in two waves.

### Wave 1 (Weeks 19–28) — Developer and college channels

Parallel workstream: translation and NGO protocol development. Start this now, because translation done properly (forward, back, reconciliation) takes longer than expected.

Also in parallel: build M3, then M2. These are cheaper than M1 and can be added mid-collection as separate modules — as long as M1 itself doesn't change.

### Wave 2 (Weeks 29–42) — NGO and professional channels

Requires translation complete, assisted-administration protocol trained, age verification in place.

Build M4 and M5 during this window if item development (critical incidents, SME keying) has progressed.

### Weekly monitoring throughout

Track N per channel per condition, completion rates, dropout points, timeout rates, quality flag rates. **Do not look at trait score distributions or run hypothesis tests.**

**Gate 3:** M1 N ≥ 300 with acceptable data quality; condition cells reasonably balanced; at least two channels well represented.

*If N stalls below 300 by week 42:* extend collection rather than proceeding to underpowered analysis. A delayed project is recoverable; an underpowered one is not.

---

## Phase 4 — Analysis and output (Weeks 43–56)

| Weeks | Task |
|---|---|
| 43–44 | Data cleaning per pre-specified rules, blind to condition |
| 45–48 | TIRT calibration; model fit; reliability |
| 49–52 | Confirmatory tests H1–H6, in order |
| 53–54 | Exploratory analyses, clearly labelled |
| 55–56 | Write-up, preprint, dataset preparation, NGO report |

**Gate 4:** technical report complete including null results; code reproducible from raw extract by someone else; dataset passes k-anonymity check before release.

---

## Realistic timeline

Roughly **14 months** end to end. Compress at your peril — the compressible parts (writing code, running analysis) are not the parts that take longest. Ethics approval, faculty relationships, translation, and participant accumulation all move at their own pace.

---

## Decision points that should change the plan

| Trigger | Action |
|---|---|
| No ethics affiliation by week 10 | Constitute the independent panel and proceed with reduced scope; drop the NGO channel until oversight is genuinely in place |
| Desirability matching fails for a dimension | Rewrite items for that dimension; consider dropping to three dimensions rather than shipping a fakable one |
| Pilot timeout rate > 25% | Time limit is wrong, or items are too long. Rewrite shorter statements |
| N < 200 at week 35 | Drop the invariance hypothesis, focus on H1/H2/H4, extend collection |
| TIRT model fails to converge | Insufficient N or poor block design — return to item analysis, do not force a solution |
| Factor structure doesn't replicate (H4 fails) | **This is a finding.** Report it. Do not respecify the model until it fits and present that as confirmatory |
| Consent concerns raised on any channel | Pause that channel immediately; resolve before resuming |
| Someone offers to buy or license the instrument | Stop. Commercial use requires fresh consent and changes the entire regulatory picture. Do not accept during the research phase |

---

## Minimum viable version

If the full scope proves too large — and it might, alongside a full-time job — here is what to cut, in order:

1. **M5** (ethics module) — highest ethics sensitivity, least essential to the core question
2. **M4** (SJT) — most expensive item development
3. **NGO channel** — most demanding safeguards; keep only if you can do it properly
4. **M2** (divergent thinking) — interesting but peripheral
5. **H6** (invariance) — needs the most N

**What must survive:** M1 with TIRT calibration, the honest-versus-faking experiment, and the timed-versus-untimed comparison. That alone is a complete, publishable study answering a real open question.

The minimum viable version is roughly **eight months** and one module. It is a genuinely good project. Do not let the ambition of the full battery prevent you from finishing the core.

---

## What "done" looks like

- A working, open-source assessment platform with a properly engineered timing subsystem
- One instrument with published calibration, reliability, and structure evidence
- One pre-registered experiment with results reported regardless of direction
- A public dataset with proper consent
- A preprint

That is a substantial and unusual body of work. It demonstrates psychometric competence, engineering capability, and research integrity in a way that no portfolio of utility tools can.

**And it stops short of claiming the instrument is ready for hiring use — because it won't be, and saying otherwise would undo everything the rest of this achieves.**

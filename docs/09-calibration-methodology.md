# Calibration Methodology

**Status:** Draft v0.1
**Companion to:** `01-instrument-design.md`, `06-analysis-plan.md`

---

## What calibration actually means

A raw response — "picked statement 47 over statement 112" — carries no meaning on its own. Calibration is the process of estimating, from a sample, the parameters that convert responses into comparable scores:

- **Item difficulty / utility:** how attractive is this statement in general?
- **Item discrimination:** how strongly does endorsing it relate to the underlying trait?
- **The latent scale:** what distribution are individual estimates placed against?

Without calibration you have a questionnaire. With it, you have an instrument.

### The bootstrap problem

You need item parameters to score people. You need people's responses to estimate item parameters. There is no way around this — every instrument in existence went through an uncalibrated data-collection phase where the responses were useless for scoring and valuable only for calibration.

**Practical consequence:** your first 300 participants are contributing to parameter estimation, not receiving valid scores. Design the participant experience around that honestly (see `08-participant-feedback.md`) rather than pretending otherwise.

---

## How other platforms handle this

Verify these against published technical manuals before citing any of them — I'm working from training knowledge without search access, and vendor methodology changes.

### The large-vendor model (SHL, Hogan, Saville)

Collect very large norming samples — tens of thousands — segmented by country, industry, and job level. Publish technical manuals with reliability and validity evidence. Recalibrate periodically and maintain multiple norm groups so a candidate can be compared against "UK managers" rather than a global mush.

**What's transferable:** the discipline of publishing item parameters and reliability figures, and the practice of naming which norm group a score is compared against.

**What isn't:** the sample sizes. You will not get 30,000 people. Design for a single, honestly-described research norm rather than pretending to have occupational norms.

### The criterion-keyed model (Pymetrics-style)

Rather than calibrating against a general population, train a model on incumbents in a specific role — high performers versus others — and score candidates by similarity. Each client gets a bespoke model.

**What's transferable:** the idea that a score is only meaningful relative to a defined comparison group.

**What isn't:** this requires performance data linking scores to outcomes, which you don't have and won't get in this project. It also has the weakness that it encodes whatever bias existed in past hiring — if the incumbent group is homogeneous, the model learns to select for that homogeneity. Worth understanding as a cautionary case, not a template.

### The open-item-bank model (IPIP)

The International Personality Item Pool put items in the public domain and let researchers accumulate calibration data collectively. Parameters improve as the community contributes.

**This is the closest model to what you should do.** Publishing your item bank and calibration data means others can extend it, and the whole thing becomes a shared resource rather than a one-off study. It also forecloses commercial use — accept that trade deliberately.

### The continuous-recalibration model (Duolingo English Test, adaptive testing generally)

The most technically interesting reference. Large item banks, adaptive item selection, continuous recalibration as new response data arrives, and new items seeded into live administration to accumulate their own parameters before being used for scoring.

**What's transferable, and worth building:**
- **Anchor items** — a fixed core set never changed, so scores remain comparable across versions
- **Seeded new items** — administered but not scored, accumulating data until they have parameters
- **Scheduled recalibration** rather than a single frozen model

This is the design that lets your item bank evolve without invalidating everything collected before. Build for it from the start; retrofitting is painful.

---

## Calibration approach for this project

### Stage 1 — Pre-calibration (before any participant data)

**Desirability rating study.** 30–50 raters score each statement on employer-favourability. This isn't calibration in the IRT sense, but it determines block composition, and blocks that aren't desirability-matched will never calibrate into a fake-resistant instrument no matter how much data you collect.

Output: mean and SD desirability per statement, blocks assembled with spread ≤ 0.5.

### Stage 2 — Pilot calibration (N ≈ 40–80)

Too small for TIRT. What it *is* enough for:

- **Response distribution per statement.** Any statement chosen "most" by under 5% or over 60% of participants is carrying little information — flag for revision.
- **Timing.** Timeout rates per block, and whether 12 seconds is right.
- **Comprehension failures.** Blocks where responses look random suggest the wording is confusing.
- **Classical item-total correlations** on a provisional basis, treating the forced-choice data crudely just to spot dead items.

Cut the worst 15–20% of statements here. It's much cheaper than discovering they're bad at N=400.

### Stage 3 — Initial TIRT calibration (N ≈ 300)

The real thing. Using `thurstonianIRT`:

```r
library(thurstonianIRT)

# Reshape triplet responses into pairwise comparisons
tirt_data <- make_TIRT_data(
  data          = responses_wide,
  blocks        = block_definitions,   # item, block, trait, keying
  direction     = "larger",
  format        = "triplets",
  family        = "bernoulli"
)

fit <- fit_TIRT_lavaan(tirt_data)      # or fit_TIRT_stan() for full Bayesian

summary(fit)
theta <- predict(fit)                  # person trait estimates with SEs
```

**Estimation back-end choice:**
- `lavaan` — fast, good for iterating during development
- `Mplus` — the reference implementation from the original literature, if you have access
- `Stan` — full Bayesian, gives proper posterior uncertainty on person estimates, slow but the most defensible for final results

Use lavaan while developing, Stan for the published calibration.

**What to check:**

| Check | Threshold | If it fails |
|---|---|---|
| Model convergence | Must converge cleanly | Usually insufficient N or a degenerate block design |
| Loadings | Meaningful magnitude, correct sign | Statement is mis-assigned to a dimension, or keying is wrong |
| Marginal reliability | ≥ .70 per trait | Add blocks for that trait, or drop the trait |
| Fit indices | CFI ≥ .90, RMSEA ≤ .08 | Consider whether the four-dimension structure holds in this sample |
| Person SE distribution | Reasonable and not bimodal | Bimodality suggests the instrument works for some people and not others — investigate by channel |

### Stage 4 — Recalibration and linking (N growing)

Once you're past initial calibration, freeze an **anchor set** — roughly 60% of blocks that never change. Any new or revised blocks are seeded alongside and calibrated on their own accumulating data, linked to the existing scale through the anchors.

This gives you a versioning story that survives contact with reality:

```
v1.0  blocks 1-24   [anchor: 1-14]   calibrated N=312
v1.1  blocks 1-24   [anchor: 1-14]   blocks 19,22 revised, recalibrated N=487
v1.2  blocks 1-28   [anchor: 1-14]   4 new blocks seeded, scored from N=650
```

Record which version each participant saw. This is why the item bank lives in git.

---

## Sample size, honestly

There is no clean published threshold for TIRT with your specific design. What's known:

- Forced-choice IRT needs **more** data than equivalent single-stimulus models — you're estimating more parameters from less direct information
- Requirements scale with the number of traits and blocks
- Simulation studies broadly point to several hundred minimum

**Do this rather than guessing:** run a simulation study matched to your exact design before collecting anything. Generate synthetic responses from known parameters, fit the model, check parameter recovery at N = 150, 250, 350, 500. That tells you your actual requirement instead of borrowing someone else's.

```r
sim <- sim_TIRT_data(
  npersons = 300,
  ntraits  = 4,
  nblocks_per_trait = 6,
  gamma    = 0,
  lambda   = runif(24, 0.65, 0.95),
  psi      = runif(24, 0.20, 0.40)
)
```

Run each N ten times, look at the spread of recovered parameters against the true values. This is a couple of days of work and it turns your sample target from a guess into a justified number. It's also a strong methods section.

---

## Deriving behavioural insight from response patterns

The second half of your question — what can you legitimately say about a person from *how* they answered, not just *what* they answered.

### What's defensible

**Response consistency.** Present matched blocks where the underlying trade-off is identical but the surface wording differs. Inconsistency across matched pairs is measurable and meaningful, and it's much harder to fake than any single response because the participant doesn't know which blocks are paired.

**Revision behaviour.** How often someone changed their answer before confirming. Plausibly related to deliberation, decisiveness, or uncertainty. Nobody reports this and it costs you nothing to capture.

**Timeout pattern.** Which blocks a person times out on — are they consistently slower on blocks involving a particular dimension? That's a real pattern worth investigating.

**Latency profile after covariate control.** Only after controlling reading speed, device, and trait extremity. Weak, but not nothing.

**Extremity of trait estimates.** Someone whose four dimension estimates are all near the mean is different from someone with a sharply differentiated profile — regardless of direction. Profile differentiation is an under-studied variable.

### What isn't defensible

**Inferring anything not measured.** You cannot infer leadership potential, integrity, cultural fit, or emotional intelligence from four dimensions of forced-choice data. The temptation to add interpretive layers is strong and should be resisted — every added inference is an unvalidated claim.

**Reading meaning into single items.** No individual response tells you anything. Statistical properties emerge across blocks; a single choice is noise.

**Post-hoc profile narratives.** Generating a story that fits the pattern is exactly how astrology works. If the narrative isn't derivable from parameters you estimated, don't write it.

**Clustering into types.** You can always run a cluster analysis and always get clusters. It doesn't mean the clusters exist in the population — continuous distributions produce apparent clusters routinely. If you do explore this, use methods that test whether a categorical solution actually fits better than a continuous one, and expect the answer to be no.

### The genuinely novel angle

Your most original contribution isn't a new trait model — the trait space is thoroughly mapped and you won't improve on it with four dimensions and 400 people.

It's the **process data**: consistency, revision, latency, timeout patterns under time pressure. Very few instruments capture this, almost none publish it, and you're building the timing infrastructure anyway. A paper on what response-process data adds beyond trait scores is more distinctive than another personality inventory, and it's the natural intersection of your engineering and psychometric interests.

---

## Build order

1. Simulation study to set the real N target *(do this before collecting anything)*
2. Desirability rating study
3. Pilot, cut bad statements
4. Freeze anchor set, tag item bank v1.0
5. Collect to N target
6. TIRT calibration, full diagnostics
7. Publish parameters alongside the instrument
8. Recalibrate as N grows, maintaining anchor linkage

Step 1 is the one people skip. It's also the cheapest and it determines whether steps 5–6 succeed.

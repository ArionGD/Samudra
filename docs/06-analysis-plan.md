# Analysis Plan (Pre-Registration Draft)

**Status:** Draft v0.1
**Intent:** to be finalised and time-stamped on OSF *before* main data collection begins.

---

## Why pre-register

Two reasons, one principled and one practical.

The principled one: with this many measures, conditions, and channels, the number of possible analyses is large enough that something will reach significance by chance. Specifying in advance is the only defence.

The practical one: a pre-registered study with null results is publishable and credible. An unregistered study with positive results, in a field with a replication problem, is neither.

Register on OSF. It's free, it takes an afternoon, and it converts "I found this" into "I predicted this."

---

## Hypotheses

### H1 — Forced-choice reduces distortion

Score inflation under instructed-faking will be **smaller** for the M1 forced-choice format than published benchmarks for single-stimulus Likert instruments.

- Test: compare condition C (fake) against condition A (honest) on M1 trait estimates, Cohen's *d* per dimension.
- Benchmark: published applicant-vs-incumbent effects of roughly *d* ≈ .45 on conscientiousness-type traits; instructed-faking effects on Likert instruments are considerably larger.
- Prediction: observed *d* for CON and STR under faking will be **below 0.45**.
- Caveat to state openly: this is a comparison against literature benchmarks, not against a Likert instrument administered in the same sample. It is weaker evidence than a within-sample format comparison. If resources allow, administering a short Likert marker set alongside would materially strengthen the design — consider it seriously.

### H2 — Time pressure reduces distortion

Among faking-instructed participants, those in the **timed** condition will show **less** score inflation than those in the untimed condition.

- Test: condition C (fake-timed) versus condition D (fake-untimed), on trait estimates.
- This is the **novel contribution**. Existing evidence on time pressure and faking is mixed and thin.
- **A null result here is a genuine finding and should be reported as such.** Write the discussion section for a null in advance, so you are not tempted to reframe if it happens.

### H3 — Latency carries distortion information

Response latency will differ between honest and faking conditions, **after** controlling for reading speed, device type, and trait extremity.

- Test: mixed-effects model, latency as outcome, condition as fixed effect, participant and item as random effects, with the covariates above.
- **Direction is not predicted.** The literature suggests responses congruent with a faking schema may be *faster* while incongruent ones are *slower* — so a simple main effect may not appear. Test the interaction with response-schema congruence.
- Treat this as exploratory-confirmatory hybrid and label it honestly.

### H4 — Intended factor structure replicates

The four M1 dimensions will emerge with acceptable fit in an Indian sample.

- Thresholds: CFI ≥ .90, RMSEA ≤ .08, SRMR ≤ .08.
- Failure to replicate is itself interesting — it would suggest structures derived on Western samples don't transfer, which is a finding worth reporting.

### H5 — Convergent and discriminant validity

M1 dimensions will correlate meaningfully with matched external markers and less with unmatched ones.

- Requires administering a short established marker set (e.g. a brief Big Five inventory) to a subsample.
- Targets: convergent *r* ≥ .50 for matched constructs; discriminant correlations meaningfully lower.
- **This subsample is essential.** Without external markers you have no evidence your dimensions measure what you claim. Budget for it.

### H6 — Measurement invariance across channels

M1 measurement properties will hold across recruitment channels.

- Test: configural → metric → scalar invariance.
- Realistically underpowered for the NGO channel. If N is insufficient, report descriptive comparisons and say plainly that invariance could not be tested rather than running an underpowered model.

---

## Analysis sequence

**Stage 0 — Data cleaning (blind to condition)**

Apply pre-specified exclusions before any hypothesis test, without looking at outcome variables:

- Attention check failures: exclude if **both** checks failed in a module
- Latency floor: exclude individual responses under 300ms on reading-required items
- Straight-lining: exclude a module if response variance is zero across all blocks
- Timeout rate: exclude a module if more than 40% of items timed out
- Focus-lost: exclude individual responses where the tab was backgrounded
- Duplicates: retain first complete session only, unless the retest interval was met

Report N excluded at each step. Sensitivity analysis with and without exclusions.

**Stage 1 — Descriptives** — demographics by channel, completion rates, dropout points, timing distributions.

**Stage 2 — Item analysis** — desirability spread verification (did blocks stay matched in practice?), block-level response distributions, item information.

**Stage 3 — TIRT calibration** — `thurstonianIRT` package. Report model fit, marginal reliability per dimension, and item parameters. Retain the full parameter table for reproducibility.

**Stage 4 — Confirmatory tests** — H1 through H6, in order, with pre-specified tests.

**Stage 5 — Exploratory** — clearly labelled as such, in a separate section. Anything not listed above is exploratory. This is a real section with real value; the sin is not exploring, it is presenting exploration as confirmation.

---

## Statistical specification

| Element | Choice |
|---|---|
| Alpha | .05 |
| Multiple comparisons | Holm-Bonferroni within hypothesis families |
| Effect sizes | Reported with 95% CIs for everything |
| Missing data | Full information maximum likelihood; do not impute latency |
| Software | R (`thurstonianIRT`, `lavaan`, `lme4`), Python for cleaning and semantic scoring |
| Reproducibility | All analysis code in the repository; `renv` for R dependencies |

**Power:** with 100 per condition cell, detecting *d* = 0.40 at 80% power is achievable. Smaller true effects will not be reliably detected — state this as a limitation rather than discovering it afterwards.

---

## Module-specific analyses

**M2 — Divergent thinking.** Fluency, flexibility, originality. Correlate frequency-based and semantic-distance originality scores; report their agreement. Control for typing speed throughout — a timed generation task partly measures typing.

**M3 — Critical reasoning.** Total score and by item family. Use as a validity anchor: check whether M1 dimensions relate sensibly to reasoning performance. **Also run subgroup difference analysis by education band** — not to publish claims about groups, but because knowing the adverse-impact profile is a precondition for ever using this responsibly.

**M4 — SJT.** Score against SME key. Report inter-rater agreement among SMEs — if experts don't agree on the key, the scores mean little. Analyse student and professional samples separately given the workplace-experience gap.

**M5 — Ethical judgement.** Orientation scores plus the consistency index across matched scenario pairs. **Report only orientation and consistency, never moral quality.** No analysis should imply any group reasons better than another.

---

## What I will not do

Stating these in advance is part of the point:

- Drop conditions or channels that produce inconvenient results
- Add covariates after seeing their effect on significance
- Convert a failed confirmatory test into an exploratory success
- Report only the modules that worked
- Interpret an underpowered invariance model as evidence of invariance
- Claim validity for hiring use — no criterion data exists in this design
- Publish individual-level data without separate open-data consent

---

## Deliverables

1. **Technical report** — full methods, results including nulls, limitations
2. **Preprint** — PsyArXiv
3. **Open dataset** — consented subset only, with data dictionary
4. **Analysis code** — public repository, reproducible from raw extract
5. **Item bank** — published openly, which precludes commercial use but is the right call for a research instrument
6. **NGO report** — plain-language findings relevant to their population, as promised

---

## Honest limitations to state in any write-up

Write these into the paper from the first draft:

- Convenience sample; not representative of any defined population
- Instructed faking is not applicant faking — it establishes capacity, not behaviour
- No criterion data; no evidence of job-performance prediction
- Latency confounds only partially controlled
- Assisted-administration data not comparable on timing measures
- Single language for most of the sample; cross-linguistic equivalence untested
- Solo researcher; no independent verification of coding decisions
- Ethics oversight arrangement (state exactly what it was)

A paper that names its own limitations clearly is far more credible than one that waits for a reviewer to find them.

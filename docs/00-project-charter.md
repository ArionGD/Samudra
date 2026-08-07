# Project Charter — Multi-Module Faking-Resistant Assessment Battery

**Status:** Draft v0.1
**Owner:** Chandan
**Last updated:** August 2026

---

## 1. What this is

An open, web-hosted assessment battery consisting of several short, independently-deployable modules measuring constructs relevant to leadership and work performance. Participants take modules voluntarily and consent to their anonymised data being used for psychometric research.

The dual purpose matters and should stay explicit:

- **Research purpose:** build and validate instruments that resist response distortion better than existing adjective-checklist tools.
- **Portfolio purpose:** produce a defensible, publicly documented body of work demonstrating psychometric, engineering, and research-design capability.

These two purposes mostly align. Where they conflict — e.g. shipping fast versus calibrating properly — the research purpose wins, because a fast-shipped instrument with no validity evidence is worthless for both.

## 2. What this is not

Stating this clearly protects you legally and reputationally:

- **Not a hiring tool.** Not until criterion validation and adverse-impact analysis are complete. Do not let anyone use scores for selection decisions during the research phase. Put this in the terms of use.
- **Not a clinical instrument.** It does not diagnose anything. No mental-health constructs, no anxiety/depression scales, no personality-disorder content.
- **Not a certified IQ test.** The critical-thinking module measures reasoning quality, not general intelligence, and should never be labelled or reported as an IQ score.

## 3. Core research question

> Does a time-pressured, multidimensional forced-choice battery with mixed item formats produce trait and ability estimates that are (a) psychometrically sound and (b) less susceptible to deliberate response distortion than conventional single-stimulus Likert instruments — in an Indian, non-Western sample?

Sub-questions worth answering along the way:

1. **RQ1 (Fakability).** How much do scores shift under instructed-faking conditions, relative to published Likert benchmarks?
2. **RQ2 (Structure).** Do the intended factors emerge in an Indian sample, or does the structure differ from Western norming data?
3. **RQ3 (Latency).** Does response latency add incremental information about distortion, after controlling for reading speed, device, and trait extremity?
4. **RQ4 (Time pressure).** Does a speeded administration condition reduce distortion relative to an untimed condition on the same items?

RQ4 is the most publishable and most original. It is also the cheapest to run — it needs one instrument and two conditions, not two instruments.

## 4. The five modules

| # | Module | Construct | Primary format | Est. duration |
|---|--------|-----------|----------------|---------------|
| M1 | Rapid Trait | Work-relevant dispositions (conscientiousness, stress tolerance, agreeableness, dominance) | Multidimensional forced-choice, timed blocks | 8–10 min |
| M2 | Divergent Thinking | Creative fluency, flexibility, originality | Open-response generation (Alternate Uses style) | 6 min |
| M3 | Critical Reasoning | Argument evaluation, bias resistance, base-rate use | Multiple choice, timed | 10–12 min |
| M4 | Judgement | Practical and interpersonal judgement | Situational Judgement Test, knowledge-keyed | 10 min |
| M5 | Ethical Judgement | Moral reasoning consistency | Scenario-based, forced-choice trade-offs | 8 min |

**Design principle:** each module stands alone. A participant can complete M2 in six minutes without committing to the whole battery. This is central to the recruitment strategy — completion rates collapse past roughly 15 minutes for unpaid online participation, and a modular design lets you accumulate a large N on individual modules even if few people finish everything.

**Sequencing rule:** never present all five in one session by default. Offer a randomised subset of two, with an optional "continue" prompt. This also gives you counterbalancing for free.

## 5. Deliberate scope exclusions

Cut these, and be firm about it:

- **No facial or video analysis.** Regulatory risk is severe and the validity evidence is poor. HireVue removed its facial-analysis component in 2021 under criticism; do not walk into a problem a well-resourced vendor retreated from.
- **No demographic inference.** Do not attempt to infer caste, religion, or socioeconomic status from any input.
- **No stress induction via deception or failure feedback.** Time pressure and cognitive load only. This keeps the project in minimal-risk territory and dramatically simplifies ethics review.
- **No dark-triad or counterproductive-behaviour scales in v1.** They attract scrutiny, produce results that feel accusatory to participants, and complicate your consent story. Add later if at all.
- **No free-text about the participant's own workplace or colleagues.** Creates third-party data problems under DPDP.

## 6. Success criteria

The project succeeds if, within twelve months:

- **N ≥ 400** on at least one module, with clean data and documented consent.
- **Factor structure** for M1 replicates the intended dimensions with acceptable fit (CFI ≥ .90, RMSEA ≤ .08 as working thresholds).
- **Marginal reliability ≥ .70** for each M1 trait scale.
- **RQ4 answered** with a properly powered honest-versus-faking comparison.
- **One public artefact** — a preprint, a technical report, or a well-documented open dataset.

Note that "instrument is validated for hiring use" is deliberately *not* a success criterion. That requires criterion data linking scores to job performance, which you almost certainly cannot obtain at this stage. Do not overclaim it.

## 7. Honest risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Sample is unrepresentative (young, urban, educated, English-literate) | **Very high** | Medium | Treat as a known limitation; report demographics fully; do not generalise beyond the sample; consider Hindi translation to broaden reach |
| Low completion rates | High | Medium | Short modules; immediate feedback as an incentive; no mandatory registration |
| Insufficient N for IRT calibration | Medium | High | Prioritise one module to full calibration rather than five to half-calibration |
| Consent quality challenged, especially NGO channel | Medium | **High** | See `02-ethics-and-consent.md` — non-negotiable safeguards |
| No institutional ethics oversight | High | Medium | Seek college IRB affiliation; failing that, constitute an independent review panel |
| Data breach | Low | **High** | Minimise collection; no direct identifiers in the response store; encrypt at rest |
| Someone uses the tool for real hiring decisions | Medium | High | Explicit terms-of-use prohibition; no employer-facing reporting features in v1 |

## 8. What makes this genuinely novel

Be clear-eyed about the contribution, because "another personality test" is not one.

1. **Indian sample.** Almost all forced-choice and faking research is conducted on Western samples. Structure replication in an Indian population is a real, publishable gap.
2. **Time pressure as a distortion countermeasure.** The evidence base here is thin and mixed. A clean experiment is a genuine contribution, and negative results are still publishable.
3. **Fully open methodology.** Published items, published scoring code, published data. Commercial vendors do not do this. It is your strongest differentiator and costs you nothing you were going to monetise anyway.

## 9. Related documents

- `01-instrument-design.md` — module-by-module item design
- `02-ethics-and-consent.md` — consent, vulnerable populations, DPDP compliance
- `03-platform-architecture.md` — technical build
- `04-data-schema.md` — storage model
- `05-recruitment-plan.md` — sampling strategy per channel
- `06-analysis-plan.md` — pre-registered analytic approach
- `07-roadmap.md` — phased execution plan

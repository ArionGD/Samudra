# Participant Feedback and Report Design

**Status:** Draft v0.1
**Companion to:** `02-ethics-and-consent.md`, `06-analysis-plan.md`

---

## Why this document exists

Feedback is the primary non-monetary incentive in this project. It is also the participant-facing artefact — the thing people screenshot, share, and judge the work by. It is therefore both the main driver of recruitment and the main reputational risk.

Two hard constraints shape every decision below.

**Constraint 1 — norms don't exist yet.** A trait score means nothing without a reference distribution. Until TIRT calibration completes on 300+ participants, there is no defensible way to tell someone their standing on a dimension. Any number shown before that point is invented.

**Constraint 2 — the Barnum effect.** People rate vague, positive, generally-applicable personality descriptions as highly accurate about themselves. Forer demonstrated this in 1948 with a description assembled from a newsstand astrology column; participants rated it 4.26/5 for accuracy.

The second constraint is the more dangerous one, because it produces *false positive feedback about your own work*. If you write a warm, plausible report, participants will tell you it's uncannily accurate — and that reaction will be entirely independent of whether your instrument measures anything. You would get the same reaction from randomised output.

**Design rule that follows:** never treat participant satisfaction with the report as evidence the instrument works. Those are separate questions, and only the psychometrics answer the second one.

---

## Staged feedback model

Different participants get different reports depending on what actually exists at the time they participate.

### Stage A — Pilot and early collection (N < 300, no norms)

**What you can honestly show:**

- **Completion summary.** Modules done, time taken, items answered.
- **Response style, descriptively.** "You changed your answer on 8 of 24 blocks" — factual, interesting, requires no norms.
- **Speed profile.** Median response time, described plainly, without evaluation.
- **M2 output returned to them.** Their own divergent-thinking responses listed back. People genuinely enjoy seeing what they produced under time pressure.
- **What their data contributes.** Which research question their session feeds, and when results will be available.
- **An honest placeholder.** "Your trait profile isn't available yet. Scores require a reference sample of about 300 people, and we're at 142. We'll email your profile when calibration is complete if you've opted in."

**What you must not show:** any trait score, any dimension label applied to them, any narrative description of their personality.

That placeholder is doing real work. It converts an absence into a reason to care about the project's progress, and it's a demonstration of research integrity that the developer channel in particular will respect.

### Stage B — Post-calibration (N ≥ 300, TIRT model fitted)

Now trait estimates exist and can be shown with their uncertainty.

**Show:**
- Four M1 dimension estimates, as percentile bands against the research sample
- **Confidence intervals, visibly** — not point estimates
- Descriptive text per dimension, written to be genuinely informative rather than flattering
- Explicit statement of what the reference sample is

**Still don't show:** M3 reasoning scores, M5 moral evaluation. Reasons below.

### Stage C — Post-validation (if it ever happens)

Only after criterion validation would occupational interpretation be defensible. Realistically this project does not reach Stage C. Don't design for it.

---

## Writing rules for the report text

These rules exist specifically to defeat the Barnum effect. A report that follows them will feel *less* accurate to participants than a vague one. That is the intended outcome.

**Be specific enough to be wrong.**
- ❌ "You have a good balance of independence and cooperation." — true of everyone
- ✅ "You consistently chose planning-oriented statements over spontaneity, in 9 of 11 blocks where they were paired."

**Describe behaviour, not essence.**
- ❌ "You are a natural leader."
- ✅ "In this assessment, you selected assertive options more often than the comparison sample."

**Show uncertainty rather than hiding it.**
- ❌ "Conscientious Reliability: 78th percentile"
- ✅ "Conscientious Reliability: around the 78th percentile, with a range of roughly 65–88. Short assessments produce wide ranges."

**Avoid unearned positivity.** Every dimension needs a genuine trade-off statement. If high scores on all four sound good, you've written a horoscope. High Assertive Drive has costs. High Cooperative Orientation has costs. Say so.

**No archetypes, no labels, no types.** This is the specific failure mode of PI, MBTI, and every four-letter or animal-name system. Types are memorable, shareable, and epistemically worthless — they discretise continuous variables and invite people to treat a probability distribution as an identity. Resisting the temptation costs you virality and buys you credibility. Take the trade.

**Symmetry test:** would this sentence read as insulting if the score were reversed? If yes, rewrite both directions to be neutral.

---

## What is never reported to participants

| Module | Withheld | Why |
|---|---|---|
| M3 | Any reasoning/accuracy score | Telling someone they reasoned poorly is unkind, serves no research purpose, and risks being read as an intelligence verdict |
| M5 | Any moral quality evaluation | Indefensible. You'd be imposing one ethical framework and scoring people against it |
| M5 | Consistency index, individually | Telling someone their moral reasoning is inconsistent is a criticism dressed as data |
| All | Comparison to named groups | "You scored higher than most engineers" invites stereotype confirmation |
| All | Any occupational recommendation | No criterion data exists. This would be fabrication |

For M3 and M5, show engagement rather than performance: "You completed all 24 reasoning items" and "Your responses across the ethical scenarios have been recorded." Explain in the report why performance isn't shown — participants respect the reasoning when it's stated.

---

## Mandatory disclaimer

Present prominently, not in a footer:

> **This is a research instrument under development.**
>
> These results come from a short assessment that has not been validated against real-world outcomes. They do not predict job performance, academic success, or anything else.
>
> They should not be used by you or anyone else to make decisions about employment, education, or opportunities.
>
> Percentiles compare you to others who have taken this research assessment — a self-selected group, not the general population.

The last line matters more than it looks. Your reference sample is developers, students, NGO participants, and professionals in unequal proportions. A percentile against that mixture is not a percentile against any meaningful population, and saying so plainly is the difference between a research report and a consumer personality quiz.

---

## Screenshot risk

People will share these. Design for that.

- Put the "research instrument, not validated" line **inside** the visual, not adjacent to it — a screenshot must carry its own caveat
- No employer-shareable or CV-ready formatting. Don't build the export button
- No score that reads as a grade or overall rating
- Consider whether the shareable image should show trade-offs rather than strengths, specifically so it isn't useful as self-promotion

---

## Using the report as a research instrument

Since you're building it anyway, get data from it. Add two optional questions after the report:

1. *"How accurately does this describe you?"* (1–7)
2. *"Which single statement felt most accurate?"*

Then — and this is the interesting part — **randomly assign a subset of participants to receive a generic report** (identical structure, content not derived from their responses). Compare accuracy ratings.

If genuine and generic reports are rated equally accurate, you have measured the Barnum effect in your own instrument, in your own sample. That's a real, publishable finding, and it's a much better use of the report than treating positive reactions as validation.

**Ethics note:** this involves temporary deception, so it needs explicit ethics approval and a debrief. Tell participants afterwards, show them their real report, and explain why the comparison was necessary. Most people find this genuinely interesting rather than objectionable — but it must go through review, and it must not be the *only* report anyone receives.

---

## Portfolio value

A report screen that shows confidence intervals, refuses to assign a type, states its own limitations, and withholds scores it can't justify is a stronger demonstration of judgement than a polished profile with an archetype name.

Anyone evaluating you technically will notice the restraint. Anyone who wouldn't notice isn't the audience worth optimising for.

---

## Build order

1. Stage A report — needed from the first pilot participant
2. Optional accuracy-rating questions
3. Stage B report — only after calibration
4. Barnum comparison condition — only with ethics approval

Do not build Stage B early "so it's ready." Having a scoring screen that works but has no valid norms behind it is exactly the situation where it gets used prematurely.

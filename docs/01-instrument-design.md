# Instrument Design — Module Specifications

**Status:** Draft v0.1

---

## Design philosophy

Three commitments drive every decision below.

**Format diversity beats format purity.** Different constructs need different measurement approaches. Forcing everything into one format (PI's mistake — everything is an adjective checklist) means most constructs are measured badly.

**Fake-resistance comes from removing the obvious answer, not from catching liars.** Detection indices don't improve validity when used to correct scores. Design the item so that distortion has nowhere to go instead.

**Time pressure is a deterrent, not a measurement.** Speeded administration plausibly makes deliberate distortion harder. It does not follow that response time is a valid distortion signal. Keep those two claims separate.

---

## M1 — Rapid Trait (Multidimensional Forced-Choice)

### Constructs

Four work-relevant dimensions, deliberately narrow rather than full Big Five:

| Code | Dimension | Working definition |
|------|-----------|--------------------|
| CON | Conscientious Reliability | Follow-through, planning, rule adherence |
| STR | Stress Tolerance | Composure and functioning under load and ambiguity |
| COO | Cooperative Orientation | Collaboration, deference to group, conflict avoidance |
| DRV | Assertive Drive | Initiative, dominance, comfort directing others |

Four dimensions is the minimum for a meaningful forced-choice design and keeps calibration sample requirements manageable. Adding a fifth roughly increases the required N.

### Item format

Blocks of **three statements** (triplets), each statement drawn from a *different* dimension. Participant selects **most like me** and **least like me**.

Triplets beat pairs: they yield more information per block and give better Thurstonian IRT recovery. Blocks of four increase cognitive load past what a speeded format tolerates.

```
Which is MOST like you, and which is LEAST like you?

  ( ) I keep a written plan for the week ahead.          [CON]
  ( ) I stay level-headed when deadlines compress.       [STR]
  ( ) I let others take the lead in group decisions.     [COO]
```

### The critical design constraint — desirability matching

**This is the single thing that determines whether the module works.** If one statement in a block is obviously more socially desirable than the others, the block collapses back into a fakable single-stimulus item.

Procedure:

1. Write an item pool of roughly 120 statements, 30 per dimension.
2. Have a separate rating sample (n ≈ 40, can be small and informal) rate each statement on social desirability: *"How favourably would an employer view someone who agreed with this?"* on a 1–7 scale.
3. Compute mean desirability per statement.
4. Assemble triplets where the three statements fall within **±0.5 scale points** of each other on mean desirability.
5. Balance keying: roughly a third of blocks should mix high-desirability statements, a third mid, a third low. All-high blocks are frustrating; all-low blocks feel insulting.

Statements that cannot be desirability-matched get discarded. Expect to lose 30–40% of your initial pool. Write more items than you think you need.

### Speeded administration

- **12 seconds per block**, with a visible but non-alarming countdown.
- Timeout records a missing response and advances. Do not force a choice; forced responses under timeout are noise.
- Target **20–24 blocks**, giving roughly 5 blocks per dimension pair.
- Practice blocks: 2, untimed, not scored.

The 12-second figure is a starting estimate for triplets of short statements. **Pilot it.** If timeout rates exceed 10%, lengthen. If mean response time is under 5 seconds, you can shorten and the pressure manipulation gets stronger.

### Scoring

Thurstonian IRT via the `thurstonianIRT` R package. Each triplet decomposes into pairwise comparisons; the model recovers normative latent trait estimates, defeating the ipsativity problem that makes classical forced-choice scores non-comparable across people.

Report **marginal reliability** per dimension, not Cronbach's alpha — alpha is not interpretable for forced-choice data.

### Experimental conditions for RQ4

Same items, three between-subjects conditions:

- **A — Honest, untimed.** Baseline.
- **B — Honest, timed.** Isolates the effect of time pressure alone on scores.
- **C — Instructed-fake, timed.** *"Answer as if applying for a job you badly want."*

A fourth condition (instructed-fake, untimed) completes the 2×2 and is worth including if N allows. The full factorial is what makes this a real experiment rather than a comparison of convenience.

---

## M2 — Divergent Thinking

### Construct

Creative ideation, scored on three classical dimensions: **fluency** (number of responses), **flexibility** (number of distinct categories), **originality** (statistical or semantic rarity).

### Format

Alternate Uses style. Two prompts, three minutes each.

```
Name as many different uses as you can for a BRICK.
Unusual answers are welcome. Type one per line.
[03:00]
```

Prompt selection matters. Use concrete, culturally neutral objects available to everyone in your sample — brick, newspaper, plastic bottle, rope. Avoid objects with class-linked familiarity.

### Scoring approach

- **Fluency:** count of non-duplicate responses. Trivial to automate.
- **Flexibility:** count of distinct semantic categories. Requires either a coding scheme or embedding-based clustering.
- **Originality:** the interesting problem. Two options:
  - *Frequency-based:* a response is original if fewer than 5% of the sample gave it. Simple, defensible, but requires the full sample before any individual can be scored.
  - *Semantic distance:* embed each response and the prompt, compute cosine distance. Scoreable immediately, correlates reasonably with human originality ratings in published work, and is a genuinely interesting engineering component for your portfolio.

Run both and report their correlation. That comparison is itself a small publishable result.

### Cautions

- Divergent-thinking tasks have **weak-to-moderate** relationships with real-world creative achievement. Do not overclaim. Frame it as ideational fluency, not "creativity."
- Typing speed is a serious confound in a timed generation task. Capture keystroke timing or include a brief typing-speed baseline, and covary it. Without this, you are partly measuring how fast people type.
- Language: responses in Hindi or mixed script will appear. Decide in advance whether to accept, and how to score them.

---

## M3 — Critical Reasoning

### Construct

Reasoning quality under conditions where intuition misleads. Not general intelligence.

### Item types

Four families, roughly six items each:

**(a) Belief-bias syllogisms.** Logically valid conclusions that are implausible, and invalid conclusions that are believable. Measures whether the person evaluates structure or content.

**(b) Base-rate problems.** Classic Kahneman-Tversky style. Does the person use prior probability or ignore it for representativeness?

**(c) Argument evaluation.** Present a short argument; ask which single fact would most weaken it. Standard critical-reasoning format, and the closest to workplace relevance.

**(d) Evidence sufficiency.** Given a claim and three pieces of evidence, identify which actually supports it versus which merely correlates.

### Faking resistance

This module is **inherently fake-resistant** — there is a correct answer, and you either know it or you don't. Faking upward is impossible; only faking downward is available, and nobody does that in a voluntary research context.

This makes M3 valuable as a **validity anchor**: if M1 scores correlate sensibly with M3 performance, that supports the whole battery's construct validity.

### Timing

Timed, but generously — 45 seconds per item. Reasoning items under severe time pressure become measures of speed rather than reasoning, which is a different construct.

### Serious caution

Cognitive-ability-type measures show the largest subgroup differences of any selection method, and are the primary source of adverse impact in hiring. In a research context this is fine. **If this module ever moves toward operational use, adverse-impact analysis is mandatory and non-optional.** Flag this in every document that touches M3.

---

## M4 — Judgement (SJT)

### Construct

Practical and interpersonal judgement in work situations.

### Format — the critical instruction choice

Use **knowledge instructions**, not behavioural-tendency instructions.

- ✅ *"Which response is the MOST effective?"* — loads on judgement, harder to fake
- ❌ *"Which would you MOST likely do?"* — loads on personality, easily faked

This distinction is well established in the SJT literature and is the single highest-leverage design decision in this module.

### Item structure

Short scenario (40–60 words), four response options, participant ranks best and worst.

```
A team member has missed two deadlines. They have told you privately
that they are dealing with a family situation. The project timeline
has no slack remaining.

Which response is MOST effective? Which is LEAST effective?

  ( ) Reassign their tasks immediately without discussion
  ( ) Ask what support would let them meet the next deadline
  ( ) Escalate to their manager for a formal record
  ( ) Extend the deadline and absorb the schedule impact
```

### Development requirement

SJT items **cannot** be written from armchair reasoning. They require critical-incident collection: interview people who do the job, ask for specific situations where judgement mattered, and derive scenarios from real incidents.

Keying options:
- **SME consensus** — a panel of experienced practitioners rates option effectiveness. Practical and defensible.
- **Empirical keying** — key against a criterion. Better, but you need criterion data you probably don't have.

Start with SME keying. Be transparent that it is expert-consensus, not empirically validated.

### Domain framing

Given your background, an infrastructure/project-execution framing is a genuine advantage — you have access to SMEs who can generate real incidents. But note that this narrows generalisability, and a college-student sample will find site-specific scenarios alien. Consider two variants: a generic workplace version for the broad sample, and a domain version for practitioner samples.

---

## M5 — Ethical Judgement

### Construct

**Consistency and structure of moral reasoning** — explicitly *not* moral correctness.

This framing is essential. An instrument that scores people as more or less moral is indefensible, invites the accusation that you are imposing one moral framework, and will not survive scrutiny. Score the *coherence* of a person's reasoning across scenarios, not whether they reached the answer you prefer.

### Format

Forced-choice trade-offs between competing goods. Both options must be defensible.

```
A supplier has consistently delivered quality work for three years.
A new vendor offers the same specification at 15% lower cost.

  ( ) Award to the new vendor; cost savings serve the organisation
  ( ) Retain the existing supplier; relationship reliability has value
```

### Scoring

Derive **orientation scores** on dimensions such as:

- Rules-based versus outcome-based reasoning
- In-group loyalty versus impartial treatment
- Short-term versus long-term weighting

Plus a **consistency index**: does the person apply the same principle when the surface details change? Present matched scenario pairs where the underlying trade-off is identical but the framing differs. Inconsistency here is the actual signal, and it is much harder to fake than a stated preference.

### Hard constraints

- No scenarios involving religion, caste, politics, or communal identity. Non-negotiable in an Indian sample.
- No content that could distress — no violence, no life-and-death medical triage, no abuse scenarios.
- Never report an individual's score as a moral evaluation. Feedback should describe *style*, not *quality*.

---

## Cross-cutting: what gets captured

For every module, log:

- Item-level responses with timestamps
- Response latency per item (research variable only — see charter)
- Device type and viewport width (latency confound)
- A brief reading-speed baseline task (latency confound)
- Condition assignment
- Module order and position

**Do not** log free-text about identifiable third parties, IP addresses beyond what's needed for abuse prevention, or anything that could re-identify a participant.

---

## Development order

Build M1 first and completely. It carries the core research question, needs the most calibration data, and has the highest engineering complexity. A fully validated M1 is worth more than five half-built modules.

Then M3 (cheap to build, serves as validity anchor), then M2 (interesting scoring problem), then M4 and M5 (expensive item development, highest ethics sensitivity).

# Recruitment and Sampling Plan

**Status:** Draft v0.1

---

## The honest starting position

You have access to a **convenience sample**, and no amount of design will make it representative. Developers, college students, and NGO participants are three non-random, non-overlapping populations, none of which resembles the general population or the working population.

This is not disqualifying. Most published psychometric research runs on convenience samples — undergraduate psychology students, largely. What separates defensible work from indefensible work is whether the limitation is **stated, analysed, and respected in the conclusions**.

So: report demographics fully, test whether findings hold across channels, and never write a sentence that generalises beyond what the sample supports.

There is also a real upside here. Your channels are *heterogeneous* in a way that a single-university sample is not. Comparing measurement properties across three quite different subpopulations is a genuine strength — measurement invariance testing across channels is more interesting than another homogeneous student sample.

---

## Target sample sizes

| Purpose | Minimum N | Comfortable N |
|---|---|---|
| Pilot (item statistics, timing calibration) | 40 | 80 |
| Desirability rating sample (separate) | 30 | 50 |
| M1 TIRT calibration | 300 | 500 |
| Fakability experiment (per cell) | 60 | 100 |
| Factor structure (CFA) | 250 | 400 |
| Measurement invariance across channels | 200 per group | 300 per group |

**Prioritisation:** if resources are limited, get M1 to full calibration N before spreading across modules. A well-calibrated single instrument is a real contribution; five under-powered instruments are not.

Note that invariance testing at 200 per group is aspirational. If the NGO channel yields 80, you can still report descriptive comparisons — just don't run an underpowered invariance model and interpret its fit indices as if they were meaningful.

---

## Channel 1 — Developer community

**Reach:** potentially wide. GitHub, dev-focused Discord/Slack communities, r/developersIndia, Hacker News (for the platform, not the study), LinkedIn tech networks.

**Strengths:** high digital literacy, comfortable with novel interfaces, low dropout on timed tasks, likely to give useful bug reports.

**Biases to name explicitly:** young, male-skewed, urban, English-fluent, high formal education, unusually high analytical self-concept. Systematically atypical on exactly the traits M1 and M3 measure.

**Approach that works:** lead with the engineering, not the psychology. A post about *building a millisecond-accurate assessment platform*, with the study as the reason it exists, will outperform a request for research participants by a wide margin. Open-source the platform and the participation follows.

**Approach that fails:** mass-posting a survey link. Reads as spam, gets removed, damages reputation in communities you want to stay in.

**Realistic yield:** 150–400 over several months if the technical framing lands.

---

## Channel 2 — College students

**Reach:** dependent on faculty cooperation. This is the channel most worth investing relationship effort in, because it also solves your ethics-review problem.

**Strengths:** accessible, plentiful, standard research population, faculty contact gives you IRB access and a potential co-author.

**Biases:** narrow age range, no work experience (a real problem for M4 workplace SJT items), education-selected, and — critically — **potential coercion if participation is course-linked**.

**Non-negotiable safeguards:**
- Participation must not affect grades in any way
- If credit is offered, an equivalent non-research alternative must exist
- The instructor should not know who participated
- Recruitment via general announcement, not individual solicitation by someone who grades them

**Approach:** identify one or two faculty members in psychology, management, or HR who would find the research interesting. Offer genuine collaboration — co-authorship, access to the data, a guest session on psychometrics for their students. This is a much better trade than "please let me survey your class."

**Note on M4:** students have no workplace experience. Either use the generic-workplace SJT variant for this channel, or accept that M4 data from students measures something different and analyse separately.

**Realistic yield:** 100–300 per cooperating institution.

---

## Channel 3 — NGO-connected participants

**Read `02-ethics-and-consent.md` before touching this channel.** The safeguards there are mandatory, not advisory.

**Strengths:** genuine demographic diversity that your other two channels entirely lack. This is what makes the sample interesting rather than just another convenience sample of educated urban young people.

**Constraints that are real and must be designed around:**
- Variable literacy and digital literacy
- Language — English-only administration will exclude most of this group
- Device access and data cost
- Power imbalance with the NGO
- Possible presence of minors

**What this requires you to build:**
- **Hindi translation at minimum**, ideally the regional language relevant to the NGO's area. Translation must be done properly — forward translation, back translation, reconciliation — not machine-translated. A badly translated instrument measures translation quality, not the construct.
- **Assisted administration protocol** for low-literacy participants: a trained facilitator who reads items aloud without interpreting or steering
- **Offline-capable** delivery, or provision of data
- Human age verification, not a self-declared checkbox

**The uncomfortable truth about assisted administration:** if a facilitator reads items aloud, your response latency data from that channel is not comparable to self-administered data. You cannot pool it for RQ3 or RQ4. Plan to analyse it separately for structure and descriptive purposes only.

**What you owe this group:** a real answer to "what do they get from this." Options that are genuinely valuable: a report to the NGO on whether standard assessment instruments work for their population, skills sessions, or findings relevant to their programme design. Deliver it, don't just promise it.

**Realistic yield:** 50–150, with substantially higher effort per participant than the other channels.

---

## Channel 4 — Working professionals (your network)

Worth adding, because it is the only channel with actual workplace experience — which M4 and M5 need.

**Reach:** LinkedIn, HR professional groups, industry contacts, EPC-sector colleagues.

**Strengths:** genuine occupational relevance, older age range, real job context for SJT items.

**Biases:** professional/managerial skew, high income, and — if recruited through your own workplace — potential concerns about whether responses could affect their standing.

**Critical constraint:** do **not** recruit your own direct reports or anyone you have authority over. Same power-imbalance problem as the NGO channel, closer to home. If colleagues participate, it must be through a general call with explicit separation from any HR process, and you must not be able to identify individual responses.

**Realistic yield:** 80–200.

---

## Combined realistic projection

| Channel | Conservative | Optimistic |
|---|---|---|
| Developer | 150 | 400 |
| College | 100 | 300 |
| NGO | 50 | 150 |
| Professional | 80 | 200 |
| **Total** | **380** | **1,050** |

The conservative figure clears the M1 calibration threshold. That's the number to plan against.

Expect roughly 40–60% of starters to complete a given module. Recruit for the number who start, not the number you need.

---

## Sampling and assignment

**Condition assignment:** random, server-side, stratified by recruitment channel so that each condition has representation from each channel. Simple randomisation with unequal channel yields produces unbalanced cells.

**Module assignment:** each participant gets a randomised subset of two modules, with an optional continue. Randomise both selection and order — order effects are real and you get the counterbalancing for free.

**Repeat participation:** allow it for test-retest data (valuable, and hard to get otherwise), but flag it clearly. A participant returning after two weeks gives you retest reliability; the same person doing the module twice in one day gives you contaminated data. Enforce a minimum interval.

---

## Recruitment materials — principles

- **Lead with honesty about what it is.** "A research study on how people answer questions under time pressure" is accurate and interesting enough.
- **State the time cost up front**, accurately. Overrunning the stated time is the main driver of dropout and of irritation.
- **Say what participants get**: descriptive feedback, and contribution to open research.
- **Do not overclaim.** No "discover your leadership type," no "find out your true personality." Those claims are false, attract the wrong participants, and undermine the research framing.
- **State clearly that it is not a hiring tool** and results should not be used for any decision.

---

## Timeline

| Phase | Duration | Focus |
|---|---|---|
| Desirability rating study | 2 weeks | 30–50 raters, item pool |
| Pilot | 3 weeks | 40–80 participants, timing calibration, bug-finding |
| Main collection wave 1 | 8 weeks | Developer + college channels |
| Translation and NGO protocol | 4 weeks | Parallel with wave 1 |
| Main collection wave 2 | 8 weeks | NGO + professional channels |
| Retest wave | 2 weeks | Subset invited back |

Roughly six months to a full dataset, assuming the channels cooperate. Build slack into this — faculty approval and translation both routinely take longer than planned.

---

## What to monitor while collecting

Track weekly, and act on it:

- N per channel per condition — catch imbalance early, while you can still fix it by targeted recruitment
- Completion rate by module and by device type
- Dropout point distribution — where exactly people quit tells you what to fix
- Timeout rate per block — if a block times out for 20% of people, its time limit is wrong
- Quality flag rate by channel

Do **not** look at trait score distributions or run any hypothesis test until collection is complete and the pre-registered analysis begins. Peeking at outcomes mid-collection and adjusting is how well-intentioned research becomes unpublishable.

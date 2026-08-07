# Ethics, Consent, and Data Protection

**Status:** Draft v0.1
**This is the document that determines whether the project is defensible.**

---

## Why this document is first among equals

Research on human participants without institutional oversight is not automatically wrong — a great deal of legitimate independent research happens outside universities. But it puts the entire ethical burden on you, personally, with no committee to catch mistakes.

The failure mode is not malice. It is a well-intentioned researcher who collects data from people with less power than them, under consent that was technically obtained but not meaningfully given, and only realises the problem when someone else points it out publicly.

Build the safeguards in now, while it costs nothing.

---

## 1. Ethical oversight

### Preferred: institutional affiliation

You have college contacts. Use them. Approach a psychology, management, or social-sciences department and ask whether a faculty member will serve as an advisor and route the protocol through their Institutional Ethics Committee (IEC).

What this gets you:
- Genuine external review by people trained to spot problems you can't see
- Legitimacy for any future publication — most journals require ethics approval
- A named advisor, which strengthens the work considerably

What it costs you: a few weeks, some paperwork, and giving up unilateral control of the protocol. Worth it.

### Fallback: independent review panel

If no institution will affiliate, constitute a panel of **three to five people** who are not on the project:

- At least one with research-methods training
- At least one with no stake in the project succeeding
- At least one who can represent participant interests — ideally someone connected to the NGO population but not employed by the NGO

Document their review in writing. Give them real authority to require changes. A panel that has never asked for a change is not doing its job.

### Not acceptable

Proceeding with no external review at all, on the reasoning that the study is low-risk. It probably is low-risk. That judgement should not be made solely by the person who wants the data.

---

## 2. The NGO channel — the hard part

### The problem, stated plainly

If participants are beneficiaries of the NGO's services, three things are true simultaneously:

1. They may believe participation affects their access to services, even if you never suggest it.
2. The NGO's staff have authority over them, so an NGO-relayed invitation carries implicit pressure.
3. They may have lower formal education, lower digital literacy, or limited English — making a standard online consent form functionally meaningless.

None of this makes the research unethical. All of it means standard procedures are insufficient.

### Mandatory safeguards

**Decouple from services, visibly.**
- Recruitment materials state prominently: *"Taking part or not taking part will make no difference to any service you receive."*
- The invitation is not delivered by anyone with authority over the participant. Not their caseworker, not their programme officer.
- Ideally, recruitment happens through a general notice rather than individual approach.

**Ensure comprehension, don't assume it.**
- Consent materials in the participant's primary language, at a plain-language reading level.
- Offer verbal explanation with the opportunity to ask questions.
- Use a **teach-back check**: ask the participant to say in their own words what the study is about and what happens to their data. If they can't, consent has not been obtained.

**Make withdrawal genuinely available.**
- Explicit statement that they can stop at any point, with no explanation and no consequence.
- A visible "exit" control on every screen, not buried.
- Contact route to delete their data afterwards, that doesn't go through NGO staff.

**Compensate fairly or not at all.**
- If you compensate one channel, compensate all. Differential compensation by population is exploitative.
- Compensation should not be large enough to be coercive for a low-income participant. A small token or nothing is safer than an amount that makes refusal costly.

**Exclude anyone under 18** unless you have a specific, reviewed protocol for minors including guardian consent. Given NGO populations often include young people, put a hard age gate in the flow, and be aware that a self-declared age gate is weak — the NGO channel needs human verification.

### The question worth asking yourself

*What does the NGO population get out of this?*

If the honest answer is "nothing, they're a convenient sample," that's a problem. Not fatal, but it should push you to either (a) find genuine value to return — a report the NGO can use, findings relevant to their work, skills training — or (b) reconsider whether that channel is necessary.

A defensible answer might be: the research addresses whether assessment instruments developed on Western, educated samples work for populations like theirs. That's real value, and it's true. But you have to actually do that analysis and share it, not just say it in the consent form.

---

## 3. Consent architecture

### Layered consent

Do not use a single wall of text with one checkbox. Use progressive disclosure:

**Layer 1 — Plain summary (always visible)**
> This is a research study about how people answer different kinds of questions. It takes about 10 minutes. Your answers are stored without your name. You can stop any time. Taking part is entirely your choice.

**Layer 2 — Expandable detail**
- What the research is trying to find out
- Exactly what data is collected (including response times and device type — people don't expect these)
- Who can access it
- How long it's kept
- What happens if it's published
- How to withdraw

**Layer 3 — Full information sheet (downloadable)**
Complete protocol description, contact details, review body.

### Granular, separated permissions

Separate checkboxes, all defaulting to unchecked:

- [ ] I agree to take part in this study *(required)*
- [ ] I agree that my anonymised responses may be used in research publications *(required)*
- [ ] I agree that my anonymised data may be included in a **public open dataset** *(optional — must be genuinely optional)*
- [ ] I would like to receive a summary of the findings by email *(optional)*

The open-dataset permission must be separate and optional. Bundling it into required consent is a common and serious error — public release is irreversible and materially different from internal research use.

### Prohibited patterns

- Pre-ticked boxes
- Consent bundled with terms of service
- "By continuing you agree..." with no affirmative action
- Making the withdrawal option visually subordinate to the continue option
- Any dark pattern that makes declining harder than accepting

---

## 4. DPDP Act 2023 compliance (India)

India's Digital Personal Data Protection Act governs this. Key obligations as they apply here:

| Requirement | Implementation |
|---|---|
| **Notice** | Itemised notice at collection: what data, what purpose, how to withdraw, how to complain |
| **Consent** | Free, specific, informed, unconditional, unambiguous, with clear affirmative action |
| **Purpose limitation** | Use data only for stated research purposes. Using it later for a commercial product is a new purpose requiring fresh consent |
| **Data minimisation** | Collect only what the analysis plan requires. If you can't name the analysis a field feeds, don't collect it |
| **Withdrawal** | Withdrawal must be as easy as giving consent. Build the mechanism, don't just promise it |
| **Erasure** | Provide a route to delete. Note that truly anonymised data may be exempt — but only if genuinely non-re-identifiable |
| **Security** | Reasonable safeguards: encryption at rest, TLS in transit, access control, no production data on laptops |
| **Breach notification** | Have a written response plan before you need it |
| **Children** | Under-18 data requires verifiable parental consent, and behavioural monitoring of children is restricted. Simplest path: exclude minors entirely |

**Status caution:** the DPDP Rules were still being finalised through 2025 and operational specifics may have changed. Verify current requirements before launch — my knowledge has a cutoff and this is exactly the kind of thing that moves.

### Anonymisation, done properly

- **Never store direct identifiers alongside responses.** If you collect email for results delivery, it lives in a separate table with a one-way link, or better, a separate system entirely.
- **Use participant codes**, generated randomly, not derived from anything.
- **Watch quasi-identifiers.** Age + city + job title + employer can uniquely identify someone in a small sample. Collect age in bands, city at state level, industry not employer.
- **Free-text is a re-identification risk.** M2 divergent-thinking responses are open text. Screen before any public release.

---

## 5. Participant welfare

### Time pressure and distress

Timed tasks create mild stress by design. This is acceptable and low-risk, but:

- Warn in advance that some sections are timed. Surprise time pressure is meaningfully worse than expected time pressure.
- Never use failure feedback, negative scores, or comparative ranking during the session.
- Provide a pause mechanism between modules.
- If a participant times out on most items, don't display that as failure.

### Feedback to participants

Giving feedback is the main non-monetary incentive and substantially improves completion. But:

- Frame everything as **descriptive, not evaluative**. "You tend to prefer structured approaches" — not "You scored low on flexibility."
- **No M3 (reasoning) scores.** Telling someone they performed poorly on a reasoning test is unkind and serves no research purpose.
- **No M5 (ethics) scores presented as moral quality.** Describe reasoning style only.
- Add a clear caveat: *"This is a research instrument under development. These results are not validated and should not be used for any decision about you."*

### Distress route

Low probability, but have it: a visible link to general mental-health support resources, and a contact address that a real person monitors. If a participant discloses distress in free text, you need a plan that isn't improvised.

---

## 6. Governance and documentation

Keep a written record of:

- Protocol versions, with dates and changes
- Ethics review correspondence and approvals
- Consent form versions (you need to know which version each participant saw)
- Data access log — who accessed what, when
- Any adverse events or complaints, and the response

This sounds bureaucratic for a solo project. It is what separates research from data collection, and it is what you will need if anyone ever asks.

---

## 7. Red lines

Do not, under any circumstances:

- Use research data for a commercial product without fresh, specific consent
- Share individual-level data with employers, the NGO, or colleges
- Allow any party to use scores for selection, admission, or benefit decisions during the research phase
- Publish data that could re-identify a participant
- Continue recruiting from a channel after concerns are raised, before resolving them
- Let the desire for a larger N override consent quality

The last one is the realistic risk. When N is at 180 and you need 300, the temptation to relax recruitment standards is real. Decide now, while it's abstract.

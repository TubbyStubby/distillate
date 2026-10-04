# Flavours

Every flavour shares the same building blocks: header, tiers, concept sections, toys, cards. What changes is which blocks appear, how deep they go, and what the page ends with. Pick one, read its entry, then outline.

Contents:
1. Concept + build (default)
2. Concept only
3. Build sheet
4. Decision brief
5. Course correction
6. Mixing flavours

---

## 1. Concept + build (default)

**Reader:** someone who is going to build the thing, usually a teammate who is new to this part of the system.
**Goal:** they understand the mechanism well enough to build the right thing, and they know what to leave out.
**Length:** 12–18 minutes, about 12–16 sections across all tiers. **Toys:** 5–8.

Structure:

```
Header: kicker, title, lede (the one question), "short version" line
Tier 1 (core)
  Concept sections (2–4), each: setup → toy/diagram → takeaway
  How to build it: 4–6 numbered steps, one code sketch, a validation step
  Where to spend your time: Focus on / Leave out
  What it can't tell you: short limits section
Tier 2 (extension, e.g. inputs, data, scale)
  Concept sections (2–3) → How to build → Focus / Leave out, plus an optional pull quote
Tier 3 (optional extras)
  "Optional" kicker + must-have / good-to-have ladder
  One section per extra, each with a toy where it helps
  A suggested build order for the extras
  Focus / Leave out for extras
Footer: what the demos are, and what they're modelled on
```

The first concept section of tier 1 should make the core mechanism tangible, with something the reader can step through. If the reader's trap is overbuilding, the second section usually shows what can be stripped away (the reveal-toggle diagram pattern).

---

## 2. Concept only

**Reader:** someone who has to understand and reason about the thing without building it: a new teammate, a PM, a reviewer, support, a neighbouring team.
**Goal:** a correct mental model they can use to predict behaviour and spot nonsense.
**Length:** 10–15 minutes, about 8–11 sections. **Toys:** 4–6, usually one centrepiece workbench plus a few satellites.

Swap out "How to build it" and "Where to spend your time", and use that space to go deeper on each concept:

```
Header
Tier 1 (core)
  The mechanism: one section with the centrepiece workbench. Its scenario presets come from the
    situations the reader actually meets (the complaints, tickets or reports they field)
  Concept sections (2–3) for what the centrepiece doesn't show on its own, each: setup → toy → takeaway
  What changes what: sliders on the centrepiece or one small sensitivity toy,
    followed by a short table of "turn this up → expect that"
  Common misreadings: 3–5 items, each "It's tempting to think X. Actually Y."
    with a pointer to the preset or toy that shows it ("Try: ...")
  Edge cases and limits
Tier 2 (extension), only if the source really has a second layer
  Same pattern, lighter
Closing
  The mental model in one picture or 5–7 sentences
  Check yourself: 3–5 questions, answers in <details> blocks
Footer
```

Code appears only when the code *is* the concept (an interface, a formula), at most one short snippet. Swap "you'll build" phrasing for "you'll see" and "this means".

If the reader has to *act* on the understanding (answer customers, triage reports), fold that into the misreadings section ("what's happening" plus "what to say") instead of adding separate sections for it. Depth here means a sharper model, not more sections.

---

## 3. Build sheet

**Reader:** someone who already understands the idea (maybe they read the concept page) and now has to execute.
**Goal:** they can work through it step by step and know when each step is done.
**Length:** 5–10 minutes. **Toys:** 0–2, only to show a pitfall that is easier to see than to describe.

```
Header: title, one-paragraph recap of the concept, one diagram of the moving parts
Per tier:
  Steps (5–8). Each step: what to do, inputs, outputs, "done when" (a checkable condition)
  One code sketch per tier, in the project's real language and interfaces
  Validation checklist: how to know the whole tier works
  Focus / Leave out
Pitfalls: 3–6 known traps, each with the symptom you'd see and the fix
Footer
```

Steps carry more detail here than in the default flavour, but stay skimmable. Put details in a sentence after the heading, not in a paragraph.

---

## 4. Decision brief

**Reader:** a lead or stakeholder who has to decide whether to fund, approve or choose between options.
**Goal:** they can decide in five minutes and defend the decision.
**Length:** about 5 minutes. **Toys:** 1–2, ideally the one that shows the core trade-off.

```
Header: title, then the question and the recommendation in the lede (answer first)
Headline numbers: 2–4 figures the decision turns on (cost, time saved, risk), shown as a small row of stat tiles, each with a one-line label
What it is: two short paragraphs + one toy or diagram showing the core trade-off
Options: 2–4 option cards, each with what you get, what it costs, and the main risk
Recommendation and why: one short section
Tiers as effort: a must-have / good-to-have ladder with rough effort per item
Risks and limits
How we'll know it works: the validation milestones, in order
Footer
```

No code. Effort in rough units the team uses (days, sprints). Name the trade-off honestly, including what the recommendation gives up.

---

## 5. Course correction

**Reader:** someone already building, in a direction that costs far more than it needs to or answers the wrong question.
**Goal:** they switch direction without feeling foolish, and keep whatever they built that's still useful.
**Length:** 12–18 minutes. **Toys:** 5–8.

```
Header: lede frames the question the work is meant to answer, not the mistake
The tempting approach and the one that answers the question:
  Side-by-side or reveal-toggle diagram. Say honestly why the tempting approach is tempting
  (it looks thorough, it mirrors production), then show what it costs and what it doesn't buy
Then the default flow (concept + build), with extra weight on the tier where the wrong turn happened.
  Leave-out lists carry the specifics of the wrong turn
If you've already built some of this: a "keep / set aside" list, so the work isn't wasted
Footer
```

Never name the person or describe what they did. Describe the approach, in the third person, as something anyone might reach for. The tone is a colleague saving someone a week, not a reviewer marking errors.

---

## 6. Mixing flavours

Users may ask for combinations ("concept only, but add a short build checklist at the end", "a brief with one deep-dive toy"). Start from the closest flavour and add the requested block, keeping the tier rhythm. Say which flavour you started from.

# Page anatomy and writing

Contents:
1. Header
2. Concept section
3. Build steps
4. Focus / Leave out cards
5. Limits section
6. Optional tiers and the ladder
7. Footer
8. Writing rules
9. Annotated outline of a page that worked

---

## 1. Header

- **Kicker:** small uppercase line naming the domain and the page type, e.g. "Matchmaking · scorer simulator guide".
- **Title (`<h1>` and `<title>`):** a short name for the thing being explained, 2–4 words, e.g. "Simulating the matchmaker". Not a sentence, and no colon with an explanation after it.
- **Lede:** 2–3 sentences. Start with the one question the thing answers ("We want to answer one question, fast: …"), then what the page covers.
- **Short version:** one muted line with the whole point in a sentence ("Short version: the simulator is a `for` loop in one Go process."). Skip it if there's no honest one-liner.

## 2. Concept section

```
<h2>  the idea, stated plainly ("A matchmaker is a loop")
<p>   setup: what happens / what the problem is (1–3 short paragraphs)
<p>   how to read the toy: what the axes, colours and marks mean, and what to press
[toy or diagram, with a one-line hint about what to try]
<p>   takeaway: name what the reader just saw and why it matters (1–2 paragraphs)
<p class="pull">  optional single-sentence line worth remembering (max one per tier)
```

Headings are claims or plain nouns. "Most of production is plumbing" works because it states the finding. "Architecture overview" says nothing, and so does a pun.

Explain the toy's encoding in the prose *before* the toy ("each dot is a ticket; left to right is skill; higher means it has waited longer"). A reader who doesn't know what they're looking at can't learn from it.

## 3. Build steps

- A numbered list, because order is real: inputs → core → validation → comparison → speed.
- Each step: a short `<h3>` that is an instruction ("Check it against production"), then 1–3 sentences saying what to do and why.
- Always include a validation step before any step that draws conclusions. "Don't skip this step" is one of the few places a firm tone is right.
- At most one code sketch per tier, 10–25 lines, in the project's real language, using its real interfaces and names. Comments on the right explain the non-obvious lines. It's a sketch: helper functions can be left unimplemented if their names say what they do.

## 4. Focus / Leave out cards

- Two cards side by side ("Focus on" ✓, "Leave out" ✕), 4–6 items each.
- Items are short, ideally one line. A leave-out item says what to do instead when that isn't obvious ("Live event streams; read exported files instead").
- The leave-out card is where the reader's trap is addressed directly. Phrase it as plain guidance, never as blame.
- One per tier, with the heading adjusted: "Where to spend your time", "… on synthetic traffic", "… on extras".

## 5. Limits section

Short, honest, at the end of the core tier: what the approach can't tell you, and what to do about it ("confirm big changes with a small production experiment"). It builds trust in everything above it.

## 6. Optional tiers and the ladder

The first optional tier opens with an "Optional" kicker, a heading, a paragraph saying these are good-to-haves to build after the core works, and a two-row ladder of chips:

```
Must have     [core item] [core item] [validation] [comparison]
Good to have  [extra] [extra] [extra] [extra]
```

Each extra then gets its own concept section, usually with a toy. Close the tier with a suggested build order for the extras and a Focus / Leave out pair.

## 7. Footer

One line: the demos use toy models and made-up numbers, and what they're modelled on in the real system.

---

## 8. Writing rules

Voice:
- Second person, present tense, active voice. "You replay the arrivals", not "arrivals are replayed by the harness".
- Plain words first. Introduce a term of art once, in context, then use it consistently.
- Short sentences. One idea each.
- Warm and direct. Assume the reader is smart and new to this.

Content:
- Problem before solution. Mechanism before rule.
- Real numbers when you have them ("a day is 17,280 ticks"), exact counts over adjectives ("11k calls per tick" over "lots of calls").
- Only claim what the toy shows or what you verified. When numbers are illustrative, say so.
- Say what to skip, and why, as plainly as what to do.

Avoid:
- Em-dash asides and parenthetical chains. Split the sentence instead.
- "Not X, but Y" framing, colon-then-reveal sentences, and scare quotes around made-up labels.
- Stock phrases: "it's worth noting", "at the end of the day", "honest caveat", "let's dive in".
- Emoji as section markers, and exclamation marks.
- Names of the source branch, PR, people or tickets (unless the user asks for them).

Length targets:
- Section prose: about 60–180 words.
- Whole page: 10–20 minutes of reading for concept and course-correction flavours, about 5–10 for build sheet and brief.
- A section that needs more than about 250 words is usually two sections.

---

## 9. Annotated outline of a page that worked

This is the shape of a "concept + build" page that explained how to build a matchmaking scorer simulator to a junior engineer who had started by running all of production's infrastructure locally. Use it to calibrate structure, pacing and tone, not as content to reuse.

```
Header  "Simulating the matchmaker"; lede = one question (is scorer B better than A?);
        short version = "it's a for loop in one process"

Tier 1: the main loop
  A matchmaker is a loop            stepper toy: tickets arrive, pairs match, leftovers wait
  Most of production is plumbing    reveal toggle: 14 boxes → 7 essential ones in one loop
                                    (aimed straight at the reader's trap)
  Replay over time, not one         same-input race: two scorers, sliders, winner-marked table
    snapshot                        + pull quote
  How to build it                   5 steps; Go sketch with the real interface; validation step
  Where to spend your time          focus / leave out (the infra list lives here)
  What it can't tell you            limits

Tier 2: synthetic inputs
  Synthetic tickets, for questions  flow diagram: two sources → same input type → same loop;
    the logs can't answer             crossed-out path for the tempting wrong use
  Arrivals have a shape             shape switcher with per-period table (claim rewritten
                                      after headless verification showed averages barely moved)
  A ticket's fields belong together joint vs independent scatter, marginals unchanged
  How to build the generator        5 steps + sketch
  Where to spend your time …        focus / leave out + pull quote

Tier 3: extras (optional)
  Extras that make it a joy to use  ladder of must-have vs good-to-have
  Rejections that explain           reason bars + drilldown, first-vs-every toggle
    themselves
  Follow one ticket                 single-entity journey
  Plugging in scorers without a     cost counter with exact counts + three option cards
    rebuild
  A workbench on top                build order for the UI
  Where to spend your time …        focus / leave out

Footer  "the demos use a made-up scorer and made-up traffic …"
```

What made it work: one question up front; the trap answered in the second section; every tier with the same rhythm; toys that each prove exactly one claim; and no mention of the branch the material came from.

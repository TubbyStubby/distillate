---
name: distillate
description: Distill a messy source (a branch, PR, design doc, codebase, experiment, Slack thread or long conversation) into one interactive explainer page that teaches the underlying concept in priority tiers, with small playable toy models and, depending on the flavour, how to build it. Use this whenever someone wants to explain a system or approach to a teammate, write an onboarding primer or field guide, turn a branch or experiment into a guide, steer someone who went off in the wrong direction, write a decision brief for a lead, or make an explorable explanation in the style of samwho.dev, even if they never say "distill".
---

# Distillate

Distillate turns a pile of specifics into the concept underneath, and presents it as one friendly, interactive web page. The source might be a branch with fifty features, a design doc, a pile of experiment notes, or a long conversation. The reader doesn't need that history. They need the mechanism, the priorities, and enough hands-on feel to believe it.

The page is about the **concept**, not about the source. A reader should come away knowing how the thing works and what matters most, without ever learning which branch it came from or who tried what.

## Pick a flavour

Infer the flavour from the request. If it isn't clear, use the default and name the flavour in one line of your reply so the user can redirect.

| Flavour | Reader | What it trades | Toys |
|---|---|---|---|
| **Concept + build** (default) | Someone who will build it | Balanced: concept, then how to build, per tier | 5–8 |
| **Concept only** | Someone who needs to understand and reason about it | Drops build steps for more depth: sensitivity, misreadings, a mental model | 4–6 |
| **Build sheet** | Someone who already gets the idea and has to execute | Drops most concept for detailed steps, done-when checks, code sketches | 0–2 |
| **Decision brief** | A lead or stakeholder deciding what to fund or approve | Answer first, options and trade-offs, effort tiers, no code | 1–2 |
| **Course correction** | Someone already building in the wrong direction | Opens with tempting-vs-right, then the default flow, ends with what to keep | 5–8 |

Cues: "explain", "intro", "why does" → concept only. "Checklist", "steps", "they already know" → build sheet. "For my lead", "should we", "pitch" → decision brief. "Went off in the wrong direction", "stop them doing X" → course correction. Each flavour's full structure is in `references/flavours.md`. Read the one you pick before outlining.

## Process

1. **Read the whole source.** Code, diff, docs, thread, whatever was given. Note five things: the one question the thing exists to answer; the core mechanism; every feature or component; the mistakes, dead ends and slow parts; and the domain's real vocabulary, units and numbers.

2. **Find the reader and the trap.** Who reads the page, what they already know, and what wrong turn they took or are likely to take. The trap decides where the emphasis goes. A whole section can exist just to show what to skip. The page never blames the reader or names who made the mistake.

3. **Distill.** Apply the rules in "What stays, what goes" below.

4. **Sort into tiers.** Group everything into 2–4 tiers by how necessary it is, for example core loop → extension → extras. Each tier gets the same rhythm of sections, so the reader learns the page's shape once. Mark later tiers as optional, and open the first optional tier with a "must have / good to have" ladder.

5. **Outline and choose toys.** For each section decide whether it needs a toy, a diagram, or just text. A toy earns its place when the claim is about behaviour over time, a trade-off, an accumulation, or a comparison on the same input, so the reader believes it faster by poking than by reading. Static structure gets a diagram (`references/diagrams.md`), and static facts get a sentence. When one mechanism sits under most of the page, build a single centrepiece workbench for it, with scenario presets taken from the situations the reader actually meets, and let later sections point back to it instead of adding toys. See `references/interactives.md` for the toy patterns.

6. **Verify the toys before writing claims.** Write the toy's logic first and run it headless (Node or Python) with the default settings across a few seeds. Read the numbers, then write only the claims they support. If a planned claim doesn't hold, change the claim or the toy, never the numbers. This step regularly saves a page. For example, you might expect a setting to change an average when it really changes how results are spread over time. The section then gets rewritten around the true finding, which is usually more interesting anyway.

7. **Build the page** from `assets/template.html`. It holds the design tokens, the components and the toy helpers (seeded RNG, canvas setup, animation loop). Section anatomy and writing rules are in `references/page-anatomy.md`.

8. **Check, then publish.** Run `python scripts/check_page.py <page.html> --flavour <name>` (names: `concept-build`, `concept-only`, `build-sheet`, `brief`, `course-correction`). It syntax-checks the script with Node and flags common slips. If the environment can publish artifacts or preview pages, publish the HTML that way. Otherwise save it and give the path. In the reply, say briefly what's on the page and what you verified, including any claim you softened because the numbers didn't support it.

9. **Extend in place.** Users often come back with "keep this as is, and after section X add Y". Insert the new sections at that spot and leave every existing section untouched. Reuse the established components, voice and section rhythm. Republish to the same place.

## What stays, what goes

- **Name the domain, not the source.** Keep the real system's vocabulary, interfaces, units and numbers: they ground the reader and are what they'll meet in the code. Drop the provenance: branch and PR names, commit history, the experiment's file paths, who wrote what, how far along it got.
- **Turn the source's choices into general guidance.** Good choices become recommended steps. Bad ones become "leave out" items, or at most one cautionary line ("an earlier attempt called the script once per pair, and it got slow"). Some bias from the source in the leave-out lists is fine, as long as each item would help someone who never saw the source.
- **Explain the mechanism behind every recommendation.** "It got slow" is weak. "It converted both tickets on every pair, n² times per tick" lets the reader reason about their own case.
- **Don't be stricter than the evidence.** Prefer "aim for", "usually" and a reason over absolute rules. The page guides, it doesn't legislate.
- **Let the user steer.** If they ask for it to be about their specific branch, team or codebase, or to call out a specific implementation, do that. These rules are defaults, not walls.

## The shape that works

Each tier follows the same rhythm (adjusted per flavour):

1. **Concept sections.** The heading states the idea in plain words ("A matchmaker is a loop", "Most of production is plumbing"). One to three short paragraphs set up the problem, then the toy or diagram, then a short takeaway that names what the reader just saw.
2. **How to build it.** Numbered steps, because order matters. Four to six steps, each a short heading plus a few sentences, with at most one code sketch per tier. Include a "check it against the real thing" step before any step that compares or concludes.
3. **Where to spend your time.** Two cards, "Focus on" and "Leave out", with four to six short items each. This is where the trap gets addressed head-on.
4. **Limits.** At the end of the core tier, say plainly what the approach can't tell you.

A pull quote of one sentence can close a tier when there's a line worth remembering. Use at most one per tier.

## Writing

Write the way a kind senior engineer explains something at a whiteboard: second person, plain words, short sentences, problem before solution, mechanism before rule. Use real numbers when you have them, and exact counts over adjectives. Keep each section's prose to roughly 60–180 words, and keep the whole page inside its flavour's budget in `references/flavours.md`. Length is the most common way a distillate goes wrong, especially in the concept-only flavour, where "more depth" tempts you to add sections. Depth means a sharper model, not more sections. When the checker warns about length, merge sections that make the same point before adding polish. Every toy gets a one-line hint about what to try. The full style notes, including phrasing to avoid, are in `references/page-anatomy.md`.

## Design

Light, welcoming and simple, in the spirit of samwho.dev: a soft neutral background, white cards, friendly rounded display type, and a small set of clear colours that mean the same thing everywhere on the page. Avoid neon, dark-first or "terminal" looks unless the user asks for one. Keep both light and dark themes working through the template's tokens. Reuse the template's components instead of inventing new ones per section, so the page feels like one piece.

The look is steerable from the prompt. A user can name a preset (Soft, Paper, Night), give brand colours and a font, or point at their design system. Steering changes the tokens, never the components, and the colour roles stay the same. Presets, the token map and the order to choose in are in `references/themes.md`.

## Reference files

- `references/flavours.md`: structure, length and toy budget for each flavour. Read the chosen flavour before outlining.
- `references/page-anatomy.md`: header, section, step and card anatomy, writing rules, and an annotated outline of a page that worked well.
- `references/interactives.md`: when a toy earns its place, the toy pattern catalogue, how to choose, tweak or invent a toy, the rules every toy follows, and how to verify a toy's claims headless.
- `references/diagrams.md`: the diagram catalogue (flow, crossed-out path, before/after, sequence, state, layers, timeline) and diagram rules.
- `references/themes.md`: the token map, theme presets, brand theming and the post-retheme checks.
- `assets/template.html`: the page skeleton with tokens, components and JS helpers. Copy it, then fill it in.
- `scripts/check_page.py`: pre-publish checks.

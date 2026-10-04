# Diagrams

A diagram shows structure that doesn't change: what talks to what, where data flows, what state something moves through. If the point is behaviour over time or a trade-off, it's a toy (`interactives.md`). If a sentence says it faster, write the sentence.

Draw diagrams as inline SVG using the template's `.flow` classes (boxes, `ok`/`no` paths, labels), so they follow the theme tokens. Every diagram sits in a `<figure>` with a one-sentence `<figcaption>` stating what it shows, and the `<svg>` gets `role="img"` plus an `aria-label` carrying the same claim.

## Catalogue

**Flow.** Boxes and labelled arrows from input to output. Use it for "where the data goes". Highlight the boxes the page is about (`.box.key`) and leave the rest plain.

**Two sources, one path.** Two or more inputs that produce the same type and feed the same pipeline. Use it for "real and synthetic data are interchangeable to the loop", or "batch and live requests share this code".

**Crossed-out path.** A dashed red path with an ✕ and a short label ("load test, not a simulation"). Use it to show a tempting wrong use right next to the right one. It's the most direct way to address a trap visually.

**Before / after.** The same system drawn twice, side by side, with the changed part highlighted. Use it for migrations and redesigns. Draw the difference, not two unrelated pictures.

**Sequence.** Lanes for actors (client, gateway, store) with time running down and labelled messages between them. Use it for request lifecycles, retries and handshakes. Keep it to 3–5 lanes.

**State.** States as rounded boxes, transitions as labelled arrows (event → effect). Use it for lifecycles such as ticket states, order states or circuit breakers. Mark the start state, and mark the terminal states with a double border.

**Layers.** Stacked horizontal bands, with the layer under discussion highlighted. Use it for "where does this logic live".

**Timeline.** Horizontal time with milestones and phases. Use it in decision briefs for the plan and the go/no-go gate. Label each phase with its duration.

**Reveal toggle.** This is interactive and lives in `interactives.md`. Use it when the point is how much of a big diagram can be dropped.

## Rules

- **Label the arrows.** `writes`, `polls every 5s` and `returns 429` carry information. A bare arrow means "related somehow".
- **One diagram, one claim.** If the caption needs "and", split the diagram or cut it.
- **Draw the parts the argument depends on.** Leave out the rest, including real components that don't matter to the claim.
- **Keep text short** (1–3 words per label, 11–13px), and align boxes to a grid with even gaps.
- **Use colour for meaning only**, through the tokens: `--go` for the path you recommend, `--b` dashed for the wrong one, `--plumb` for context.
- **Make wide diagrams scroll** inside their own container (`.scroll`), so the page body never scrolls sideways on a phone.

New diagram shapes are fine when none of these fits. Follow the same rules.

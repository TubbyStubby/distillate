# Interactives

Toys are what make a distillate stick. A reader who presses Step and watches a pool drain believes the mechanism in a way no paragraph achieves. Each toy is a small, honest model of one mechanism, built to prove one claim.

Contents:
1. When a toy earns its place
2. Pattern catalogue
3. Rules every toy follows
4. Verifying a toy's claims headless
5. Implementation notes

---

## 1. When a toy earns its place

Use a toy when the claim is about:
- **Behaviour over time:** queues, loops, retries, caches warming, state that accumulates.
- **A trade-off:** turning one knob helps one metric and hurts another.
- **Comparison on the same input:** two strategies, identical inputs, diverging results.
- **Combinatorics or scale:** counts that grow as n², costs per day, fan-out.
- **Hidden structure:** correlations, distributions, the shape behind an average.
- **Reduction:** a big system whose essential part is small (the reveal toggle).

Use a static diagram when the point is structure that doesn't change (what talks to what, where data flows). Use a sentence when the point is a fact.

Budget per flavour is in `flavours.md`. Two toys proving the same claim is one too many.

## 2. Pattern catalogue

Each pattern lists what it proves and its minimum controls.

**Stepper.** One loop, stepped one tick at a time. Proves "the system is a loop, and here's what one iteration does". Controls: Step (primary), Play/Pause, Reset, maybe a "show X" checkbox. Shows counter chips for what happened this tick ("+2 arrived · 1 matched · 0 expired · 5 waiting").

**Same-input race.** Two variants run on identical seeded input, stacked lanes, and a metrics table that marks the winner of each row. Proves "the choice changes outcomes, and here's the trade-off". Controls: Play, Step, Reset, New input, a shared input slider, and one or two sliders per variant. Changing any setting replays from the start with the same input.

**Reveal toggle.** An architecture diagram with two states. In the "full" state everything appears; in the "essential" state, inessential boxes fade out and the essential ones animate into a simple line or loop, with their labels changing to the simplified role. Proves "most of this is plumbing for the question we're asking". Controls: a two-button segmented control. A caption and a component count update with the state.

**Shape switcher.** The same total amount of input arranged in different shapes over time (even, random, bursty). Shows a timeline strip of the input plus a per-period results table. Proves "averages hide where things happen".

**Joint vs independent.** A scatter of two related fields, toggled between real (joint) samples and the same values shuffled independently. The marginal histograms on the edges stay identical, and points that couldn't exist turn a warning colour, with a counter. Proves "each field looks right on its own; the combination is what's wrong".

**Reason bars + drilldown.** Horizontal bars counting categories (rejection reasons, error types), sorted, clickable to show a few example rows with the numbers behind them. A toggle can switch the counting rule (first failing check vs every failing check). Proves "categorised outcomes point at the cause".

**Single-entity journey.** One item's timeline through the system, row per step, colour-coded by outcome. Previous/Next and a "most interesting" jump button. Proves "here's the story behind one long wait".

**Cost counter.** A size slider and a table of exact counts per approach (calls, conversions, per-day totals) with a log-scale bar. Proves "this approach scales as n², that one as n". Use exact arithmetic, never invented timings.

New patterns are welcome when a claim needs one. Keep the same control vocabulary (primary button, Play/Pause, Reset, segmented controls, labelled sliders with a live value).

## 3. Rules every toy follows

- **One claim per toy.** Write the claim down before building. The takeaway paragraph after the toy states it.
- **Deterministic.** A seeded RNG, so the same seed and settings always draw the same picture and the prose can describe what the reader will see. Offer "New input" to change the seed.
- **Complete at rest.** On load, pre-run some steps instantly so the toy already shows a realistic state. An empty canvas teaches nothing, and the first frame is what skimmers see.
- **Fair comparisons.** Variants share the same input. Changing a setting replays from the start.
- **Small model, honest labels.** A toy model is a simplification. Say so in a caption or the footer ("Toy scorer: …", "made-up traffic").
- **Readable encoding.** Explain axes, colours and marks in the prose before the toy, and label the canvas itself where space allows ("skill →", "waited ↑", "expires at 60s").
- **A hint.** One small line saying what to try ("Set a high minimum wait and flip the toggle").
- **Accessible.** An `aria-label` on each canvas or SVG, plus live text readouts (chips or a table with `aria-live="polite"`) carrying the same information.
- **Themed.** Colours come from CSS tokens, and canvas code reads them every frame, so a theme switch just works. Respect `prefers-reduced-motion` by snapping instead of easing.
- **Few controls.** One primary action, Play/Pause and Reset, and at most three sliders per toy.

## 4. Verifying a toy's claims headless

Before writing the prose around a toy:

1. Keep the toy's model (the simulation step, the generator, the counting) in plain functions with no DOM access, so they can run outside the page.
2. Copy them into a scratch script (or extract them from the page with a regex) and run with Node across the default settings and at least three seeds.
3. Print the numbers each claim depends on.
4. Decide what's true for most seeds at the defaults:
   - **Clear and consistent:** write the claim, with the size of the effect if it helps.
   - **Inconsistent or noise-level:** don't claim it. Find the real effect (often a breakdown by period, group or tail instead of the mean), or tune the defaults until the true effect is visible, and only then describe it.
   - **Opposite of what you planned:** good, you learned something. Write the true version.
5. Re-run after any change to the model or the defaults.

Never tune the defaults to manufacture a claim that's false in general. Tuning is for making a real effect visible at toy scale.

## 5. Implementation notes

The template (`assets/template.html`) provides:
- `rng(seed)` and `gauss(r)`: a seeded uniform generator and a normal sample from it.
- `css(name)`: reads a CSS custom property (use it for canvas colours each frame).
- `fitCanvas(canvas, height)`: sizes a canvas for its container and the device pixel ratio, returning `{ctx, w, h}`.
- `widgets` and the animation loop: push `{ views: [...], playing, last, interval, step(instant), resize() }`. Each view has `frame(ms)`. The loop calls `step` on an interval while `playing`, and calls `frame` on every view each animation frame.
- Component CSS: `.toy`, `.bar`, `.btn`, `.btn.primary`, `.seg`, `.chip`, `.slider`, `.stats` (with `.win`, `.sel`), `.steps`, `.two`, `.three`, `.pull`, `.ladder`, `.reasons`/`.rbar`, `.journey`/`.jrow`, `.logbar`, and `.reveal` / `.flow` diagram styles.

Patterns that worked well in practice:
- One shared model class (for example a `Lane` with `reset()`, `step()`, `stats()`) reused across several toys on the page, so all the toys agree with each other.
- For easing, give each drawn entity a current and target position plus an alpha, and lerp each frame. Mark entities leaving with a `dieAt` time, and remove them once they have faded.
- For the reveal toggle, build the SVG from a node list `[id, kind, prodX, prodY, label, sub, simIndex, simLabel, simSub]`, position each `<g>` with a CSS `transform` so it animates, and toggle one class on the `<svg>` to fade the plumbing and swap the labels.
- Keep large scripts in one IIFE per toy, so names don't collide.

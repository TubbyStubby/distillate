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

**One centrepiece beats many small toys.** When a single mechanism sits under most of the page (a bucket, a queue, a cache, a loop), build one richer toy for it early on and make it the page's workbench. Later sections then point back to it ("press *Two jobs, one key* above") instead of adding a new toy each. That keeps the page shorter, and the reader gets to know one model well instead of skimming seven. Save separate toys for claims the centrepiece can't show: a different mechanism, a comparison, a distribution.

## 2. Pattern catalogue

Each pattern lists what it proves and its minimum controls.

**Centrepiece workbench.** One live model of the core mechanism, with:
- a clear picture of its state (a bucket's fill level, a pool, a cache), with the number and the reader-facing readout next to it (the header value a customer would see);
- direct controls the reader can poke (send this request, add this item), plus a play speed;
- **named scenario presets** taken from the situations the reader actually meets (the support ticket, the incident, the confusing report). Each preset plays out on its own and ends with a short "Result:" note saying what happened and why;
- **output in the reader's terms**: a log or table of what the outside world saw (status codes, headers, which request was refused, what the user waited), and a small chart over time if it helps.

This proves "here is the whole mechanism, and here is why each familiar situation turns out the way it does". It's usually the best toy on the page, so put real effort into it. Verify each preset's result note headless (section 4).

**Stepper.** One loop, stepped one tick at a time. Proves "the system is a loop, and here's what one iteration does". Controls: Step (primary), Play/Pause, Reset, maybe a "show X" checkbox. Shows counter chips for what happened this tick ("+2 arrived · 1 matched · 0 expired · 5 waiting").

**Same-input race.** Two variants run on identical seeded input, stacked lanes, and a metrics table that marks the winner of each row. Proves "the choice changes outcomes, and here's the trade-off". Controls: Play, Step, Reset, New input, a shared input slider, and one or two sliders per variant. Changing any setting replays from the start with the same input.

**Reveal toggle.** An architecture diagram with two states. In the "full" state everything appears; in the "essential" state, inessential boxes fade out and the essential ones animate into a simple line or loop, with their labels changing to the simplified role. Proves "most of this is plumbing for the question we're asking". Controls: a two-button segmented control. A caption and a component count update with the state.

**Shape switcher.** The same total amount of input arranged in different shapes over time (even, random, bursty). Shows a timeline strip of the input plus a per-period results table. Proves "averages hide where things happen".

**Joint vs independent.** A scatter of two related fields, toggled between real (joint) samples and the same values shuffled independently. The marginal histograms on the edges stay identical, and points that couldn't exist turn a warning colour, with a counter. Proves "each field looks right on its own; the combination is what's wrong".

**Reason bars + drilldown.** Horizontal bars counting categories (rejection reasons, error types), sorted, clickable to show a few example rows with the numbers behind them. A toggle can switch the counting rule (first failing check vs every failing check). Proves "categorised outcomes point at the cause".

**Single-entity journey.** One item's timeline through the system, row per step, colour-coded by outcome. Previous/Next and a "most interesting" jump button. Proves "here's the story behind one long wait".

**Cost counter.** A size slider and a table of exact counts per approach (calls, conversions, per-day totals) with a log-scale bar. Proves "this approach scales as n², that one as n". Use exact arithmetic, never invented timings.

**Threshold slider.** Two overlapping distributions (good vs bad, normal vs incident) with a draggable cut line. Counts of false positives and false negatives update live, plus precision and recall or alert volume. Proves "every threshold trades one kind of error for the other".

**Load vs latency.** A utilisation slider driving a simple queue. It shows the queue length and p50/p99 wait, with a curve that bends sharply near 100%. Proves "latency explodes near capacity, so headroom matters".

**Tail explorer.** A histogram of sampled latencies (or sizes, or costs) with mean, p50, p95 and p99 markers. A slider sets the share of rare slow events. Proves "the average hides the tail, and the tail is what users feel".

**Interleaving explorer.** Two actors, each with a short list of steps. The reader picks which actor moves next (or presses Shuffle) and sees the shared state change, with a highlight when an ordering produces the bug. Proves "this only breaks in one ordering", for races, lost updates and double-spends.

**State machine explorer.** Event buttons and a state diagram with the current state highlighted. Illegal events are disabled, with a short reason on hover, and there's a history of transitions. Proves "these are the only legal paths, and here's how you get stuck".

**Blast radius.** A small dependency graph. Clicking a node fails it, and the failure spreads to everything that depends on it, with counts of affected services or users. A toggle can add a fallback or cache to show what it saves. Proves "what goes down when X goes down".

**What-if calculator.** A few labelled inputs, the formula written out in words, and the outputs updating live, with the user's real numbers as defaults. Good in decision briefs for capacity, cost and throughput. Proves "here's how the numbers combine, so try your own".

### Choosing, tweaking or inventing a toy

Keep this simple:
1. **Write the claim** the toy must prove, in one sentence.
2. **Use a catalogue pattern** whose "Proves" line matches the claim's shape.
3. **Tweak before inventing.** If a pattern is close, adapt it: add scenario presets, change the readout to the reader's terms, swap what the axes show, combine two patterns into one centrepiece. Most good toys are a tweak.
4. **Invent only when nothing fits.** A new toy must still follow every rule in section 3, use the same control vocabulary (primary button, Play/Pause, Reset, segmented controls, labelled sliders with a live value), and be describable in one "Proves …" line. If you can't write that line, it isn't a toy. Use a diagram or a sentence.
5. **Say so in the reply.** When you invent a toy, name it and give its "Proves" line, so it can be added to this catalogue if it works well.

## 3. Rules every toy follows

- **One claim per toy.** Write the claim down before building. The takeaway paragraph after the toy states it. The centrepiece workbench is the exception: one claim per scenario preset.
- **Deterministic.** A seeded RNG, so the same seed and settings always draw the same picture and the prose can describe what the reader will see. Offer "New input" to change the seed.
- **Complete at rest.** On load, pre-run some steps instantly so the toy already shows a realistic state. An empty canvas teaches nothing, and the first frame is what skimmers see.
- **Fair comparisons.** Variants share the same input. Changing a setting replays from the start.
- **Small model, honest labels.** A toy model is a simplification. Say so in a caption or the footer ("Toy scorer: …", "made-up traffic").
- **Readable encoding.** Explain axes, colours and marks in the prose before the toy, and label the canvas itself where space allows ("skill →", "waited ↑", "expires at 60s").
- **A hint.** One small line saying what to try ("Set a high minimum wait and flip the toggle").
- **Accessible.** An `aria-label` on each canvas or SVG, plus live text readouts (chips or a table with `aria-live="polite"`) carrying the same information.
- **Themed.** Colours come from CSS tokens, and canvas code reads them every frame, so a theme switch just works. Respect `prefers-reduced-motion` by snapping instead of easing.
- **Few controls.** One primary action, Play/Pause and Reset, and at most three sliders per toy. A centrepiece can carry more, but group them: state, actions, scenarios, speed.
- **Playback a person can follow.** Default to a pace where the reader can see what one step did: roughly one step per 0.6–1.2 s for a stepper, and a run of under about 30 s for a full scenario. Offer a speed control (1×, 4×, 10×) and Step for anyone who wants it faster or slower. When the data is fine-grained (thousands of events), don't animate every event. Batch them into visible steps (one per tick, minute or request burst), and show a per-step summary chip, so speed never hides what happened.
- **Speak the reader's language.** Show results the way the reader meets them in real life (the response a customer got, the page a user saw, the bill line), not only as internal state.

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
- Component CSS: `.toy`, `.bar`, `.btn`, `.btn.primary`, `.seg`, `.chip`, `.slider`, `.stats` (with `.win`, `.sel`), `.steps`, `.two`, `.three`, `.tiles`/`.tile`, `.pull`, `.ladder`, `.reasons`/`.rbar`, `.journey`/`.jrow`, `.logbar`, and `.reveal` / `.flow` diagram styles.

Patterns that worked well in practice:
- One shared model class (for example a `Lane` with `reset()`, `step()`, `stats()`) reused across several toys on the page, so all the toys agree with each other.
- For easing, give each drawn entity a current and target position plus an alpha, and lerp each frame. Mark entities leaving with a `dieAt` time, and remove them once they have faded.
- For the reveal toggle, build the SVG from a node list `[id, kind, prodX, prodY, label, sub, simIndex, simLabel, simSub]`, position each `<g>` with a CSS `transform` so it animates, and toggle one class on the `<svg>` to fade the plumbing and swap the labels.
- Keep large scripts in one IIFE per toy, so names don't collide.

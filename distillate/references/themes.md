# Themes

The page's whole look lives in one token block at the top of `assets/template.html`: eleven colour tokens (each with a dark-mode twin) and three font tokens. Components and canvas toys read only these tokens, and the canvas code re-reads them every frame. So restyling the page means changing tokens, never components.

Steering comes from the prompt. Pick the look in this order:
1. **The user's words:** "Paper theme", "dark", "use our brand: #0B5FFF and Inter", "match the docs site".
2. **The project's own design system**, if the user points at one or the repo has an obvious one (a tokens file, a theme in CSS or Tailwind config). Map its colours onto the roles below.
3. **The Soft preset**, the default.

Keep the *roles* stable whatever the colours are, because the prose and the toys rely on them ("the green path", "greyed-out boxes").

## Token map

| Token | Role | Safe to change? |
|---|---|---|
| `--bg` | Page background | Yes |
| `--card` | Cards, toys, code blocks | Yes, keep it distinct from `--bg` |
| `--ink` | Body text, primary buttons | Yes, keep 7:1 contrast on `--bg` |
| `--muted` | Captions, labels, axis text | Yes, keep 4.5:1 on `--card` |
| `--line` | Borders, table rules | Yes |
| `--grid` | Chart gridlines, empty tracks | Yes, subtle |
| `--a` | Primary series, variant A, tickets/items | Yes, must read on `--card` |
| `--b` | Second series, variant B, warnings, "leave out" | Yes, must differ clearly from `--a` (also for colour-blind readers) |
| `--go` | Recommended path, "focus on", essential parts | Yes |
| `--sun` | Highlights, focus rings, pull-quote rule | Yes |
| `--plumb` | Infrastructure, inactive, greyed-out | Yes, should look quieter than everything else |
| `--font-display` / `--font-body` / `--font-mono` | Headings / text / code and data | Yes, Google Fonts or system stacks, always with fallbacks |

Change the light set and the dark set together. Both dark blocks (the media query and `[data-theme="dark"]`) must carry identical values.

## Presets

### Soft (default)
Friendly and light, in the spirit of samwho.dev. These are the template's values.

### Paper
Calm and editorial, for briefs and long reads. Cool off-white, serif text, ink-blue accent.
```
light: --bg #f8f8f5  --card #ffffff  --ink #1c2229  --muted #5d6670  --line #e2e2dc  --grid #eeeeea
       --a #2b59c3  --b #b8336a  --go #2f7d5b  --sun #d9a21b  --plumb #a7adb4
dark:  --bg #16191d  --card #1e2227  --ink #e9ecef  --muted #a0a8b0  --line #2f353c  --grid #252a30
       --a #8fb0f5  --b #f08fb4  --go #6cc79f  --sun #f0c45a  --plumb #5a626b
fonts: display "Source Serif 4" 600/700, body "Source Serif 4" 400/600, mono "IBM Plex Mono"
```
Drop the rounded display font. Use slightly smaller radii (8px cards) and a 70ch measure.

### Night
Dark-first, for engineering audiences who live in dark mode. The same fonts as Soft.
```
dark (bare :root): --bg #0f1419  --card #172029  --ink #e6edf3  --muted #93a1af  --line #2a3542  --grid #1d2731
                   --a #79a8ff  --b #ff8fab  --go #5fd4a0  --sun #f5c66b  --plumb #4b5a68
light (mirrored):  use the Soft light values
```
For a dark-first page, put the dark values on bare `:root` with `color-scheme: dark`. Put the light values under `@media (prefers-color-scheme: light)` guarded by `:root:not([data-theme="dark"])`, and again under `:root[data-theme="light"]`.

### Brand
For when the user gives brand colours or a font.
- Put the main brand colour on `--a`. If there's a second brand colour, use it for `--go`. Otherwise keep a green `--go` so "recommended" still reads as positive.
- Keep `--b` clearly different from `--a`, warm if `--a` is cool and the other way round.
- Make each colour's dark twin lighter and slightly less saturated, then re-check its contrast on the dark `--card`.
- Use the brand font for `--font-display` (and body if it reads well at 17px), with a system fallback.
- If a brand colour fails contrast as text, keep it for fills and marks and use `--ink` for text on top.

## Checks after retheming

- Text contrast: `--ink` on `--bg`, and `--muted` on `--card`, as in the token map.
- `--a` and `--b` stay distinguishable side by side in a race toy.
- Both themes still work. Flip the OS theme, or set `data-theme` on `<html>`, and look once.
- `check_page.py` still passes. It warns if a theme block is missing.

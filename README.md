# Distillate

A Claude skill that distills a messy source (branch, PR, design doc, thread) into one
friendly, interactive explainer page, organised in priority tiers with small toy models.

- `distillate/`: the skill itself (`SKILL.md`, `references/`, `assets/template.html`, `scripts/check_page.py`)
- `examples/`: pages made this way (the scorer simulator guide the skill was extracted from)
- `evals/`: test prompts and source fixtures for iterating on the skill

Flavours: concept + build (default), concept only, build sheet, decision brief, course correction.

## Install

**Claude Code (plugin):**

    /plugin marketplace add TubbyStubby/distillate
    /plugin install distillate@distillate

Or from a terminal: `claude plugin marketplace add TubbyStubby/distillate`, then
`claude plugin install distillate@distillate`.

**Claude Code (manual):** copy or symlink the `distillate/` folder to
`~/.claude/skills/distillate/` (all projects) or `<repo>/.claude/skills/distillate/`
(one project).

## Use

Ask for an explainer, guide, primer, brief or course correction from a source, or
call it directly: `/distillate:distillate` after a plugin install, or `/distillate` after a
manual install. Name a flavour or a theme to steer it, for
example "concept only, Paper theme".

## Licence

MIT (see `LICENSE`), except `evals/viewer/`, which is a modified copy of the eval viewer from Anthropic's skill-creator skill and stays under the Apache License 2.0 (see `evals/viewer/LICENSE.txt` and `evals/viewer/NOTICE`).

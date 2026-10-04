# Distillate

A Claude skill that distills a messy source (branch, PR, design doc, thread) into one
friendly, interactive explainer page, organised in priority tiers with small toy models.

- `distillate/`: the skill itself (`SKILL.md`, `references/`, `assets/template.html`, `scripts/check_page.py`)
- `examples/`: pages made this way (the scorer simulator guide the skill was extracted from)
- `evals/`: test prompts and source fixtures for iterating on the skill

Flavours: concept + build (default), concept only, build sheet, decision brief, course correction.

Install for Claude Code by linking the skill folder into your skills directory:

    ln -s ~/Projects/distillate/distillate ~/.claude/skills/distillate

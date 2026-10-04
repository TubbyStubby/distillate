#!/usr/bin/env python3
"""Pre-publish checks for a Distillate page.

Usage: python check_page.py page.html [--flavour concept-build|concept-only|build-sheet|brief|course-correction]

Errors (exit 1): missing <title>, a script that fails `node --check`.
Warnings: leftover template placeholders, missing theme blocks, em dashes in the
visible text, canvases/SVGs without an aria-label, unusual external hosts.
Also prints a rough reading time and the section list, to sanity-check pacing.
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

ALLOWED_HOSTS = (
    "fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com",
    "cdn.jsdelivr.net", "unpkg.com",
)
# (max words, max sections) before a "too long" warning, per flavour
BUDGETS = {
    "concept-build": (3400, 18),
    "course-correction": (3400, 18),
    "concept-only": (2600, 11),
    "build-sheet": (2200, 12),
    "brief": (1800, 9),
}
PLACEHOLDERS = (
    "PAGE NAME", "DOMAIN · GUIDE TYPE", "THE ONE QUESTION", "ONE SENTENCE",
    "THE IDEA, STATED PLAINLY", "DESCRIBE WHAT THE CANVAS SHOWS", "HINT:",
    "STEP AS AN INSTRUCTION", "STEP WITH A SKETCH", ">ITEM<", "EXTRAS HEADING",
    "REAL SYSTEM DETAILS", ">CORE<", ">EXTRA<",
)


def visible_text(src: str) -> str:
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<pre\b.*?</pre>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)


def main() -> int:
    args = sys.argv[1:]
    flavour = "concept-build"
    if "--flavour" in args:
        i = args.index("--flavour")
        flavour = args[i + 1] if i + 1 < len(args) else ""
        args = args[:i] + args[i + 2:]
    if len(args) != 1 or flavour not in BUDGETS:
        print(__doc__)
        return 2
    path = args[0]
    max_words, max_sections = BUDGETS[flavour]
    src = open(path, encoding="utf-8").read()
    errors, warnings = [], []

    m = re.search(r"<title>(.*?)</title>", src[:8192], re.S | re.I)
    if not m or not m.group(1).strip():
        errors.append("no <title> in the first 8KB")
    else:
        title = m.group(1).strip()
        words = len(title.split())
        if ":" in title or " - " in title or words > 5:
            warnings.append(f"title '{title}' reads like a caption; aim for a 2-4 word name")

    for ph in PLACEHOLDERS:
        if ph in src:
            warnings.append(f"template placeholder still present: {ph.strip('<>')}")

    if ":root" not in src or "prefers-color-scheme: dark" not in src or 'data-theme="dark"' not in src:
        warnings.append("theme tokens incomplete: need :root, a prefers-color-scheme dark block and a [data-theme=\"dark\"] block")

    code = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    scripts = [s for s in re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", code, re.S | re.I) if s.strip()]
    node = shutil.which("node")
    if scripts and not node:
        warnings.append("node not found; skipped script syntax check")
    for i, body in enumerate(scripts):
        if not node:
            break
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(body)
            tmp = f.name
        try:
            r = subprocess.run([node, "--check", tmp], capture_output=True, text=True)
            if r.returncode != 0:
                errors.append(f"script #{i + 1} fails node --check:\n{r.stderr.strip()}")
        finally:
            os.unlink(tmp)

    for tag in re.findall(r"<(?:canvas|svg)\b[^>]*>", src, re.I):
        if "aria-label" not in tag and 'aria-hidden="true"' not in tag:
            warnings.append(f"missing aria-label: {tag[:70]}")

    for url in re.findall(r"""(?:src|href)=["'](https?://[^"']+)""", src):
        host = re.sub(r"^https?://", "", url).split("/")[0]
        if not host.endswith(ALLOWED_HOSTS):
            warnings.append(f"external host may be blocked: {host}")

    text = visible_text(src)
    dashes = text.count("—")
    if dashes:
        warnings.append(f"{dashes} em dash(es) in visible text; split those sentences instead")

    words = len(text.split())
    minutes = max(1, round(words / 230))
    if words > max_words:
        warnings.append(f"~{words} words is long for a {flavour} page (budget ~{max_words}); merge sections that make the same point")
    heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", src, re.S)]
    toys = len(re.findall(r'class="toy[" ]', src))
    if len(heads) > max_sections:
        warnings.append(f"{len(heads)} sections is a lot for a {flavour} page (budget ~{max_sections}); merge sections")

    print(f"Page: {path} [{flavour}]")
    print(f"  ~{words} words, about {minutes} min to read, {len(heads)} sections, {toys} toy blocks")
    for h in heads:
        print(f"   - {html.unescape(h)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print("OK" + (" (with warnings)" if warnings else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

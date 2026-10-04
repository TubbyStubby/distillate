#!/usr/bin/env python3
"""Grade Distillate eval runs with scripted checks.

Usage: python evals/grade.py distillate-workspace/iteration-N

Writes grading.json into every <eval>/<config>/ directory that has outputs/page.html.
"""
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "..", "distillate", "scripts", "check_page.py")


def visible(src):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s))


def toys(src):
    # interactive blocks: canvases plus interactive SVG/HTML widgets with controls
    return len(re.findall(r"<canvas\b", src, re.I)) or len(re.findall(r'class="toy', src))


def controls(src):
    return len(re.findall(r'<input[^>]+type="range"|<button\b', src, re.I))


COMMON = [
    ("page.html exists and passes check_page.py with no errors", "checker"),
    ("No source provenance: no people, PR/ticket numbers or branch names from the source", "provenance"),
    ("Supports light and dark themes via tokens", "themes"),
    ("Contains interactive controls (sliders or buttons) wired to toys", "interactive"),
]

PER_EVAL = {
    "cache-eviction-concept-build": {
        "provenance": ["Priya", "Dan", "#812", "edge-cache-v2", "imgcache/", "Mar 13", "Mar 14"],
        "checks": [
            ("Has numbered build steps", lambda s, t: bool(re.search(r"<ol\b", s)) and re.search(r"build", t, re.I) is not None),
            ("Includes a validation step against production / real metrics", lambda s, t: re.search(r"(check|validat|compare)[^.]{0,80}(production|real|live|prometheus|metrics)", t, re.I) is not None),
            ("Leave-out guidance drops the docker / nginx / k6 setup", lambda s, t: re.search(r"leave out", t, re.I) is not None and re.search(r"docker|nginx|k6", t, re.I) is not None),
            ("Distinguishes byte hit rate from request hit rate", lambda s, t: re.search(r"byte hit", t, re.I) is not None and re.search(r"request hit", t, re.I) is not None),
            ("Marks an optional / good-to-have tier", lambda s, t: re.search(r"optional|good to have|good-to-have|nice to have", t, re.I) is not None),
            ("At least 4 toys", lambda s, t: toys(s) >= 4),
        ],
    },
    "rate-limiter-concept-only": {
        "provenance": ["mkowalski", "ana-r", "tjb", "#2291", "INC-4471", "shard 3"],
        "checks": [
            ("No build / implementation steps section", lambda s, t: re.search(r"how to build|implementation steps", t, re.I) is None),
            ("Has a misreadings / common confusions section", lambda s, t: re.search(r"misread|tempting to think|confus|myth|common question", t, re.I) is not None),
            ("Has check-yourself questions with hidden answers", lambda s, t: re.search(r"<details\b", s, re.I) is not None),
            ("Explains that Remaining can go up between requests (refill)", lambda s, t: re.search(r"remaining[^.]{0,120}(go(es)? up|increase|rise|climb|refill)", t, re.I) is not None),
            ("Explains weighted endpoint costs", lambda s, t: re.search(r"export", t, re.I) is not None and re.search(r"20 tokens", t, re.I) is not None),
            ("Within the concept-only length budget (<= 2,600 words, <= 11 sections)", lambda s, t: len(t.split()) <= 2600 and len(re.findall(r"<h2\b", s)) <= 11),
        ],
    },
    "search-replay-decision-brief": {
        "provenance": ["Leo", "Mei", "Sam", "Raj", "Priyanka"],
        "checks": [
            ("Recommendation appears near the top (first 1,200 characters of text)", lambda s, t: re.search(r"recommend|we should|build it|go ahead|yes,", t[:1200], re.I) is not None),
            ("No code blocks", lambda s, t: re.search(r"<pre\b", s, re.I) is None),
            ("Compares options including interleaving and A/B only", lambda s, t: re.search(r"interleav", t, re.I) is not None and re.search(r"a/b", t, re.I) is not None),
            ("Calibration against past A/B tests is a go/no-go milestone", lambda s, t: re.search(r"calibrat", t, re.I) is not None and re.search(r"70", t) is not None),
            ("Short: about 8 minutes of reading or less", lambda s, t: len(t.split()) <= 1850),
            ("1 to 3 toys", lambda s, t: 1 <= toys(s) <= 3),
        ],
    },
    "alerting-burn-rate-paper-theme": {
        "provenance": ["Farah", "Tomasz", "Ines", "OPS-1187"],
        "checks": [
            ("Uses the Paper theme (serif display font and Paper background token)", lambda s, t: re.search(r"Source\+?\s?Serif", s) is not None and "#f8f8f5" in s.lower()),
            ("Has a threshold-style toy (a slider tied to a threshold or cut line)", lambda s, t: re.search(r'type="range"', s) is not None and re.search(r"threshold", t, re.I) is not None),
            ("Explains error budget and burn rate", lambda s, t: re.search(r"error budget", t, re.I) is not None and re.search(r"burn rate", t, re.I) is not None),
            ("Explains the short window stops paging after recovery", lambda s, t: re.search(r"(short|5.?m|5-minute|five-minute)[^.]{0,160}(recover|stop|clear|resolve)", t, re.I) is not None),
            ("Mentions the low-traffic caveat", lambda s, t: re.search(r"low.traffic|quiet hours|few requests|minimum request", t, re.I) is not None),
            ("Stays within about 2,800 words", lambda s, t: len(t.split()) <= 2800),
        ],
    },
    "queue-tail-latency-concept-build": {
        "provenance": ["Gabriel", "Sunita", "Joe", "INC-5530"],
        "checks": [
            ("Has numbered build steps", lambda s, t: bool(re.search(r"<ol\b", s))),
            ("Includes a validation / load-test step before rollout", lambda s, t: re.search(r"(load test|validat|replay|check)[^.]{0,120}(tail|p99|queue|before)", t, re.I) is not None),
            ("Shows latency vs utilisation (a utilisation control and p99)", lambda s, t: re.search(r"utili[sz]ation", t, re.I) is not None and re.search(r"p99", t, re.I) is not None and re.search(r'type="range"', s) is not None),
            ("Explains the average / p50 hiding the tail", lambda s, t: re.search(r"(average|mean|p50|median)[^.]{0,160}(hide|hid|look(ed)? fine|green|tail)", t, re.I) is not None),
            ("Mentions Little's law", lambda s, t: re.search(r"little.s law", t, re.I) is not None),
            ("Includes at least one diagram (figure with SVG)", lambda s, t: re.search(r"<figure\b[\s\S]{0,400}?<svg\b", s, re.I) is not None or re.search(r'class="flow"', s) is not None),
        ],
    },
}


def provenance_hits(text, words):
    hits = []
    for w in words:
        pat = r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])"
        if re.search(pat, text):
            hits.append(w)
    return hits


def grade_run(run_dir, eval_name):
    page = os.path.join(run_dir, "outputs", "page.html")
    exp = []
    if not os.path.exists(page):
        for text, _ in COMMON:
            exp.append({"text": text, "passed": False, "evidence": "no outputs/page.html"})
        for text, _ in PER_EVAL[eval_name]["checks"]:
            exp.append({"text": text, "passed": False, "evidence": "no outputs/page.html"})
        return exp
    src = open(page, encoding="utf-8").read()
    text = visible(src)
    r = subprocess.run([sys.executable, CHECKER, page], capture_output=True, text=True)
    errs = [l for l in r.stdout.splitlines() if l.startswith("ERROR")]
    exp.append({"text": COMMON[0][0], "passed": r.returncode == 0, "evidence": "; ".join(errs) or r.stdout.splitlines()[1].strip()})
    hits = provenance_hits(text, PER_EVAL[eval_name]["provenance"])
    exp.append({"text": COMMON[1][0], "passed": not hits, "evidence": ("found: " + ", ".join(hits)) if hits else "none found"})
    themed = "prefers-color-scheme: dark" in src or "prefers-color-scheme:dark" in src
    exp.append({"text": COMMON[2][0], "passed": themed, "evidence": "dark media query present" if themed else "no dark-mode block"})
    n = controls(src)
    exp.append({"text": COMMON[3][0], "passed": n >= 2, "evidence": f"{n} controls, {toys(src)} toys"})
    for label, fn in PER_EVAL[eval_name]["checks"]:
        ok = bool(fn(src, text))
        exp.append({"text": label, "passed": ok, "evidence": f"toys={toys(src)}, words={len(text.split())}"})
    return exp


def main():
    base = sys.argv[1]
    # Layout: <base>/eval-<id>-<name>/<config>/run-<n>/outputs/page.html
    for dirname in sorted(os.listdir(base)):
        ed = os.path.join(base, dirname)
        eval_name = re.sub(r"^eval-\d+-", "", dirname)
        if eval_name not in PER_EVAL or not os.path.isdir(ed):
            continue
        for config in sorted(os.listdir(ed)):
            cd = os.path.join(ed, config)
            if not os.path.isdir(cd):
                continue
            for run in sorted(os.listdir(cd)):
                rd = os.path.join(cd, run)
                if not os.path.isdir(os.path.join(rd, "outputs")):
                    continue
                exp = grade_run(rd, eval_name)
                passed = sum(e["passed"] for e in exp)
                out = {
                    "expectations": exp,
                    "summary": {"passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": round(passed / len(exp), 3)},
                }
                json.dump(out, open(os.path.join(rd, "grading.json"), "w"), indent=2)
                print(f"{eval_name:32} {config:14} {run:6} {passed}/{len(exp)}")


if __name__ == "__main__":
    main()

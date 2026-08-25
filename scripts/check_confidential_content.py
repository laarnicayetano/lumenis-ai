#!/usr/bin/env python3
"""
Flag possible unreleased-product leaks in skill markdown: this repo is
public, and Claude review alone isn't a reliable enough backstop, so this
is a hard keyword/date lint that runs independently of any model judgment.

Flags two things per line:
  - Keywords that often signal not-yet-public info (upcoming, future
    release, NPI, embargo, ...).
  - Dates that resolve to after today (ISO, "March 2027", "Q3 2027",
    "3/1/2027", etc).

False positives are expected -- this can't judge intent. If a hit is
genuinely fine (an illustrative example, a discussion *about* what
counts as confidential, a real public date), suppress that one line by
appending a marker comment to it:

    ... upcoming webinar on March 3 2027 <!-- confidential-ok: public event -->

Usage: python scripts/check_confidential_content.py
Exits non-zero if any unsuppressed hits are found.
"""
import re
from datetime import date
from pathlib import Path

SEARCH_DIRS = ["plugins", ".claude/skills"]

OVERRIDE_RE = re.compile(r"<!--\s*confidential-ok\b", re.IGNORECASE)

KEYWORDS = [
    "upcoming", "future release", "not yet announced", "unannounced",
    "unreleased", "npi", "embargo", "embargoed", "pre-launch", "prelaunch",
    "under wraps", "internal only", "internal-only",
]
KEYWORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(k).replace(r"\-", "-") for k in KEYWORDS) + r")\b",
    re.IGNORECASE,
)

MONTHS = ("january|february|march|april|may|june|july|august|september|"
          "october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec")
MONTH_NUM = {name: i + 1 for i, name in enumerate([
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
])}
MONTH_NUM.update({
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7,
    "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
})

def _iso(m):
    y, mo, d = (int(g) for g in m.groups())
    return date(y, mo, d)

def _slash(m):
    mo, d, y = (int(g) for g in m.groups())
    return date(y, mo, d)

def _month_day_year(m):
    mo, d, y = m.groups()
    return date(int(y), MONTH_NUM[mo.lower()], int(d))

def _month_year(m):
    mo, y = m.groups()
    return date(int(y), MONTH_NUM[mo.lower()], 1)

def _quarter_year(m):
    q, y = m.groups()
    return date(int(y), (int(q) - 1) * 3 + 1, 1)

DATE_PATTERNS = [
    (re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"), _iso),
    (re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"), _slash),
    (re.compile(rf"\b({MONTHS})\.?\s+(\d{{1,2}}),?\s+(\d{{4}})\b", re.IGNORECASE), _month_day_year),
    (re.compile(rf"\b({MONTHS})\.?\s+(\d{{4}})\b", re.IGNORECASE), _month_year),
    (re.compile(r"\bQ([1-4])\s+(\d{4})\b", re.IGNORECASE), _quarter_year),
]

def iter_markdown_files():
    for base in SEARCH_DIRS:
        yield from Path(base).rglob("*.md")

def check_line(line, today):
    hits = []
    for m in KEYWORD_RE.finditer(line):
        hits.append(f"keyword '{m.group(0)}'")
    for pattern, parse in DATE_PATTERNS:
        for m in pattern.finditer(line):
            try:
                parsed = parse(m)
            except ValueError:
                continue
            if parsed > today:
                hits.append(f"future date '{m.group(0)}' ({parsed.isoformat()})")
    return hits

def check_file(md_file, today):
    findings = []
    for lineno, line in enumerate(md_file.read_text().splitlines(), start=1):
        if OVERRIDE_RE.search(line):
            continue
        for hit in check_line(line, today):
            findings.append((lineno, hit, line.strip()))
    return findings

def main():
    today = date.today()
    failures = []
    for md_file in sorted(iter_markdown_files()):
        for lineno, hit, text in check_file(md_file, today):
            failures.append(f"{md_file}:{lineno}: {hit}\n    {text}")
    if failures:
        print("Possible unreleased-product content found:\n")
        print("\n".join(failures))
        print(
            "\nIf a hit is genuinely fine, append `<!-- confidential-ok: "
            "<reason> -->` to that line rather than deleting the check."
        )
        raise SystemExit(1)
    print("No unreleased-product content found.")

if __name__ == "__main__":
    main()

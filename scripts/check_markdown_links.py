#!/usr/bin/env python3
"""
Find dead relative links in skill markdown files (SKILL.md and their bundled
docs). Checks markdown [text](path) links whose target is not http(s):// —
these are relative paths into the repo and rot silently when a skill is
renamed or moved.

Usage: python scripts/check_markdown_links.py
Exits non-zero if any dead links are found.
"""
import re, sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SEARCH_DIRS = ["plugins", ".claude/skills"]

def iter_markdown_files():
    for base in SEARCH_DIRS:
        yield from Path(base).rglob("*.md")

def resolve(md_file, target):
    # Strip an anchor fragment; drop links Claude Code treats as skill names.
    target = target.split("#", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    return (md_file.parent / target).resolve()

def check_file(md_file):
    dead = []
    text = md_file.read_text()
    for match in LINK_RE.finditer(text):
        resolved = resolve(md_file, match.group(1))
        if resolved is not None and not resolved.exists():
            line = text.count("\n", 0, match.start()) + 1
            dead.append((line, match.group(1)))
    return dead

def main():
    failures = []
    for md_file in sorted(iter_markdown_files()):
        for line, target in check_file(md_file):
            failures.append(f"{md_file}:{line}: dead link -> {target}")
    if failures:
        print("Dead links found:\n")
        print("\n".join(failures))
        raise SystemExit(1)
    print("No dead links found.")

if __name__ == "__main__":
    main()

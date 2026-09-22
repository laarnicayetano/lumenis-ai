#!/usr/bin/env python3
"""
Reference implementation for Event Registration Reconciliation — step 3
(Deduplicate PEOPLE), see ../SKILL.md.

Union-find over normalized-name keys:
  1. Auto-union every record whose normalized name matches exactly.
  2. Union additional pairs from a manually-curated "corroborated merges"
     list — nickname/typo/transposition variants confirmed by a shared
     email or practice name (run find_candidates.py first to generate
     candidate pairs, then decide which ones are real merges).
  3. Everything else that merely shares an email or practice, but isn't a
     confirmed variant, is left UNMERGED and reported separately as
     "needs human confirmation" (counted as 2 distinct people, per
     SKILL.md).

Input: a CSV with one row per attendee (build this from the pulled Rep
Approval / Flight / Non-Flight sheets first — remember Rep Approval rows
hold TWO attendee slots each, see SKILL.md step 2):
  id,source_sheet,division,first_name,last_name,email,practice_name

Usage:
  python3 dedupe_people.py attendees.csv \
      --merges corroborated_merges.csv \
      --needs-confirmation needs_confirmation.csv

  corroborated_merges.csv / needs_confirmation.csv: two columns, id_a,id_b
  — pairs of attendee ids from attendees.csv, one pair per row.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict

TITLES = {"dr", "mr", "mrs", "ms", "mx"}
SUFFIXES = {"md", "od", "ii", "iii", "iv", "jr", "sr", "np", "pa", "rn", "do"}
LEGAL_SUFFIXES = {"llc", "llp", "pa", "pllc", "inc", "dba", "corp", "co"}


def normalize_name(first, last):
    def clean(token):
        return re.sub(r"[^a-z]", "", token.lower())

    parts = [clean(p) for p in re.split(r"[\s,]+", f"{first} {last}".strip()) if p]
    parts = [p for p in parts if p and p not in TITLES and p not in SUFFIXES]
    return " ".join(parts)


def normalize_practice(name):
    if not name:
        return ""
    tokens = re.split(r"[\s,]+", re.sub(r"[^\w\s&]", "", name.lower()))
    tokens = [t for t in tokens if t and t not in LEGAL_SUFFIXES]
    return " ".join(tokens)


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def load_pairs(path):
    pairs = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 2 or row[0].strip().lower() == "id_a":
                continue
            pairs.append((row[0].strip(), row[1].strip()))
    return pairs


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("attendees_csv")
    ap.add_argument(
        "--merges",
        help="CSV of id_a,id_b pairs to force-merge (corroborated near-matches)",
    )
    ap.add_argument(
        "--needs-confirmation",
        help="CSV of id_a,id_b pairs that share email/practice but are NOT "
        "confirmed merges — reported, never merged",
    )
    args = ap.parse_args()

    with open(args.attendees_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_id = {r["id"]: r for r in rows}

    for r in rows:
        blob = f"{r.get('first_name','')} {r.get('last_name','')} {r.get('practice_name','')}".lower()
        if "test" in blob:
            print(
                f"WARNING: row {r.get('id')} ({r.get('first_name')} {r.get('last_name')} / "
                f"{r.get('practice_name')}) looks like a test row — exclude it before "
                "dedup, per SKILL.md step 2.",
                file=sys.stderr,
            )
        r["_name_key"] = normalize_name(r.get("first_name", ""), r.get("last_name", ""))
        r["_practice_key"] = normalize_practice(r.get("practice_name", ""))

    uf = UnionFind()

    # Step 1: auto-union exact normalized-name matches.
    by_name_key = defaultdict(list)
    for r in rows:
        by_name_key[r["_name_key"]].append(r["id"])
    for ids in by_name_key.values():
        for other in ids[1:]:
            uf.union(ids[0], other)

    # Step 2: union manually-corroborated near-match pairs.
    if args.merges:
        for a, b in load_pairs(args.merges):
            if a not in by_id or b not in by_id:
                print(
                    f"WARNING: merge pair ({a}, {b}) references an id not in "
                    f"{args.attendees_csv} — skipped",
                    file=sys.stderr,
                )
                continue
            uf.union(a, b)

    # Step 3: needs-confirmation pairs are reported, never merged.
    needs_confirmation = load_pairs(args.needs_confirmation) if args.needs_confirmation else []

    clusters = defaultdict(list)
    for r in rows:
        clusters[uf.find(r["id"])].append(r)

    print(f"Unique people after dedup: {len(clusters)} (from {len(rows)} raw attendee rows)\n")
    for members in clusters.values():
        sheets = sorted({m["source_sheet"] for m in members})
        divisions = sorted({m["division"] for m in members if m.get("division")})
        display = members[0]
        note = f" | {len(members)} raw rows merged" if len(members) > 1 else ""
        print(
            f"- {display['first_name']} {display['last_name']} | "
            f"divisions: {', '.join(divisions) or '?'} | sheets: {', '.join(sheets)}{note}"
        )

    if needs_confirmation:
        print(
            f"\nNeeds human confirmation ({len(needs_confirmation)} pair(s), each counted "
            "as 2 people — see find_candidates.py):"
        )
        for a, b in needs_confirmation:
            ra, rb = by_id.get(a), by_id.get(b)
            if ra and rb:
                print(
                    f"  - {ra['first_name']} {ra['last_name']} ({ra['source_sheet']})  vs  "
                    f"{rb['first_name']} {rb['last_name']} ({rb['source_sheet']})"
                )

    print(
        "\nSanity check (SKILL.md step 5): total unique people above must not exceed "
        "rep_approved_people + registered_with_no_approval_people — verify against the "
        "Standard Output Shape derived lists before reporting."
    )


if __name__ == "__main__":
    main()

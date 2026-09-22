#!/usr/bin/env python3
"""
Reference implementation for the self-check scan in step 3 of Event
Registration Reconciliation (Deduplicate PEOPLE), see ../SKILL.md.

Scans every pair of DISTINCT normalized-name keys and flags any pair that
shares an email OR a normalized practice name — these are candidate
near-matches: either a nickname/typo/transposition variant of the same
person, or two real people who happen to share an office inbox or
practice. Run this BEFORE trusting dedup numbers, and again after any
merge to confirm nothing was missed.

Print output is intentionally UNTRUNCATED (see SKILL.md: "not just a
tail") — read the whole list, don't skim it.

Input: the same attendees CSV used by dedupe_people.py:
  id,source_sheet,division,first_name,last_name,email,practice_name

Usage:
  python3 find_candidates.py attendees.csv
  python3 find_candidates.py attendees.csv --name-similarity 0.85
"""
import argparse
import csv
from collections import defaultdict
from difflib import SequenceMatcher

# Kept identical to dedupe_people.py's normalization so candidates line up
# with what the merge step will actually key on.
import re

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


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("attendees_csv")
    ap.add_argument(
        "--name-similarity",
        type=float,
        default=0.0,
        help="Also flag pairs with normalized-name SequenceMatcher ratio >= this "
        "(0 disables; try ~0.8 to catch typos/transpositions with no shared "
        "email or practice)",
    )
    args = ap.parse_args()

    with open(args.attendees_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        r["_name_key"] = normalize_name(r.get("first_name", ""), r.get("last_name", ""))
        r["_practice_key"] = normalize_practice(r.get("practice_name", ""))
        r["_email"] = (r.get("email") or "").strip().lower()

    by_name_key = defaultdict(list)
    for r in rows:
        if r["_name_key"]:
            by_name_key[r["_name_key"]].append(r)
    distinct_keys = sorted(by_name_key)

    candidates = []
    for i, key_a in enumerate(distinct_keys):
        for key_b in distinct_keys[i + 1 :]:
            rows_a, rows_b = by_name_key[key_a], by_name_key[key_b]
            emails_a = {r["_email"] for r in rows_a if r["_email"]}
            emails_b = {r["_email"] for r in rows_b if r["_email"]}
            practices_a = {r["_practice_key"] for r in rows_a if r["_practice_key"]}
            practices_b = {r["_practice_key"] for r in rows_b if r["_practice_key"]}
            shared_email = emails_a & emails_b
            shared_practice = practices_a & practices_b

            reason = None
            if shared_email:
                reason = f"shared email ({', '.join(sorted(shared_email))})"
            elif shared_practice:
                reason = f"shared practice ({', '.join(sorted(shared_practice))})"
            elif args.name_similarity:
                ratio = SequenceMatcher(None, key_a, key_b).ratio()
                if ratio >= args.name_similarity:
                    reason = f"name similarity {ratio:.2f}"

            if reason:
                candidates.append((rows_a[0], rows_b[0], reason))

    print(
        f"{len(candidates)} candidate pair(s) found across {len(distinct_keys)} distinct "
        f"normalized names, {len(rows)} raw rows.\n"
    )
    print("Per SKILL.md step 3, for each pair below decide:")
    print(
        "  (a) a recognized nickname/typo/transposition variant of one person "
        "-> add to the corroborated-merge list for dedupe_people.py, or"
    )
    print(
        "  (b) genuinely different people who share an inbox/practice "
        "-> leave separate, add to the needs-confirmation list.\n"
    )

    if not candidates:
        print("(none — every shared email/practice belongs to a single normalized name)")
        return

    for ra, rb, reason in candidates:
        print(
            f"- \"{ra['first_name']} {ra['last_name']}\" ({ra['source_sheet']})  vs  "
            f"\"{rb['first_name']} {rb['last_name']}\" ({rb['source_sheet']})  —  {reason}"
        )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Aggregate an AOP Budget Detail sheet export into per-category FY26 totals.

Input: a JSON file in the shape returned by the Smartsheet MCP `get_sheet_summary`
tool (or produced by merge_sheet_pulls.py):
  {"availableColumns": [{"index": int, "title": str}, ...],
   "rows": [{"rowId": int, "cells": [{"columnIndex": int, "value": ...}, ...]}, ...]}

Required columns in the query that produced this file: Event, Category, Status, FY26.

Usage:
    python3 aop_budget_aggregate.py <path.json>

Prints one JSON object to stdout with per-category FY26 totals for Active rows,
the Active-rows grand total, and the excluded (non-Active) rows so you can
sanity-check the exclusion count.

--- Why this exists (read before reaching for get_sheet_aggregates instead) ---

Smartsheet's `get_sheet_aggregates` MCP tool cannot produce "sum of FY26 by
Category." Its `group_by` parameter only returns row COUNTS per group, and its
`summary_stats` parameter only returns overall (ungrouped) numeric stats --
median, mean, min, max, outliers -- for the whole filtered row set. Neither
combination yields a per-category dollar sum. The Budget Detail sheets are
small (well under 100 rows per division as of FY26), so the correct and
cheapest approach is to pull the full sheet with get_sheet_summary and sum
locally, which is what this script does.
"""
import json
import sys

ACTIVE_STATUS = "Active"


def load_rows(path):
    data = json.load(open(path))
    col_by_idx = {c["index"]: c["title"] for c in data["availableColumns"]}
    rows = []
    for r in data["rows"]:
        cells = {col_by_idx.get(c["columnIndex"], c["columnIndex"]): c.get("value") for c in r["cells"]}
        rows.append(cells)
    return rows


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: aop_budget_aggregate.py <path.json>", file=sys.stderr)
        sys.exit(1)

    rows = load_rows(sys.argv[1])

    by_category = {}
    excluded = []
    active_total = 0.0

    for r in rows:
        status = r.get("Status")
        if status != ACTIVE_STATUS:
            excluded.append({"event": r.get("Event"), "status": status})
            continue
        cat = r.get("Category") or "UNCATEGORIZED"
        fy26 = to_float(r.get("FY26")) or 0.0
        by_category.setdefault(cat, 0.0)
        by_category[cat] += fy26
        active_total += fy26

    result = {
        "total_rows_in_export": len(rows),
        "rows_excluded": excluded,
        "rows_used": len(rows) - len(excluded),
        "by_category": by_category,
        "active_total": active_total,
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

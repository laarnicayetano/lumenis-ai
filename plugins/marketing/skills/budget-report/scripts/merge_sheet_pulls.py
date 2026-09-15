#!/usr/bin/env python3
"""Merge multiple Smartsheet get_sheet_summary JSON pulls into one file.

Needed whenever a single sheet's query has to be split across several calls
to avoid silent sampling (e.g. VIS PR Tracking split by Quarter -- see the
budget-report SKILL.md Step 2 sampling note). Concatenates the `rows` arrays
so the result is shaped for reconcile_pr_data.py or aop_budget_aggregate.py.

Usage:
    python3 merge_sheet_pulls.py <out.json> <in1.json> <in2.json> [...]

No dedup is performed -- if two input queries' filters overlap, the same row
will appear twice in the output. Keep the split filters mutually exclusive
and collectively exhaustive across all input files (e.g. one call per
Quarter-IN group, plus a Quarter-IS_BLANK call for rows with no Quarter set).
"""
import json
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: merge_sheet_pulls.py <out.json> <in1.json> <in2.json> [...]", file=sys.stderr)
        sys.exit(1)

    out_path = sys.argv[1]
    in_paths = sys.argv[2:]

    available_columns = None
    merged_rows = []
    for p in in_paths:
        data = json.load(open(p))
        if available_columns is None:
            available_columns = data["availableColumns"]
        merged_rows.extend(data["rows"])

    merged = {
        "availableColumns": available_columns,
        "rows": merged_rows,
        "metadata": {"mergedFrom": in_paths, "totalRows": len(merged_rows)},
    }
    json.dump(merged, open(out_path, "w"))
    print(f"Merged {len(merged_rows)} rows from {len(in_paths)} files into {out_path}")


if __name__ == "__main__":
    main()

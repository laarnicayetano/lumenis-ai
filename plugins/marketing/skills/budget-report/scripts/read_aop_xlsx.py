#!/usr/bin/env python3
"""Parse the FY AOP budget workbook's category-detail sheets into structured JSON.

Usage:
    python3 read_aop_xlsx.py "<path to AOP xlsx>" "FY26 Detail by Q (Aesthetics)"
    python3 read_aop_xlsx.py "<path to AOP xlsx>" "FY26 Detail by Q (Vision)"

Prints one JSON object to stdout:
{
  "sheet": "...",
  "categories": {
     "Lumenis Workshops (VIS & AES Combined)": {"q1":..,"q2":..,"q3":..,"q4":..,"fy":..},
     ...
  },
  "grand_total": {"q1":..,...},
  "budget": {"q1":..,...},      # the buffer-inclusive AOP target -- this is "budget" per the skill
  "delta": {"q1":..,...}
}

How it works: these sheets aren't a clean table -- they're a human-built model with
category header rows ("Lumenis Workshops...  Q1 Q2 Q3 Q4 FY26"), a variable number of
line-item rows per category, and a "<DIVISION> TOTAL" row closing each section, ending
in "<DIVISION> GRAND TOTAL" / "BUDGET" / "Delta". This walks the sheet structurally
(find header rows by the literal Q1/Q2/Q3/Q4/FY26 labels, find each section's close by
the "TOTAL" marker in column B) rather than hardcoding row numbers, since row numbers
shift whenever a line item is added or removed. If the workbook's structure changes
beyond this pattern (per SKILL.md's own warning that this should be re-derived each
fiscal year), this script will print a warning rather than silently returning wrong
numbers -- check for "WARNING" lines in stderr before trusting the output.
"""
import json
import sys

from xlsx_lite import read_sheet_rows, cell, as_float


def parse_detail_sheet(path, sheet_name):
    rows = read_sheet_rows(path, sheet_name)
    max_row = max(rows.keys()) if rows else 0

    categories = {}
    grand_total = None
    budget = None
    delta = None

    row_num = 1
    while row_num <= max_row:
        row = rows.get(row_num, {})
        # category header row: column A has a label, and C..G literally read Q1,Q2,Q3,Q4,FY26
        header_vals = (row.get("C"), row.get("D"), row.get("E"), row.get("F"), row.get("G"))
        if row.get("A") and header_vals == ("Q1", "Q2", "Q3", "Q4", "FY26"):
            cat_name = row["A"]
            # scan forward for this category's "<...> TOTAL" close row
            scan = row_num + 1
            found_total = None
            while scan <= max_row and scan < row_num + 60:  # sane bound
                b_val = (rows.get(scan, {}).get("B") or "")
                if "TOTAL" in b_val.upper() and "GRAND" not in b_val.upper():
                    found_total = scan
                    break
                if "GRAND TOTAL" in b_val.upper():
                    break
                scan += 1
            if found_total:
                t = rows[found_total]
                categories[cat_name] = {
                    "q1": as_float(t.get("C")) or 0.0,
                    "q2": as_float(t.get("D")) or 0.0,
                    "q3": as_float(t.get("E")) or 0.0,
                    "q4": as_float(t.get("F")) or 0.0,
                    "fy": as_float(t.get("G")) or 0.0,
                    "total_row": found_total,
                }
                row_num = found_total + 1
                continue
            else:
                print(f"WARNING: category '{cat_name}' at row {row_num} has no TOTAL row found within 60 rows", file=sys.stderr)

        b_val = (row.get("B") or "")
        if "GRAND TOTAL" in b_val.upper():
            grand_total = {
                "q1": as_float(row.get("C")) or 0.0,
                "q2": as_float(row.get("D")) or 0.0,
                "q3": as_float(row.get("E")) or 0.0,
                "q4": as_float(row.get("F")) or 0.0,
                "fy": as_float(row.get("G")) or 0.0,
            }
            budget_row = rows.get(row_num + 1, {})
            delta_row = rows.get(row_num + 2, {})
            if (budget_row.get("B") or "").upper().strip() == "BUDGET":
                budget = {
                    "q1": as_float(budget_row.get("C")) or 0.0,
                    "q2": as_float(budget_row.get("D")) or 0.0,
                    "q3": as_float(budget_row.get("E")) or 0.0,
                    "q4": as_float(budget_row.get("F")) or 0.0,
                    "fy": as_float(budget_row.get("G")) or 0.0,
                }
            else:
                print(f"WARNING: expected 'BUDGET' row at {row_num + 1}, found '{budget_row.get('B')}'", file=sys.stderr)
            if (delta_row.get("B") or "").upper().strip() == "DELTA":
                delta = {
                    "q1": as_float(delta_row.get("C")) or 0.0,
                    "q2": as_float(delta_row.get("D")) or 0.0,
                    "q3": as_float(delta_row.get("E")) or 0.0,
                    "q4": as_float(delta_row.get("F")) or 0.0,
                    "fy": as_float(delta_row.get("G")) or 0.0,
                }
            break

        row_num += 1

    if grand_total is None:
        print("WARNING: no 'GRAND TOTAL' row found -- sheet structure may have changed", file=sys.stderr)
    if not categories:
        print("WARNING: no category sections found -- sheet structure may have changed", file=sys.stderr)

    return {
        "sheet": sheet_name,
        "categories": categories,
        "grand_total": grand_total,
        "budget": budget,
        "delta": delta,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: read_aop_xlsx.py <path.xlsx> <sheet name>", file=sys.stderr)
        sys.exit(1)
    result = parse_detail_sheet(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
"""Clean, reconcile, and aggregate a Smartsheet PR-tracking export for budget-report.

Input: a JSON file in the shape returned by the Smartsheet MCP `get_sheet_summary`
tool (or saved to disk by it when the result is too large to inline):
  {"availableColumns": [{"index": int, "title": str}, ...],
   "rows": [{"rowId": int, "cells": [{"columnIndex": int, "value": ...}, ...]}, ...],
   "metadata": {...}}

Required columns in the query that produced this file: PR#, Header Text, Quarter,
Category, Status, Valuation Price, PO#, PO SAP Balance, Date into SAP. (PO# is
required to correctly classify #NO MATCH rows -- see below. PR# and Date into
SAP are required for the no-PO-yet and oldest-open-PR lists.)

Usage:
    python3 reconcile_pr_data.py <path.json> [--current-fy-quarters Q126,Q226,Q326,Q426] [--oldest-n 10]

Prints one JSON object to stdout with cleaned/reconciled totals, a category
breakdown, a quarter breakdown, the POPR-unmatched count, the full list of
rows with no PO# yet (pending approval), and the N oldest still-open rows by
'Date into SAP' (candidates to close out). Required columns in the query
therefore also include PR# and Date into SAP -- see below.

--- Why this exists (read before changing the reconciliation logic) ---

`PO SAP Balance` is a Smartsheet formula column that looks up each PR's SAP-reported
balance from a shared "Open POPR" staging sheet, matched on `PO#`. It is the
REMAINING OPEN / UNPAID balance on the PO, not a cumulative "amount paid so far" --
confirmed by tracking the same PR's balance across multiple months (it shrinks
toward zero as invoices post; a PO already marked "Payment Issued, Process Complete"
can still show a nonzero balance if part of the requisitioned amount was never
invoiced -- the tracker's own Status option "Partial PO amount left over" exists for
exactly this case). So the amount actually spent on a PR, once its balance is known,
is `Valuation Price - PO SAP Balance`.

When `PO SAP Balance` is `#NO MATCH`, there are two structurally different reasons --
per the team that owns this feed (a contractor's explanation, confirmed accurate):
`Open POPR` is bumped up against a monthly PO/PR report pull (internally "Ismael's
tool") that **only pulls currently-open POs**. So:

  1. The row has no `PO#` yet (Status is still "PR Entered, Pending Approval" or
     "PR Approved, PO Creation Pending") -- there is nothing to look up yet. This is
     expected, not a discrepancy, and not a sign of anything wrong. These rows fall
     back to full Valuation Price as their spend contribution (same as
     pre-reconciliation behavior) -- correctly representing "committed, not yet
     confirmed paid," since nothing has been invoiced against a PR with no PO.

  2. The row HAS a `PO#`, but Open POPR has no matching row for it. **In most cases
     this means the PO has been 100% utilized and closed out in SAP** -- since Open
     POPR only tracks open POs, a fully-spent one naturally falls off the list. This
     is actually GOOD news, not a data gap: it means `Valuation Price` (the fallback
     used below) is very likely the correct, fully-realized spend figure for that
     row, not a rough approximation. The real exceptions, which this script cannot
     distinguish from the common case on its own, are: (a) a typo in the PO# on
     Smartsheet, or (b) Open POPR genuinely hasn't been refreshed to include a PO
     that's still open. Report this count as "unconfirmed by Open POPR (usually
     means fully closed)," not as "discrepancy" -- that word overstates the problem
     for what is, in most of these rows, an expected and correct outcome.
"""
import json
import re
import sys


DEFAULT_CURRENT_FY_QUARTERS = {"Q126", "Q226", "Q326", "Q426"}
CANCELLED_STATUS = "Cancelled (See Notes)"
PAID_STATUS = "Payment Issued, Process Complete"


def load_rows(path):
    data = json.load(open(path))
    col_by_idx = {c["index"]: c["title"] for c in data["availableColumns"]}
    rows = []
    for r in data["rows"]:
        cells = {col_by_idx.get(c["columnIndex"], c["columnIndex"]): c.get("value") for c in r["cells"]}
        cells["_rowId"] = r.get("rowId")
        rows.append(cells)
    return rows, data.get("metadata", {})


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def is_wrong_fy_header(header, current_fy_quarters):
    """Check free-text Header Text for a quarter tag (e.g. 'Q127A') from a
    different fiscal year than the current-FY quarters set."""
    if not header:
        return False
    current_years = {q[-2:] for q in current_fy_quarters}
    for m in re.finditer(r"Q\d(\d{2})", header):
        if m.group(1) not in current_years:
            return True
    return False


def clean_rows(rows, current_fy_quarters):
    kept, excluded = [], []
    for r in rows:
        reason = None
        if r.get("Status") == CANCELLED_STATUS:
            reason = "cancelled"
        elif r.get("Quarter") and r.get("Quarter") not in current_fy_quarters:
            reason = f"explicit wrong-FY quarter ({r.get('Quarter')})"
        elif not r.get("Quarter") and is_wrong_fy_header(r.get("Header Text"), current_fy_quarters):
            reason = "wrong-FY header tag on blank-Quarter row"

        if reason:
            excluded.append({"header": r.get("Header Text"), "reason": reason})
        else:
            kept.append(r)
    return kept, excluded


def reconcile(rows):
    """Returns (rows_with_computed_fields, negative_rows, no_po_count, po_unmatched_count)."""
    out = []
    negative_rows = []
    no_po_count = 0
    po_unmatched_count = 0

    for r in rows:
        val = to_float(r.get("Valuation Price")) or 0.0
        balance_raw = r.get("PO SAP Balance")
        balance = to_float(balance_raw)
        has_po = bool(r.get("PO#"))

        if balance is not None:
            row_spend = val - balance
            po_unmatched = False
        else:
            # Fallback: full face value. For has_po=True this is usually the
            # CORRECT figure (PO fully utilized, closed out in SAP, fell off
            # Open POPR's open-only feed) -- not a rough guess. See module
            # docstring. For has_po=False, this is the "committed, not yet
            # paid" face value, same as pre-reconciliation behavior.
            row_spend = val
            if has_po:
                po_unmatched_count += 1
                po_unmatched = True
            else:
                no_po_count += 1
                po_unmatched = False

        if row_spend < 0:
            negative_rows.append({
                "header": r.get("Header Text"),
                "valuation": val,
                "po_sap_balance": balance_raw,
                "reconciled_spend": row_spend,
            })

        rr = dict(r)
        rr["_reconciled_spend"] = row_spend
        rr["_has_po"] = has_po
        rr["_po_unmatched_in_open_popr"] = po_unmatched
        out.append(rr)

    return out, negative_rows, no_po_count, po_unmatched_count


def build_pr_lists(rows, oldest_n=10):
    """From the cleaned+reconciled rows, pull:
      - every row with no PO# yet (needs approval before anything can move)
      - the N oldest still-open rows by 'Date into SAP' (candidates to close out)

    'Open' here means Status is not Paid and not Cancelled (cancelled rows are
    already excluded upstream by clean_rows, but the check is kept for safety).
    Rows missing a 'Date into SAP' value are sorted to the end (can't rank an
    age we don't have) and are not silently dropped.
    """
    no_po = []
    open_rows = []
    for r in rows:
        if not r.get("PO#"):
            no_po.append({
                "pr_number": r.get("PR#"),
                "date_into_sap": r.get("Date into SAP"),
                "header": r.get("Header Text"),
                "category": r.get("Category"),
                "quarter": r.get("Quarter"),
                "status": r.get("Status"),
                "valuation_price": r.get("Valuation Price"),
            })
        if r.get("Status") not in (PAID_STATUS, CANCELLED_STATUS):
            open_rows.append(r)

    def date_key(r):
        d = r.get("Date into SAP")
        return (d is None or d == "", d or "")

    open_rows_sorted = sorted(open_rows, key=date_key)
    oldest = [{
        "pr_number": r.get("PR#"),
        "header": r.get("Header Text"),
        "status": r.get("Status"),
        "date_into_sap": r.get("Date into SAP"),
        "po_number": r.get("PO#"),
        "valuation_price": r.get("Valuation Price"),
    } for r in open_rows_sorted[:oldest_n]]

    return no_po, oldest, len(open_rows)


def aggregate(rows):
    by_category = {}
    by_quarter = {}
    paid_total = 0.0
    committed_total = 0.0
    face_value_total = 0.0

    for r in rows:
        cat = r.get("Category") or "UNCATEGORIZED"
        q = r.get("Quarter") or "BLANK"
        val = to_float(r.get("Valuation Price")) or 0.0
        spend = r["_reconciled_spend"]

        face_value_total += val
        by_category.setdefault(cat, {"face_value": 0.0, "reconciled": 0.0, "rows": 0, "po_unmatched_in_open_popr": 0})
        by_category[cat]["face_value"] += val
        by_category[cat]["reconciled"] += spend
        by_category[cat]["rows"] += 1
        if r["_po_unmatched_in_open_popr"]:
            by_category[cat]["po_unmatched_in_open_popr"] += 1

        by_quarter.setdefault(q, 0.0)
        by_quarter[q] += spend

        if r.get("Status") == PAID_STATUS:
            paid_total += spend
        else:
            committed_total += spend

    return {
        "by_category": by_category,
        "by_quarter": by_quarter,
        "paid_total": paid_total,
        "committed_total": committed_total,
        "reconciled_total": paid_total + committed_total,
        "face_value_total": face_value_total,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: reconcile_pr_data.py <path.json> [--current-fy-quarters Q126,Q226,Q326,Q426]", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    current_fy_quarters = DEFAULT_CURRENT_FY_QUARTERS
    oldest_n = 10
    for i, arg in enumerate(sys.argv):
        if arg == "--current-fy-quarters" and i + 1 < len(sys.argv):
            current_fy_quarters = set(sys.argv[i + 1].split(","))
        if arg == "--oldest-n" and i + 1 < len(sys.argv):
            oldest_n = int(sys.argv[i + 1])

    raw_rows, metadata = load_rows(path)
    clean, excluded = clean_rows(raw_rows, current_fy_quarters)
    reconciled_rows, negative_rows, no_po_count, po_unmatched_count = reconcile(clean)
    agg = aggregate(reconciled_rows)
    no_po_list, oldest_open_prs, open_pr_count = build_pr_lists(reconciled_rows, oldest_n)

    result = {
        "source_metadata": metadata,
        "total_rows_in_export": len(raw_rows),
        "rows_excluded": excluded,
        "rows_used": len(clean),
        "rows_with_no_po_yet": no_po_count,
        "rows_with_po_unmatched_in_open_popr": po_unmatched_count,
        "note": (
            f"{po_unmatched_count} rows have a PO# but no Open POPR match. Open POPR "
            "only tracks currently-open POs, so in most cases this means the PO is "
            "100% utilized and closed out in SAP -- not a data gap, and the full "
            "Valuation Price fallback used for these rows is likely correct as-is. "
            "The real exceptions (can't be told apart automatically): a PO# typo in "
            "Smartsheet, or Open POPR genuinely not yet updated for a still-open PO. "
            f"{no_po_count} more rows have no PO# yet (expected -- still pending "
            "approval, nothing to look up)."
        ),
        "face_value_total": agg["face_value_total"],
        "reconciled_total": agg["reconciled_total"],
        "reconciled_paid": agg["paid_total"],
        "reconciled_committed": agg["committed_total"],
        "by_category": agg["by_category"],
        "by_quarter": agg["by_quarter"],
        "negative_reconciled_rows": negative_rows,
        "open_pr_count": open_pr_count,
        "rows_without_po": no_po_list,
        "oldest_open_prs": oldest_open_prs,
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

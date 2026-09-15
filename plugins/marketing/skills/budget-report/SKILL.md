---
name: budget-report
description: Report remaining marketing budget and run rate for Lumenis Aesthetics (AES) and Vision (VIS), reconciling Smartsheet PR tracking data against the FY Annual Operating Plan (AOP). Use when the user asks "how much budget do we have left," wants a budget-vs-actual report, a burn rate / run rate check, or a remaining-runway report for AES and/or VIS marketing spend.
---

# Manage Budget — AES & VIS

Produces a remaining-budget and run-rate report for Aesthetics (AES) and Vision (VIS) marketing, by reconciling live PR data in Smartsheet against the division's AOP (Annual Operating Plan) budget. Built from a real reconciliation session where several data-quality issues silently distorted the numbers by hundreds of thousands of dollars — the steps below exist specifically to catch those, not as generic best practice.

## Inputs needed

1. **Smartsheet connection (MCP)**, workspace **"2026 - PR Entry Tracking"**. Known sheet IDs (current as of FY26 — hardcoded here to skip the search/discovery step on every run; re-verify with `search` / `list_workspaces` / `browse_workspace` if any of these stop resolving, most likely when a new fiscal year's sheets get created, e.g. "2027 - AES PR Tracking"):
   - `2026 - AES PR Tracking` — sheet ID `605402086461316`
   - `2026 - VIS PR Tracking` — sheet ID `585086740156292`
   - `2026 - HOS PR Tracking` — sheet ID `4838202960465796` (include only if asked)
   - `Open POPR` — sheet ID `2555837718417284` — shared raw SAP staging sheet, not division-specific; see Step 3 for how it's used
2. **AOP budget sheets (Smartsheet, MCP)** — the AOP now lives on Smartsheet, not in a local Excel file. **Current location is the `Test` workspace, not `2026 - PR Entry Tracking`** — these were built there because the account only has Editor (not Admin) access to `2026 - PR Entry Tracking`, which blocks sheet creation. If someone moves them (or grants Admin access there and they get migrated), re-resolve the IDs via `search`/`browse_workspace` and update this file rather than assuming these IDs still work.
   - `Aesthetics` — sheet ID `645062850727812`
   - `Vision` — sheet ID `3747094390329220`
   - `Hospital` — sheet ID `6567796713672580` (include only if asked)
   - `Targets` — sheet ID `2064197086302084` — one row per division, with the buffer-inclusive **`Mktg Target ($)`** column — this is **the number the user means by "budget"** (AES `3,014,000` / VIS `2,687,000` / Hospital `232,000` as of FY26; re-read the sheet rather than trusting these hardcoded values once a new fiscal year's Targets sheet exists). Also carries `Bookings ($M)`, `Revenue ($M)`, and `Projected FY25 Spend ($)` for context.
   - Each `... Budget Detail` sheet is line-item grain (one row per event/vendor, same idea as the PR trackers): `Category` (picklist — division's own AOP categories, e.g. Workshops/Webinars/Industry Initiatives/Tradeshows/Digital/Outsourced Services — AES has Digital, VIS/Hospital don't), `Line Item / Event`, `Status` (Active/Cancelled), `Q1–Q4 Budget`, `FY26 Budget` (formula column, always trust this over hand-summing), `KOL Fees`, `# of KOLs`, `Shared Event Group` (tags the AES row and VIS row of a split cross-division event, e.g. an Accelerate), `Reported Actual (AOP-era)` (a stale manually-entered actual from the old workbook, historical reference only — never use this as a stand-in for Step 3's reconciled actual), and `Notes`.

## Scripts (use this — don't re-derive PR reconciliation logic inline)

This skill's folder has one script (stdlib-only Python, no API-credential dependency, and no MCP access — the Smartsheet queries in Steps 1-2 still have to happen through the live MCP tools first):

- **`scripts/reconcile_pr_data.py <saved get_sheet_summary JSON> [--oldest-n 10]`** — takes the JSON that Smartsheet's `get_sheet_summary` returns (or saves to disk when the result is too large to inline) and applies Step 2's cleaning + Step 3's reconciliation + category/quarter aggregation. **The query that produces this input must include `PR#`, `PO#`, and `Date into SAP`**, not just `PO SAP Balance` — `PO#` lets the script correctly separate rows Open POPR simply hasn't matched (usually because the PO is fully closed out — see Step 3) from rows that don't have a PO# yet at all, and `PR#`/`Date into SAP` feed the two PR lists in Steps 7-8. Outputs reconciled totals, a category breakdown, a quarter breakdown, both counts (`rows_with_no_po_yet`, `rows_with_po_unmatched_in_open_popr`), any negative-reconciled-spend rows (a data-quality flag, not something the script can resolve on its own), the full `rows_without_po` list (Step 7), and the `oldest_open_prs` list (Step 8, 10 by default — pass `--oldest-n` for a longer list). **A single `get_sheet_summary` call against a Budget Detail sheet may get silently sampled if the row count is high and many columns are selected** (seen firsthand building these sheets — VIS PR Tracking's 228 rows got truncated to 200 once extra columns were added) — check the response's `metadata.isSampled`/`rowsActual` vs `rowsInFilter` before trusting a pull, and split the query (e.g. by `Quarter`, using the `IN` filter operator) if it's sampled.

The Budget Detail sheets is tabular Smartsheet data, so Step 4's category totals come directly from `get_sheet_aggregates` (`group_by: Category`, summed `FY26 Budget`, filtered to `Status = Active`) rather than a parsing step. Run one `reconcile_pr_data.py` call per division (filtered to that division's Marketing cost center from Step 1). Feed its output, plus the AOP aggregates, into Steps 4-6 below rather than re-deriving the cleaning/reconciliation math from the prose description each time.

## Step 1 — Identify each division's cost center(s)

Don't hardcode cost center numbers — they change. In each PR tracking sheet, pull the `PGR/Cost Center` column's picklist options (`get_columns`) and find the entry whose label matches the division's Marketing team (e.g. "... US Aesthetics Marketing ... - Marketing" / "... US Vision Marketing ... - Marketing"). Extract its numeric cost center ID (there's usually a separate `Cost Center` formula column that parses it out of the picklist label) and filter on that. A single sheet can contain many cost centers (regional sales teams, other departments) — the budget report should only cover the Marketing cost center(s) unless the user explicitly asks for something broader.

## Step 2 — Pull raw PR data, clean it, and map categories to the AOP

Pull each division's rows with `get_sheet_summary`, filtered to that division's Marketing cost center (Step 1), selecting at minimum: `PR#, Header Text, Quarter, Category, Status, Valuation Price, PO#, PO SAP Balance, Date into SAP`. (`PR#` and `Date into SAP` are needed for Steps 7-8's PR lists, not just the reconciliation math.) Save the result and run it through `scripts/reconcile_pr_data.py` (see "Scripts" above) — it applies cleaning steps 1-2 below itself (cancelled-status filter, wrong-FY-quarter filter including the blank-Quarter/Header-Text check) and reports exactly what it excluded and why in its `rows_excluded` output. **Do not skip feeding data through this script and re-doing the cleaning by hand or in prose** — in the source session, skipping equivalent steps overstated one division's spend by ~$570K and understated the other's headroom by a comparable amount. The two things the script does NOT do for you:

1. Cancelled-status and wrong-fiscal-year exclusion — handled automatically; just check its `rows_excluded` list matches your expectations (e.g. no more than a handful of rows, all with an understandable reason).
2. **Reconcile the PR tracker's `Category` picklist against the AOP Budget Detail sheet's `Category` picklist — they are two different taxonomies and do not mirror each other.** The PR tracker uses ~14 fine-grained values (Workshops, Trade Show Expenses, Luminaries, Other Outside Svcs, Digital/Online Mktng, Consulting Svcs, Sales Training/Materials, Direct Mail Advertising, Literature & Brochure(s), Meetings, etc.); the AOP Budget Detail sheet uses the division's own 5-6 top-level categories (Workshops, Webinars, Industry Initiatives, Tradeshows, Digital [AES only], Outsourced Services). Re-derive this mapping from the current AOP's line-item notes each time; as a starting point, this was the confirmed mapping as of FY26:
   - `WORKSHOPS` (PR) → `Workshops` (AOP) — the Accelerate / Users-Meeting events, including their per-division `KOL Fees` column
   - `TRADE SHOW EXPENSES` (PR) → `Tradeshows` (AOP) — compare event-by-event, since the AOP names each show individually
   - `DIGITAL/ONLINE MKTNG` (PR) → `Digital` (AOP, AES only — VIS/Hospital have no Digital category)
   - `OTHER OUTSIDE SVCS` + `CONSULTING SVCS` + `SALES TRAINING/MATERIALS` + `DIRECT MAIL ADVERTISING` + `LITERATURE & BROCHURE(S)` + `MEETINGS` (PR) → collectively `Outsourced Services` (AOP)
   - `LUMINARIES` (PR) → **no single clean match.** Individual doctor/KOL honorariums in the PR tracker are smeared across several AOP categories depending on context: some fold into a Workshop event's `KOL Fees` column, some are their own `Webinars` line items, some sit under `Industry Initiatives`, and some are embedded inside a `Tradeshows` line's honorarium-inclusive total (the AOP's Tradeshow category headers are literally named "... (honorariums embedded in TC)"). Don't force `LUMINARIES` into one AOP bucket — treat it as split/unmapped and say so in the response rather than silently misattributing it to whichever category is closest.
     Getting a category mapping wrong doesn't change the division's total, but it will misattribute _which line item_ is over or under — verify against the AOP's own notes/labels rather than reusing this list blindly.

## Step 3 — Compute "Actual" per division, reconciled against Open POPR

Each PR tracking sheet carries a `PO SAP Balance` formula column — a live lookup against the `Open POPR` staging sheet (see "Inputs needed" above), matched on `PO#`. **Critical, non-obvious fact about this field, confirmed by the contractor who owns the feed it's built from:** `Open POPR` is bumped up against a monthly PO/PR report pull that **only pulls currently-open POs**. So `PO SAP Balance` is the _remaining open/unpaid_ balance on the PO, not a cumulative "amount paid so far" — it shrinks toward zero as invoices post, and once a PO hits 100% utilization it drops off the feed entirely rather than showing a zero balance. A PO already marked "Payment Issued, Process Complete" on the tracker can still show a nonzero balance if part of the requisitioned amount was never invoiced — the tracker's own Status option "Partial PO amount left over (see notes)" exists for exactly this case.

`scripts/reconcile_pr_data.py` computes this per row and aggregates it for you (see "Scripts" above) — this section documents what it does and why, so you can sanity-check its output rather than re-deriving it:

- **If `PO SAP Balance` resolves** (i.e. is not `#NO MATCH`): reconciled spend = `Valuation Price − PO SAP Balance`. This is the correct field to use — it reflects real posted SAP activity, not just what's recorded in the tracker's Status dropdown.
- **If `PO SAP Balance` is `#NO MATCH`**: fall back to using the full `Valuation Price` as that row's spend contribution.

**`#NO MATCH` splits into two structurally different cases — do not conflate them into one "discrepancy" count, and do not call the second one a discrepancy by default:**

- **No `PO#` yet** (Status is still "PR Entered, Pending Approval" or "PR Approved, PO Creation Pending"): there's nothing to look up — expected, not a data gap. The full-Valuation-Price fallback correctly represents "committed, not yet paid" here. The script tracks this count separately as `rows_with_no_po_yet`.
- **Has a `PO#`, but Open POPR has no matching row for it**: per the contractor, **in most cases this means the PO is 100% utilized and closed out in SAP** — a fully-spent PO naturally falls off an open-POs-only feed. This is good news, not a gap: the full-Valuation-Price fallback is very likely the _correct_, fully-realized spend figure here, not a rough approximation. The real exceptions — which cannot be told apart from the common case automatically — are (a) a typo in the PO# on Smartsheet, or (b) Open POPR genuinely hasn't been refreshed to include a PO that's still open. The script reports this count as `rows_with_po_unmatched_in_open_popr`. **Mention this count in every response this skill produces** — `template.md` has no dedicated row for it, so surface it in the closing note (`{{CLOSING_NOTE}}`), framed as "rows relying on the fully-closed-PO assumption," not as "discrepancies" or "errors" — most of them aren't.

Report actual spend split into:

- **Paid** — Status = "Payment Issued, Process Complete" (or equivalent). Cash that has actually left the building — but still apply the reconciliation above; a "Paid" row's true spend can be less than face value.
- **Committed, not yet paid** — PO Created/Pending Invoice, PR Entered/Pending Approval, Invoice Received/Sent to AP, etc. Money that's spoken for but not yet disbursed.

Also check the script's `negative_reconciled_rows` output — a row where `PO SAP Balance` exceeds `Valuation Price` (reconciled spend goes negative) means Open POPR and the tracker's own recorded requisition amount disagree. The script can't resolve this; flag it in the response as a data-quality item worth someone checking directly, and exclude it from category totals if it's large enough to distort the section.

## Step 4 — Remaining budget

`Remaining budget = AOP target (full-year, the "Mktg Target ($)" column on the FY26 AOP - Targets sheet — the buffer-inclusive figure) − Actual (cleaned per Step 2, Paid + Committed)`

Pull the category-level AOP budget with `get_sheet_aggregates` against the division's `... Budget Detail` sheet: `group_by: Category`, summed `FY26 Budget`, filtered to `Status = Active` (Cancelled rows are $0 by construction, but filter them out anyway rather than relying on that).

Report the remaining-budget figure for both AES and VIS side by side, plus:

- A category-level table (AOP category budget vs. cleaned actual vs. variance $/%) so the user can see _which_ line items drive any variance — a division can look on-budget in aggregate while one category runs wildly over and another masks it by running under. **Only include rows where both sides of the mapping exist** — if a PR tracker `Category` has no corresponding AOP category for that division (e.g. VIS has no `Digital` AOP category), leave it out of the table entirely rather than including it with a blank/flagged cell. `LUMINARIES` (PR) has no single AOP counterpart at all (see Step 2) — omit it from this table rather than guessing which bucket it belongs in.
- A flag on any category variance beyond ~15-20% in either direction. A large _under_-spend on a big-ticket line (Tradeshows, Workshops) late in the year is often unbilled/uncommitted spend still coming, not free money — don't report it as pure headroom without checking Step 3's paid/committed split for that category.

## Step 5 — Run rate (on request only)

`template.md`'s default output has no row for run rate — don't compute or report it unless the user specifically asks for a pace/run-rate/burn-rate check. When they do, report it in prose appended after the template's tables (don't try to force it into the template's row set), two ways — they answer different questions:

1. **Actual pace vs. budgeted pace.** The AOP's quarterly split usually isn't flat — pull the real quarterly budget numbers (sum `Q1 Budget`...`Q4 Budget` across Active rows on the division's `... Budget Detail` sheet, via `get_sheet_aggregates`) rather than assuming budget ÷ 4. Compare cleaned actual spend in completed quarters to the budgeted amount for those same quarters, then extrapolate a full-year projection at the current pace and flag whether that trajectory lands over or under the AOP target.
2. **Committed run rate (forward-looking).** Of the remaining budget, how much is already committed — PO'd/PR'd for a future quarter (e.g. Q4 events already entered but unpaid) — versus genuinely uncommitted. This tells the user how much _real_ discretionary room is left; a division can show large "remaining budget" that's almost entirely already spoken for by open POs. **Note:** `reconcile_pr_data.py`'s `by_quarter` breakdown sums total spend per quarter but doesn't cross it with Paid/Committed status, and the script has no concept of "current quarter" — computing this split requires pulling Quarter+Status per row directly and reasoning about which quarters have elapsed yourself.

## Step 6 — Output format

Follow `template.md` in this skill's folder exactly for structure and row set — it covers the summary table, category breakdown, and the Step 7/8 PR-list tables below. Fill in its `{{PLACEHOLDER}}` fields, don't add or remove rows/sections on your own judgment. If the template needs a structural change (a new row, a renamed section), edit `template.md` itself first and treat that as a deliberate skill change, not a per-run formatting choice.

**Don't add a prose narrative (biggest variance drivers, etc.) unless the user asks for one.** The template's tables + the two lists in Steps 7-8 are the default output — keep the response scannable rather than re-explaining the tables in paragraph form.

## Step 7 — Rows with no PO# yet (pending approval)

List every row in `rows_without_po` (per division) — these PRs haven't been assigned a PO# yet, meaning they're still stuck somewhere before/at approval (Status will be "PR Entered, Pending Approval" or similar). This is a follow-up/action list, not a budget metric: these are the PRs someone needs to push through approval.

Report as a table per division: PR#, Date into SAP, Header Text, Category, Quarter, Status, Valuation Price. Don't cap the list — report all of them (this is typically a short list; Step 6's "no PO yet" count tells the user the size in advance).

## Step 8 — Oldest open PRs

List the `oldest_open_prs` from the script's output (per division) — the PRs that have been sitting the longest (by `Date into SAP`) without reaching "Payment Issued, Process Complete" or "Cancelled." These are candidates for someone to close out, chase down, or cancel if they're stale.

Report as a table per division: PR#, Date into SAP, Header Text, Status, PO#, Valuation Price. Default to 10 per division (the script's default `--oldest-n`); mention the total `open_pr_count` so the user knows how many more exist, and offer a longer list if they want one (re-run with `--oldest-n <N>`).

## Notes for future runs

- A follow-up drill-down (e.g. "how much did we spend across all Accelerate events this year," "break down [vendor/category] spend") should reuse the Step 1-2 cleaned dataset, not recompute from raw/uncleaned totals.
- Re-verify the cost center IDs (Step 1) and the category-to-AOP-category mapping (Step 2.2) every time this runs in a new fiscal year — both are known to change when the AOP is rebuilt.
- If the AOP Budget Detail sheets' structure has changed (new categories, renamed columns), re-derive Steps 2 and 4 from the current sheets rather than forcing this year's data into last year's shape.
- The hardcoded workspace/sheet IDs in "Inputs needed" are FY26-specific. When they stop resolving (most likely at a new fiscal year, or when the AOP sheets get moved into `2026 - PR Entry Tracking` once Admin access is sorted out), re-discover the new sheets via `search`/`browse_workspace` and update this file with the new IDs rather than searching fresh on every single run.
- The `Shared Event Group` column on the AOP Budget Detail sheets ties a split cross-division event's AES row to its VIS row (e.g. an Accelerate is 60/40 AES/VIS) — each division's sheet already carries only its own share, so summing a division's `FY26` column never double-counts a split event. Only use `Shared Event Group` if asked to reconstruct a split event's full combined cost.
- `Reported Actual (AOP-era)` on the Budget Detail sheets is a stale manually-entered figure carried over from the old AOP workbook (populated for a handful of AES Tradeshow rows only) — it predates this skill's reconciliation approach and should never substitute for Step 3's live reconciled actual.
- `Open POPR` is refreshed manually/periodically by someone outside this skill, not on a fixed schedule — its coverage of the current PR set can vary run to run. Don't assume a low `#NO MATCH` count this run means it'll stay low next time.
- If a row's actual spend genuinely needs confirming beyond what `rows_with_po_unmatched_in_open_popr` can tell you (e.g. the user is disputing a specific PR), the two real exceptions to check by hand are a PO# typo on that Smartsheet row, or asking whoever runs the monthly Open POPR refresh whether that specific PO was still open as of the last pull.

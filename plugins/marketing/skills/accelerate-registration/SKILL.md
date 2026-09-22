---
name: accelerate-registration
description: Reconcile the accelerate event registration/approval data from Smartsheet (Rep Approval + Flight/Non-Flight Registration sheets), dedupe people and accounts across sheets, and report headcounts, follow-up lists, and pipeline. Use for any Accelerate-style event registration report.
---

# Event Registration Reconciliation

Use this whenever asked to pull, analyze, or report on registration numbers for an Accelerate event. Every 2026 event lives in the **2026 Accelerate** workspace as one folder per event, and every folder follows the exact same 4-sheet structure: `AES Rep Approval - <Event>`, `VIS Rep Approval - <Event>`, `<City> Flight Registration (AES+VIS)`, `<City> Non-Flight Registration (AES+VIS)`. Rep Approval is two separate sheets (one per division); Flight and Non-Flight Registration are each a single sheet covering both divisions, split by a `Division` picklist column.

## 0. Known workspace (hardcoded — start here, not with a global search)

- **2026 Accelerate workspace ID: `1905963444791172`** (`https://app.smartsheet.com/workspaces/3Vv3MjVH2V57MHvjX3fhhR7VMR6pHMfxGC4JGmH1`). Go straight to `browse_workspace` with this ID (if the event is in 2026) rather than a bare `search` — a name-only search can also surface two unrelated, confusingly similar places:
  - **`Accelerate Flight Bookings 2025`** workspace (ID `8357172296869764`) — last year's series, wrong year.
  - **`2026 Accelerates`** folder (ID `4945363883845508`) inside the separate **`Vision Marketing Events`** workspace (ID `721669699463044`) — a differently-structured, Vision-only holding area, not this event series.

  If a sheet ID ever comes back from one of those two, stop and confirm the event/year with the user before using it — don't silently reconcile against the wrong workspace.

- **Folder naming isn't fully consistent — don't rely on the word "Accelerate" alone.** `Q3 Chicago Owners Meeting` is itself an Accelerate event (same 4-sheet structure as every other folder) but wasn't named like one. Treat any folder in this workspace containing the `AES Rep Approval` / `VIS Rep Approval` / `Flight Registration` / `Non-Flight Registration` sheet pattern as reconcilable, regardless of what the folder itself is called.

- **Folders present as of this writing** (new quarters get their own new folder over time — treat this as a shortcut for these events, not a ceiling; if the named event isn't here, `browse_workspace` again to pick up folders added since):

  | Folder                    | Folder ID          |
  | ------------------------- | ------------------ |
  | Q1 Orlando Accelerate     | `1423262832977796` |
  | Q2 NYC Accelerate         | `949683364358020`  |
  | Q2 SoCal Accelerate       | `8647089392510852` |
  | Q3 Accelerate Nashville   | `7034853393753988` |
  | Q3 Chicago Owners Meeting | `6172836277577604` |
  | Q4 Miami Accelerate       | `204160760080260`  |
  | Q4 Scottsdale Accelerate  | `432859178657668`  |

## 1. Locate and pull live

- If the event's folder ID is already known (see the table above), skip straight to `browse_folder(folder_id=...)`. Otherwise `browse_workspace(workspace_id=1905963444791172, asset_types=["folders"])` first to find it — folder names are frequently near-duplicates across quarters/cities, so confirm you have the right one before pulling.
- `browse_folder`'s response already returns each sheet's `modifiedAt` alongside its ID and name — capture it per sheet now. That's the "sheet last updated" timestamp for the report (see **Standard output shape**); there's no need for a separate `get_sheet_version` call just to get it.
- Always re-pull **all** the event's sheets live before answering, not just the ones that seem relevant to the question — these change multiple times a day. Report both the pull timestamp (via `mcp__claude_ai__current_time`) and each sheet's `modifiedAt` in the final output, so a stale sheet is visible before anyone reads a headcount off it.
- Call `get_columns` first on each sheet to get exact column names before filtering/selecting.

## 2. Attendee counting

- Rep Approval sheets hold TWO attendees per row (Attendee #1 and #2 First/Last/Email columns). Count FILLED ATTENDEE SLOTS, not rows — if people-count equals row-count on an approval sheet, attendee #2 has been missed.
- Exclude test rows (name or company containing "test").
- Registration sheets (Flight / Non-Flight) are one attendee per row.

## 3. Deduplicate PEOPLE — by normalized name, not email

Practices frequently share one office inbox across multiple staff (e.g. one practice email covers 3-4 different attendees), so **never dedupe on email**. Instead:

1. Normalize: lowercase, strip punctuation, strip titles (Dr., Mr., Mrs., Ms.) and suffixes (MD, OD, II, III, IV, Jr, Sr).
2. Auto-merge exact normalized-name matches.
3. Merge near-matches (nickname variants like Connie/Constance, Katie/Katherine, Richard/Richards; spelling typos; letter transpositions) ONLY when corroborated by a shared email OR shared normalized practice name. Never merge on shared inbox alone — two different first names sharing an email are usually two real people.
4. Cases that share email/practice but have genuinely different names (not a recognized nickname/typo variant) go to a "needs human confirmation" list — leave them as 2 separate people, don't auto-merge.
5. Dedupe ACROSS all sheets (both approval sheets + both registration sheets), not just within each sheet — **this is the step that gets skipped most often.** Someone who is rep-approved and then registers for a flight is one person, not two. Apply it symmetrically to both divisions — don't cross-sheet dedupe Vision and forget to do the same for Aesthetics (or vice versa).

Implement with a union-find over normalized-name keys; [scripts/dedupe_people.py](scripts/dedupe_people.py) is a runnable reference implementation (exact-key auto-union, then a manual corroborated-merge list, then a manual needs-confirmation list). Build a CSV of one row per attendee (`id,source_sheet,division,first_name,last_name,email,practice_name` — remember Rep Approval rows hold two attendee slots each, per step 2) from the pulled sheets, then run it: `python3 scripts/dedupe_people.py attendees.csv --merges merges.csv --needs-confirmation needs_confirmation.csv`.

**Self-check before delivering numbers**: scan for a person appearing in two mutually exclusive derived buckets (e.g. "approved not registered" AND "registered no approval") — that contradiction almost always means a missed near-match merge. Re-run the full candidate scan with [scripts/find_candidates.py](scripts/find_candidates.py) (`python3 scripts/find_candidates.py attendees.csv`, same input CSV as above) — it flags every pair of distinct normalized names sharing an email or practice — and read its UNTRUNCATED output before trusting the numbers, not just a `tail`. Its output pairs are exactly the `merges.csv` / `needs_confirmation.csv` candidates for `dedupe_people.py` above, once you've decided which are real.

## 4. Deduplicate ACCOUNTS

Normalize practice/account names separately: lowercase, strip punctuation, strip legal suffixes (LLC, LLP, PA, PLLC, Inc, DBA). Do not fuzzy-merge spelling variants into the core account-count methodology — keep that rule simple and consistent so every accounts figure in the report uses the same definition. If a narrower question needs stricter merging (e.g. "how many accounts have pipeline data", where the same rep entering "Purele Waxing" three different ways inflates the count), do that merge in a clearly-labeled scoped sub-analysis and say explicitly that it's a different (stricter) rule than the headline accounts number — don't silently change the main figure.

## 5. Sanity check

Total unique people (all sheets) must never exceed:
`rep_approved_people + registered_with_no_approval_people`
If this identity breaks, redo the cross-sheet dedup — something was double-counted or under-merged.

## 6. Standard output shape

**Header block**: before the summary table, list the pull timestamp and a small Sheet | Last Updated table (one row per sheet, from each sheet's `modifiedAt` captured in step 1) — so anyone reading the report can see at a glance whether a given sheet had fresh data at pull time.

**Summary tables — two separate tables, one per division, not one combined table.** Each is Sheet | Accounts | People, with a TOTAL row deduplicated (not summed) across that division's three sheets — explicitly note the total will be lower than the naive sum and explain why (dedup, not double-counting). Default row order/shape, unless the user asks for something else:

**Vision**

| Sheet                   | Accounts | People |
| ----------------------- | -------- | ------ |
| VIS Rep Approval        |          |        |
| Flight Registration     |          |        |
| Non-Flight Registration |          |        |
| **TOTAL**               |          |        |

**Aesthetics**

| Sheet                   | Accounts | People |
| ----------------------- | -------- | ------ |
| AES Rep Approval        |          |        |
| Flight Registration     |          |        |
| Non-Flight Registration |          |        |
| **TOTAL**               |          |        |

The Flight/Non-Flight Registration rows in each table are a `Division`-filtered cut of that one combined sheet, not a separate sheet per division.

Below both tables, state explicitly: the **combined total unique people across both divisions** (this will be lower than the two tables' TOTALs summed, whenever someone is rep-approved or registered under both divisions — see **Per-division or filtered re-cuts** below), and call out by name anyone who appears in both tables so the combined total is auditable, not just asserted.

**Derived lists** (each tagged with division and source sheet(s)):

- Approved AND registered
- Approved but NOT registered (the follow-up/chase list)
- Registered with NO approval row (nobody owns these attendees — a compliance/ownership gap)
- On BOTH flight and non-flight registration (double bookings — real cost, worth a manual check)
- Practice-name mismatches between approval and registration for the same person (use a stricter normalizer + `difflib.SequenceMatcher` threshold ~0.55 to separate genuine mismatches from cosmetic ones like "&" vs "and" or an added LLC)
- Name-variant merges actually made (audit trail) — every corroborated near-match merge applied (e.g. a Connie → Constance merge and what corroborated it), separate from the list below of merges considered but NOT made
- Needs human confirmation (ambiguous merge candidates, count as 2)

**Pipeline (if asked)**: Opportunity Amount / Opportunity Stage / Expected Value columns live ONLY on the Rep Approval sheets, at the deal/row level — not the deduplicated attendee headcount. Registration sheets are frequently entirely blank for these columns; confirm and say so explicitly rather than assuming. Flag identical dollar figures repeated across different accounts for the same rep as a possible copy-paste duplicate worth a human check, rather than silently including or excluding them.

**Per-division or filtered re-cuts**: when asked for "just Aesthetics" or "just Vision" after a full report, filter the same underlying cluster/dedup results rather than re-pulling or re-deriving — the person-level clusters don't change, only which ones you filter to. Watch for people who belong to both divisions (e.g. rep-approved on both AES and VIS Rep Approval sheets) and flag them explicitly in a per-division cut rather than silently dropping or double-counting them.

## 7. Delivery

- For a quick answer, a chat table is enough — but every answer, chat or Excel, states the matching rules applied and a count of merges made under each rule (exact-name auto-merges; corroborated near-matches, broken out by shared-email vs shared-practice), so the numbers are auditable without asking for a re-run. This isn't an Excel-only feature.
- When asked for "excel" or a shareable report, use the xlsx skill's conventions (Arial, styled headers, autofilter, frozen header row, `recalc.py` verification) and build a multi-tab workbook: Summary (including the header block from step 6), one tab per derived list, Double Bookings, Practice Mismatches, Needs Confirmation, Pipeline (if relevant), and Methodology (spelling out every matching rule and every merge made, so the numbers are auditable).
- Always disclose corrections transparently: if a self-check catches a missed merge after numbers were already reported, say exactly what changed and why before giving the new numbers — don't quietly revise.

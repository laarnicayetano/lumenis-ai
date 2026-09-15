<!--
Template for the budget-report skill's output.
Placeholders use {{curly_braces}}. Tables assume two divisions (AES, VIS);
duplicate/remove columns if the skill is ever run for a single division or
adds Hospital.
-->

## Budget Report

{{OPTIONAL_CAVEAT_CALLOUT}}

|                      | {{DIVISION_A}}   | {{DIVISION_B}}   |
| -------------------- | ---------------- | ---------------- |
| Full Year AOP Target | ${{A_TARGET}}    | ${{B_TARGET}}    |
| Paid                 | ${{A_PAID}}      | ${{B_PAID}}      |
| Committed            | ${{A_COMMITTED}} | ${{B_COMMITTED}} |
| Total                | ${{A_TOTAL}}     | ${{B_TOTAL}}     |
| Remaining Budget     | ${{A_REMAINING}} | ${{B_REMAINING}} |
| % of Budget Used     | {{A_PCT_USED}}%  | {{B_PCT_USED}}%  |

## Category breakdown

**{{DIVISION_A}}:**

| AOP Category                                                                   | AOP Budget          | Reconciled Actual   | Variance                                       |
| ------------------------------------------------------------------------------ | ------------------- | ------------------- | ---------------------------------------------- |
| {{A_CAT_1_NAME}}                                                               | ${{A_CAT_1_BUDGET}} | ${{A_CAT_1_ACTUAL}} | {{A_CAT_1_VARIANCE_SIGN}}${{A_CAT_1_VARIANCE}} |
| {{A_CAT_2_NAME}}                                                               | ${{A_CAT_2_BUDGET}} | ${{A_CAT_2_ACTUAL}} | {{A_CAT_2_VARIANCE_SIGN}}${{A_CAT_2_VARIANCE}} |
| {{A_CAT_N_NAME}}                                                               | ${{A_CAT_N_BUDGET}} | ${{A_CAT_N_ACTUAL}} | {{A_CAT_N_VARIANCE_SIGN}}${{A_CAT_N_VARIANCE}} |
| _({{A_UNMAPPED_CATEGORY_NAME}} — unmapped, ${{A_UNMAPPED_ACTUAL}} reconciled)_ | —                   | —                   | —                                              |

**{{DIVISION_B}}:**

| AOP Category                                                                   | AOP Budget          | Reconciled Actual   | Variance                                       |
| ------------------------------------------------------------------------------ | ------------------- | ------------------- | ---------------------------------------------- |
| {{B_CAT_1_NAME}}                                                               | ${{B_CAT_1_BUDGET}} | ${{B_CAT_1_ACTUAL}} | {{B_CAT_1_VARIANCE_SIGN}}${{B_CAT_1_VARIANCE}} |
| {{B_CAT_2_NAME}}                                                               | ${{B_CAT_2_BUDGET}} | ${{B_CAT_2_ACTUAL}} | {{B_CAT_2_VARIANCE_SIGN}}${{B_CAT_2_VARIANCE}} |
| {{B_CAT_N_NAME}}                                                               | ${{B_CAT_N_BUDGET}} | ${{B_CAT_N_ACTUAL}} | {{B_CAT_N_VARIANCE_SIGN}}${{B_CAT_N_VARIANCE}} |
| _({{B_UNMAPPED_CATEGORY_NAME}} — unmapped, ${{B_UNMAPPED_ACTUAL}} reconciled)_ | —                   | —                   | —                                              |
| _({{B_NO_COUNTERPART_NOTE}})_                                                  | —                   | —                   | —                                              |

## Rows with no PO# (Pending Approval)

**{{DIVISION_A}}** ({{A_NO_PO_COUNT}}):

| PR#             | Date into SAP       | Header Text         | Category              | Quarter              | Status              | Valuation Price         |
| --------------- | ------------------- | -------------------- | --------------------- | -------------------- | ------------------- | ----------------------- |
| {{A_NOPO_1_PR}} | {{A_NOPO_1_DATE}} | {{A_NOPO_1_HEADER}} | {{A_NOPO_1_CATEGORY}} | {{A_NOPO_1_QUARTER}} | {{A_NOPO_1_STATUS}} | ${{A_NOPO_1_VALUATION}} |

**{{DIVISION_B}}** ({{B_NO_PO_COUNT}}):

| PR#             | Date into SAP       | Header Text         | Category              | Quarter              | Status              | Valuation Price         |
| --------------- | ------------------- | -------------------- | --------------------- | -------------------- | ------------------- | ----------------------- |
| {{B_NOPO_1_PR}} | {{B_NOPO_1_DATE}} | {{B_NOPO_1_HEADER}} | {{B_NOPO_1_CATEGORY}} | {{B_NOPO_1_QUARTER}} | {{B_NOPO_1_STATUS}} | ${{B_NOPO_1_VALUATION}} |

## Oldest Open PRs

**{{DIVISION_A}}** (showing {{A_OLDEST_SHOWN_COUNT}} of {{A_OPEN_PR_COUNT}} open — {{A_OLDEST_MORE_NOTE}}):

| PR#               | Date into SAP       | Header Text           | Status                | PO#               | Valuation Price           |
| ----------------- | ------------------- | --------------------- | ---------------------- | ----------------- | ------------------------- |
| {{A_OLDEST_1_PR}} | {{A_OLDEST_1_DATE}} | {{A_OLDEST_1_HEADER}} | {{A_OLDEST_1_STATUS}} | {{A_OLDEST_1_PO}} | ${{A_OLDEST_1_VALUATION}} |

**{{DIVISION_B}}** (showing {{B_OLDEST_SHOWN_COUNT}} of {{B_OPEN_PR_COUNT}} open — {{B_OLDEST_MORE_NOTE}}):

| PR#               | Date into SAP       | Header Text           | Status                | PO#               | Valuation Price           |
| ----------------- | ------------------- | --------------------- | ---------------------- | ----------------- | ------------------------- |
| {{B_OLDEST_1_PR}} | {{B_OLDEST_1_DATE}} | {{B_OLDEST_1_HEADER}} | {{B_OLDEST_1_STATUS}} | {{B_OLDEST_1_PO}} | ${{B_OLDEST_1_VALUATION}} |

{{CLOSING_NOTE — e.g. reconciliation confidence note}}

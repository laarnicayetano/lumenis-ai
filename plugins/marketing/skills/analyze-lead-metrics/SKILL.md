---
name: analyze-lead-metrics
description: Analyze a lead-status/pipeline data export (e.g. CRM lead dashboard) split across business lines, as either a full analysis or an executive-simplified summary. Use when the user pastes lead/pipeline data and asks to "analyze these leads," wants a "full analysis" or "assessment," or wants leads/pipeline data "simplified for executives." Always confirm which output is wanted before producing one — don't default to both.
---

# Lead metrics analysis

Turns a raw lead-status export into one of two outputs: a full analysis or an executive-simplified summary. These are two distinct deliverables, not a two-pass sequence — produce only the one that's actually wanted.

## Input

A lead/pipeline data table, pasted or attached, typically from a CRM export. Expect:

- **A business-line split** — most commonly Vision/Ophthalmic vs. Aesthetics, but use whatever divisions the data actually contains.
- **A status funnel**, commonly staged (e.g. "1/4 Open," "2/4 Could not reach," "3/4 Nurturing," "4/4 Cold lead") alongside terminal states (CONVERTED, DISQUALIFIED, Abandoned). Statuses vary by export — read what's actually there rather than assuming this exact list, but expect a staged-pipeline + terminal-state shape.
- **Touched vs. not-touched** counts or a way to derive them, where present.

If the data is missing a clear division split or status labels are ambiguous, ask rather than guessing at what a status code means.

## Which output — ask before producing either

The request usually makes this clear ("analyze these leads" → full analysis; "simplify for executives" → executive-simplified), but if it's genuinely ambiguous (e.g. just "can you look at this data"), ask which is wanted rather than assuming or building both. Producing the full analysis when a two-line executive summary was wanted (or vice versa) wastes a turn either way — confirm first.

## Output option A: Full analysis

1. **Totals**: total leads, and the split by business line (count + % of total each).
2. **Status distribution**: count (and %) per status, called out per business line where the split matters.
3. **Conversion metrics**: conversion rate overall and per business line (converted / total for that line) — this comparison is usually the most load-bearing number in the whole analysis.
4. **Touch analysis**: touched vs. not-touched, especially within "Open" leads — untouched-but-open leads are the immediate-action item.
5. **Areas for improvement / opportunity**: call out concretely — e.g. size of the disqualified/abandoned pool, size of the untouched-open pool, any business line underperforming the other and by how much.

Offer a visualization (stacked bar of status by division, plus key-metric cards for total/conversion-rate/open) if useful, but don't build one unasked — offer it the way the full analysis naturally leads there.

## Output option B: Executive-simplified summary

- **Key Numbers**: total leads, overall conversion rate, size of the active pipeline (open + nurturing) — 3-5 numbers, no more.
- **Top insights** (2-4): the comparisons and patterns that actually matter — which line is outperforming and by how much, the untouched/immediate-opportunity pool, a quality concern (disqualification rate) if notable. State the "so what," not just the number.
- **Recommended action(s)**: one or two concrete, near-term moves tied directly to an insight above (e.g. "contact the N untouched open leads this week") — not a generic process-improvement list.

Keep it short enough to read in under a minute — headline numbers and a few bullets, not paragraphs. This is derived from the same underlying data as the full analysis, but work it out directly rather than writing out the full analysis first — the point is a fast, compressed read, not an intermediate document.

## Notes

- If the person wants both eventually, that's two separate requests, not one skill invocation producing both — build the one that was asked for, and only produce the other if they explicitly ask for it next (e.g. "now simplify that for executives").
- Business-line comparison (which line is winning, and why) is consistently the most useful single insight across past requests like this — don't bury it, in either output.
- Pair with [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md)'s Executive Team persona for tone in the executive-simplified output.

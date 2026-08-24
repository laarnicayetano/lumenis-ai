---
name: create-slides
description: Build a slide deck as plain, clearly-labeled markdown text, or restructure the narrative flow of a deck that already has content. Use when the user wants a presentation, slide deck, or deck outline built from a topic/key points or existing long-form content — or when they already have slide content/an outline and want the story reviewed, re-sequenced, or fixed (e.g. a QBR deck that needs better flow, a stronger "ask" slide, or a better executive summary). Recognizes named recurring deck types (QBR, close meeting, AOP, sales weekly update) with their own default structure. Pair with the audience-archetypes skill to match tone/depth to who the deck is for.
---

# Slide builder

Produces a full slide deck as plain markdown text. No visual design, no theme, no rendering — just clearly-labeled slide content that a human (or a later export step) can turn into an actual deck. This intentionally does not depend on the Lumenis design system.

## Input

Accept whatever the user has on hand:

- A topic plus rough key points/outline, or
- Existing long-form content (a doc, brief, report) to distill down into slide form, or
- An existing deck's content/outline that needs its narrative reviewed or fixed rather than built fresh — see **Narrative restructuring** below

Also establish, before or while drafting:

- **Audience** — load [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) and match tone/depth/emphasis to whichever persona(s) apply. If it's not clear from the request, ask.
- **Purpose/context** — what's this deck for (e.g. KOL training, sales pitch, internal update, conference talk)? This affects which slide types belong.
- **Roughly how many slides** — if not specified, use your judgment based on the amount of source content, but default toward fewer, denser slides over many thin ones.

## Output format

Plain markdown. One slide per section, separated by `---`. Each slide labeled clearly so there's no ambiguity about what a line represents:

```
## Slide 1 — Title
# [Deck title]
### [Subtitle, if any]

> Speaker notes: [optional — context the presenter needs but the slide shouldn't show]

---

## Slide 2 — Agenda
### Agenda
- [Item]
- [Item]

---

## Slide 3 — Content
### [Slide headline — the one idea this slide makes]
- [Point, short phrase not a full sentence]
- [Point]
- [Point]

> Speaker notes: [optional]

---

## Slide 4 — Data
### [Slide headline]
[CHART: description of the chart/data that would go here — no design system to render it yet]

---

## Slide N — Close
### Thank You
[Contact info / call to action]
```

Common slide types to draw from as needed: title, agenda/overview, section divider, content (one idea per slide), data/chart placeholder, comparison, quote/testimonial, key takeaways/summary, call-to-action, thank-you/contact. Not every deck needs all of these — pick what the purpose calls for.

## Named deck types

Some deck purposes recur often enough to have their own default structure — check whether the request matches one of these before improvising a structure from scratch, and read only the matching file:

- [deck-types/qbr.md](deck-types/qbr.md) — quarterly business review for a C-suite/exec audience.
- [deck-types/close-meeting.md](deck-types/close-meeting.md) — sales quarter-close/management meeting, revenue-focused.
- [deck-types/aop.md](deck-types/aop.md) — Annual Operating Plan, budget allocation and approval.
- [deck-types/sales-weekly-update.md](deck-types/sales-weekly-update.md) — recurring weekly field-sales call deck.

If a new recurring deck type shows up that doesn't fit these, add a new file here rather than improvising each time — follow the existing files' pattern (default shape, tone pointer to audience-archetypes, note on how it differs from the generic flow below).

## Narrative restructuring

Sometimes the input isn't a topic to build from but an existing deck's content or outline that already has slides — the ask is to fix how it *reads*, not to write new material. Treat this as a distinct pass:

1. Read the existing content in full before touching structure — identify what story it's currently telling (even if unintentionally) and where it breaks: a slide in the wrong place, a summary that doesn't summarize, an ask that's missing or diluted, results presented with no "why."
2. Re-sequence and re-frame using the same slide-type vocabulary above — this is edit/reorder work, not a rewrite from scratch. Keep the user's actual content; move it, retitle it, tighten it, or split/merge slides as the flow requires. If the deck matches a named type above, use its default shape as the target structure to restructure toward, adjusted for whatever content actually exists.
3. Output the same plain-markdown format as any other deck, but call out what changed and why in a short note above the deck (e.g. "moved the ask earlier — it was buried on slide 9; reframed the exec summary to lead with outcome, not activity") so the user can see the edit, not just the result.

## Brevity rules

- One idea per slide. If a slide needs two, split it.
- Max ~5–6 bullets per slide.
- Bullets are short phrases, not full sentences — this is a presentation aid, not a document.
- Cut ruthlessly. If a point doesn't support the deck's purpose or audience, leave it out rather than including it "just in case."
- Speaker notes are the place for detail, caveats, and context — not the slide itself.

## Notes

- This skill only produces the text-form deck. It does not render to PDF/PPTX/HTML — that's a separate future step, and when it's built it should use a pure-Python approach (e.g. python-pptx / reportlab) rather than a browser-dependent renderer, so it works reliably wherever this skill runs (including claude.ai's sandboxed environment).
- Always load [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) unless the user has already made the audience explicit.
- Pair with [core:brand-context](../../../core/skills/brand-context/SKILL.md) for company voice underneath whatever audience-specific tone applies.

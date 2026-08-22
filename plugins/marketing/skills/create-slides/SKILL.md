---
name: create-slides
description: Build a slide deck as plain, clearly-labeled markdown text — no design system or visual rendering involved. Use when the user wants a presentation, slide deck, or deck outline built from a topic/key points or from existing long-form content (a doc, brief, or report). Pair with the audience-archetypes skill to match tone/depth to who the deck is for.
---

# Slide builder

Produces a full slide deck as plain markdown text. No visual design, no theme, no rendering — just clearly-labeled slide content that a human (or a later export step) can turn into an actual deck. This intentionally does not depend on the Lumenis design system.

## Input

Accept whatever the user has on hand:
- A topic plus rough key points/outline, or
- Existing long-form content (a doc, brief, report) to distill down into slide form

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

## Brevity rules

- One idea per slide. If a slide needs two, split it.
- Max ~5–6 bullets per slide.
- Bullets are short phrases, not full sentences — this is a presentation aid, not a document.
- Cut ruthlessly. If a point doesn't support the deck's purpose or audience, leave it out rather than including it "just in case."
- Speaker notes are the place for detail, caveats, and context — not the slide itself.

## Notes
- This skill only produces the text-form deck. It does not render to PDF/PPTX/HTML — that's a separate future step, and when it's built it should use a pure-Python approach (e.g. python-pptx / reportlab) rather than a browser-dependent renderer, so it works reliably wherever this skill runs (including claude.ai's sandboxed environment).
- Always load [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) unless the user has already made the audience explicit.
- Pair with [marketing:positioning](../positioning/SKILL.md) and [core:brand-context](../../../core/skills/brand-context/SKILL.md) for company voice underneath whatever audience-specific tone applies.

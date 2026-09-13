---
name: create-job-description
description: Draft or revise a complete job description, delivered as plain text or a .docx file. Use whenever the user wants to create, draft, write, or edit a job description, job posting, JD, or role/position description — a brand-new role or a revision of an existing one. Defaults to the US market, a B2B business with a direct field-sales collaboration model, and a HubSpot + Salesforce tech stack unless told otherwise.
---

# Job description writer

Produces a complete, ready-to-post job description for a Lumenis role. The company context is fixed (B2B, US-only, sales-aligned — see **Defaults** below); what changes per request is the role itself: title, department, seniority, and what the person will actually do.

## Input

Ask only for what you can't reasonably infer:

- **Role title** — required.
- **Department / business unit** — e.g. If the role sits under a named business unit (Aesthetics, Vision) or supports a specific product, note it — it changes which context to load (see **Context to pull** below).
- **Seniority / reporting line** — individual contributor, manager, director+; who they report to. Shapes structure (see **Structure**).
- **What the user already knows** — any responsibilities, must-have qualifications, travel %, comp notes, or team size already decided. Treat these as fixed facts, not suggestions to soften or drop.
- **Output format** — plain text or `.docx`. Ask if not specified.
- **New role vs. edit** — if editing an existing JD, treat the pasted draft as the source of truth for facts already in it; don't quietly rewrite scope or requirements that weren't part of the ask.

Don't ask about market (always US) or core tech stack (always HubSpot + Salesforce where relevant) — those are fixed defaults, not open questions. Only raise them if the role plausibly doesn't fit the default (see below).

## Context to pull before drafting

- Always ground company framing (mission, tone, positioning) in [core:brand-context](../../../core/skills/brand-context/SKILL.md).
- If the role sits in or supports **Aesthetics**, load [core:aesthetics](../../../core/skills/aesthetics/SKILL.md); for **Vision**, load [core:vision](../../../core/skills/vision/SKILL.md). Either gives business-unit-level portfolio and positioning context — layer the specific `core:product-*` skill on top where the role is tied to one product.
- [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) is occasionally useful for roles that engage a named external audience directly (e.g. a role working with KOLs or practice owners) — load it only when describing that interaction accurately matters, not as a default.

## Defaults (the company context, unless told otherwise)

- **Market: US only.** No visa sponsorship language, no international-territory framing, no non-US compliance references. Travel language should describe travel _within_ the US when relevant, not "international."
- **B2B, direct field-sales collaboration.** Most roles should name how they work with the field sales team, not just marketing — this is a standing part of the operating model here, not a role-specific detail to invent case by case. See the marketing-automation-manager example for how territory/region-based sales alignment gets folded into daily responsibilities.
- **Tech stack: HubSpot + Salesforce.** Bake these in wherever the role is genuinely CRM/marketing-ops/sales-ops facing (required or technical-skills section). Use judgment on where it doesn't belong — a pure creative/production role (see the event-production-manager example) legitimately has zero CRM tooling in it; forcing HubSpot/Salesforce into every JD regardless of fit reads as templated and undermines the rest of the document.

## Structure

The four files in `examples/` are real Lumenis-pattern JDs — read the one or two closest to the requested role's seniority and function before drafting, rather than working from the template below alone. They intentionally vary in style (all-caps section headers and tiered "Must Excel / Expected / Nice to Have" responsibilities vs. plain markdown headers and flat bullet lists) — pick the register that matches the role:

- **Simple, single-owner roles** (individual contributor, narrower scope) → the plain Overview / Key Responsibilities / Required Qualifications shape in `marketing-specialist-vision.md`. This is the closest thing to a standard company template — default to this shape when nothing else points elsewhere.
- **Senior/strategic roles with real budget or KPI accountability** → the tiered responsibility structure and Success Metrics section in `event-production-manager.md`, or the deliverables-heavy structure in `marketing-automation-manager.md` for a role with recurring operational reporting.
- **Leadership roles with direct reports** → `marketing-director.md`'s shape (Strategic Leadership / Team Management / Operations / Cross-functional, plus Career Advancement Criteria).

A typical JD includes, roughly in this order: title (+ department/business unit line), Position Overview, Key Responsibilities (grouped by theme for broader roles, flat for narrow ones), Required Qualifications, Preferred/Technical Qualifications, Reporting Structure, Working Conditions (including travel % and US-only framing), and — for senior roles — Success Metrics. Close with a short CTA line for individual-contributor roles (see `marketing-specialist-vision.md`); senior roles can close on Compensation Philosophy or Salary Range & Benefits instead (see `event-production-manager.md` and `marketing-director.md`).

## Output

- **Plain text**: clean prose, matching whichever register was chosen above (markdown headers are fine for the markdown-style templates; all-caps section headers with no markdown syntax for the tiered style). Don't mix the two conventions within one document.
- **`.docx`**: write the finished JD as clean Markdown first, then convert:
  1. If `pandoc` is available (`which pandoc`), run `pandoc job-description.md -o "<Role Title>.docx"`.
  2. Otherwise, use `python-docx` (`pip install python-docx` if not already installed) with a short script that maps headers to Word heading styles and bullets to Word list items — don't hand back a `.docx` that's just a plain-text dump with no real formatting.
  3. Confirm the file was created and tell the user its path — don't just claim success.

## Notes

- If a request doesn't specify department or seniority and it isn't inferable from the title, ask — the structure and tone genuinely differ enough (see **Structure**) that guessing produces a document that has to be redone.
- When editing an existing JD, run it past the same **Defaults** checklist (US-only framing, field-sales tie-in, tech-stack fit) rather than only making the literally-requested edit — but flag any default you're adding rather than silently inserting it into someone else's draft.

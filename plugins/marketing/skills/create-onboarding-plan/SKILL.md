---
name: create-onboarding-plan
description: Create or edit a 30-60-90 day onboarding plan for a new marketing hire, output as plain markdown text — never a .docx or artifact. Includes a market/category/competitive learning module (aesthetics market, energy-based device market, medspas, dermatology, plastic surgery, competitor SWOTs) building toward the new hire producing their own first marketing plan by day 90. The user takes it into Claude Design themselves for a polished layout if they want one. Use when the user wants a new-hire onboarding plan, 30-60-90 plan, or wants to edit an existing one.
---

# Onboarding plan writer

Builds a 30-60-90 day onboarding plan for a new hire joining the marketing org. The plan is genuinely different by role — a field-facing product marketer and an internal marketing-ops hire don't get the same introductions or learning path — so role drives most of the content, not just the header.

**The point of the plan is not just orientation.** By day 90 the new hire should be sharp on the portfolio, the category, and the competitive landscape, and should have applied that — together with whatever expertise they already brought in — to a first real marketing plan or point of view. Every learning module below builds toward that, not toward a stack of read-only reference material.

## Input

Always required — ask if not given:

- **New hire name**
- **Role** — the title. This drives almost everything else; see **Role shapes the plan** below.
- **Team** — which team/function they're joining.
- **Start date**
- **Manager**

Ask the user directly rather than guessing — these are decisions only they can make:

- **Next New Hire Training date**, so it can be placed in the plan. If they don't know it, note it in the plan as "TBD — confirm with Bill" rather than inventing a date.
- **Platform access** (HubSpot, Salesforce, Smartsheet, Asana, SharePoint, OneDrive, DropBox, anything else) the new hire should have by day 30 — ask which ones apply to this role.
- **Meeting** — the new hire needs to know what meetings they will be apart of; ask what meetings they need to be a part of and what is the cadence of the meetings.
- **Product Manager / BU personnel** worth introducing this new hire to — ask which ones make sense, don't guess from the title alone.
- **What the new hire already brings** — prior industry, role, or domain expertise the manager is hiring for. This is what the learning modules and the day-90 marketing plan should explicitly build on (see **Market, category & competitive learning**) — without it, the plan can only teach Lumenis, not connect Lumenis to what this person already knows.

Nice to have — use if the user provides them, otherwise leave a clearly-marked placeholder rather than inventing a name:

- Local sales rep (for the video call and ride-along)
- Specific vendor contacts (PR, Marketing Agency, Event Production, AV, Social)

## Role shapes the plan

- If a job description exists for this role, use it to learn realistic responsibilities, tools, and who the role actually works with — check [create-job-description's examples](../create-job-description/examples/) for a role that matches, or ask the user to paste the real JD. Use this to decide which sections below genuinely apply, rather than including everything by default.
- **Products & market learning** — the portfolio is large, so give every hire a breadth pass and only some hires real depth. Load [core:aesthetics](../../../core/skills/aesthetics/SKILL.md) for an Aesthetics-facing role or [core:vision](../../../core/skills/vision/SKILL.md) for a Vision-facing role — full business-unit portfolio, technology platforms, and condition/treatment categories, regardless of seniority — that's the breadth layer everyone gets. Then go deep on whichever `core:product-*` skill(s) the role is actually tied to (most Vision products besides OptiLIFT/OptiLIGHT don't have a dedicated product skill yet — `core:vision` is the fallback there, not an invented one).
- **Sales exposure** — every hire gets a video call with a local sales rep. Only roles with broader remit (director+, or a role that shapes sales-facing programs) should also meet Regional Sales Managers or the VP of Sales — don't add senior sales leadership to every plan by default.
- **Vendor introductions** — only for roles that would plausibly own or touch a vendor relationship (events, PR, advertising, AV). Skip entirely for roles with no vendor-facing scope rather than including it as a formality.

## Output

Plain markdown text only — never generate a `.docx` or a design artifact for this. If the user wants a polished/visual version, tell them to take the plain-text output into Claude Design themselves; that's a separate, deliberate step, not something this skill does.

Structure exactly as follows. Omit a bullet only when **Role shapes the plan** says it genuinely doesn't apply — don't pad with filler to keep every section present.

### 30-60-90 Onboarding Plan

- Open with new hire name, role, team, start date, manager.
- Note the next New Hire Training date if the user provided one (or flag it TBD).
- Products & market orientation appropriate to their department (see **Role shapes the plan**).
- By day 30: platform access needed (HubSpot / Salesforce / Smartsheet / Asana / SharePoint / OneDrive / DropBox / other), as confirmed with the user — don't assume access needs.
- Overview of sprint planning & reporting cadence.
- Overview of project management and tracking (tools/process the team actually uses).
- Lay this out across the 30/60/90 phases: orientation and access concentrated early, ramping to real ownership by day 90.
- Point to the **Market, category & competitive learning** module below and its day-90 capstone as part of the plan, not a separate track.

### Market, category & competitive learning

A dedicated learning track, phased across the 90 days, that builds toward the new hire producing their own marketing plan or point of view — not a pile of reading assigned and never followed up on. Don't invent market data or competitor specifics that aren't sourced from something real (a Lumenis skill, the company site, or research the new hire does and reports back) — this module is where fabricated "facts" would be most damaging.

- **Days 1-30 — portfolio and category orientation:**
  - Full business-unit product portfolio and technology platforms — `core:aesthetics` or `core:vision` as applies — as breadth, regardless of role.
  - The energy-based device (EBD) category itself — what it is, how it's regulated, how it's sold — as the umbrella category Lumenis competes in.
  - The customer/channel landscape this role will actually sell or market into: medspas, dermatology practices, and plastic surgery practices as distinct segments — how they differ in buying behavior, decision-maker, and what they value, not treated as one undifferentiated "provider" audience.
  - If the new hire brought outside expertise (from Input), have them note early where it maps or doesn't map to this category — that comparison is itself useful onboarding output, not busywork.
- **Days 31-60 — competitive landscape:**
  - Build the working competitor list from what's already documented: check each relevant product's `core:product-*` skill for its **Competitors** section first (several are populated — e.g. FoLix vs. LaserMD/Alma TED/Nutrafol, triLift vs. Morpheus8/Genius/Secret/Emface — others are marked "not yet provided," which is a real gap to research, not to fill in with a guess).
  - Where a product's competitor section is empty, that's an assignment for the new hire: research and propose the missing competitor list (and flag it back so the source skill can eventually be updated), rather than the plan asserting competitors that were never verified.
  - Have the new hire produce a short SWOT per major competitor identified — this is their work product to build (with guidance/review from their manager), not something handed to them pre-filled, since building it is how the learning actually happens.
- **Days 61-90 — synthesis and capstone:**
  - The new hire drafts a first marketing plan or point of view for their area, explicitly informed by the portfolio/category orientation, the competitor SWOTs, and — critically — the expertise they came in with (see Input). Name specifically how their prior background should shape this (a fresh angle, a channel they already know, a gap they're positioned to spot) rather than leaving "apply their skillset" implicit.
  - Set a review checkpoint with the manager for this deliverable before day 90 closes out.

### Meetings

- List the recurring meetings this hire should join.
- Always include the sales-marketing meeting, with the cadence/timing the user provided.

### Planned Introductions

- Cap at **4 introductions per week** across the full 90-day period — spread across the plan, not front-loaded into week one.
- **Vendors** (PR, Marketing Agency, Event Production, AV, Social) — only where role-relevant per **Role shapes the plan**.
- **Sales** — video call with a local sales rep for every hire; Regional Sales Manager / VP of Sales only where role-relevant. Schedule a ride-along with a local sales rep sometime within the 90-day window.
- **Business Unit** — Product Manager / BU personnel, per what the user specified.
- **Marketing** — calls with teammates to learn their function and the systems they use day to day.

### Key Contacts

| Person      | Role      | For What                            |
| ----------- | --------- | ----------------------------------- |
| [Manager]   | Manager   | Day-to-day guidance                 |
| [VP Sales]  | Sales     | Questions on sales                  |
| [RSM 1]     | Sales     | Regional Sales Manager for [Region] |
| [Teammates] | Marketing | Questions, culture, navigation      |

Fill in names where the user gave them; leave the bracketed placeholder where they didn't, rather than inventing a name.

## Notes

- If role, team, or manager is missing, ask before drafting — the plan is genuinely different per role, and guessing produces a plan that has to be redone rather than lightly edited.
- Editing an existing plan: treat what's already in it (dates, names, decisions already made) as source of truth. Make the requested change; don't regenerate the whole plan from scratch.

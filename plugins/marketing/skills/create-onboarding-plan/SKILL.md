---
name: create-onboarding-plan
description: Create or edit a 30-60-90 day onboarding plan for a new marketing hire, output as plain markdown text — never a .docx or artifact. The user takes it into Claude Design themselves for a polished layout if they want one. Use when the user wants a new-hire onboarding plan, 30-60-90 plan, or wants to edit an existing one.
---

# Onboarding plan writer

Builds a 30-60-90 day onboarding plan for a new hire joining the marketing org. The plan is genuinely different by role — a field-facing product marketer and an internal marketing-ops hire don't get the same introductions or learning path — so role drives most of the content, not just the header.

## Input

Always required — ask if not given:

- **New hire name**
- **Role** — the title. This drives almost everything else; see **Role shapes the plan** below.
- **Team** — which team/function they're joining.
- **Start date**
- **Manager**

Ask the user directly rather than guessing — these are decisions only they can make:

- **Next New Hire Training date**, so it can be placed in the plan. If they don't know it, note it in the plan as "TBD — confirm with HR/People Ops" rather than inventing a date.
- **Platform access** (HubSpot, Salesforce, Smartsheet, anything else) the new hire should have by day 30 — ask which ones apply to this role.
- **Sales-marketing meeting cadence** — the new hire should be part of it; ask when it happens rather than assuming a day/time.
- **Product Manager / BU personnel** worth introducing this new hire to — ask which ones make sense, don't guess from the title alone.

Nice to have — use if the user provides them, otherwise leave a clearly-marked placeholder rather than inventing a name:

- Local sales rep (for the video call and ride-along)
- Specific vendor contacts (PR, ad agency, event production, AV)
- IT and HR contact names for the Key Contacts table

## Role shapes the plan

- If a job description exists for this role, use it to learn realistic responsibilities, tools, and who the role actually works with — check [create-job-description's examples](../create-job-description/examples/) for a role that matches, or ask the user to paste the real JD. Use this to decide which sections below genuinely apply, rather than including everything by default.
- **Products & market learning** — scope to the new hire's department/business unit: load [core:aesthetics](../../../core/skills/aesthetics/SKILL.md) for an Aesthetics-facing role, or the relevant `core:product-*` skill if the role is tied to one product. There's no Vision-level business-unit skill yet — for a Vision role, use [core:brand-context](../../../core/skills/brand-context/SKILL.md) plus the product skill where one applies.
- **Sales exposure** — every hire gets a video call with a local sales rep. Only roles with broader remit (director+, or a role that shapes sales-facing programs) should also meet Regional Sales Managers or the VP of Sales — don't add senior sales leadership to every plan by default.
- **Vendor introductions** — only for roles that would plausibly own or touch a vendor relationship (events, PR, advertising, AV). Skip entirely for roles with no vendor-facing scope rather than including it as a formality.

## Output

Plain markdown text only — never generate a `.docx` or a design artifact for this. If the user wants a polished/visual version, tell them to take the plain-text output into Claude Design themselves; that's a separate, deliberate step, not something this skill does.

Structure exactly as follows. Omit a bullet only when **Role shapes the plan** says it genuinely doesn't apply — don't pad with filler to keep every section present.

### 30-60-90 Onboarding Plan

- Open with new hire name, role, team, start date, manager.
- Note the next New Hire Training date if the user provided one (or flag it TBD).
- Products & market orientation appropriate to their department (see **Role shapes the plan**).
- By day 30: platform access needed (HubSpot / Salesforce / Smartsheet / other), as confirmed with the user — don't assume access needs.
- Overview of sprint planning & reporting cadence.
- Overview of project management and tracking (tools/process the team actually uses).
- Lay this out across the 30/60/90 phases: orientation and access concentrated early, ramping to real ownership by day 90.

### Meetings

- List the recurring meetings this hire should join.
- Always include the sales-marketing meeting, with the cadence/timing the user provided.

### Planned Introductions

- Cap at **4 introductions per week** across the full 90-day period — spread across the plan, not front-loaded into week one.
- **Vendors** (PR, ad agency, event production, AV) — only where role-relevant per **Role shapes the plan**.
- **Sales** — video call with a local sales rep for every hire; Regional Sales Manager / VP of Sales only where role-relevant. Schedule a ride-along with a local sales rep sometime within the 90-day window.
- **Business Unit** — Product Manager / BU personnel, per what the user specified.
- **Marketing** — calls with teammates to learn their function and the systems they use day to day.

### Key Contacts

| Person | Role | For What |
|---|---|---|
| [Manager] | Manager | Day-to-day guidance |
| [Sales Contact] | Sales | Questions on sales |
| [Teammates] | Marketing | Questions, culture, navigation |
| [IT Contact] | IT | Tool access, equipment |
| [HR Contact] | HR | Benefits, policies |

Fill in names where the user gave them; leave the bracketed placeholder where they didn't, rather than inventing a name.

## Notes

- If role, team, or manager is missing, ask before drafting — the plan is genuinely different per role, and guessing produces a plan that has to be redone rather than lightly edited.
- Editing an existing plan: treat what's already in it (dates, names, decisions already made) as source of truth. Make the requested change; don't regenerate the whole plan from scratch.

---
name: create-onboarding-plan
description: Create or edit a 30-60-90 day onboarding plan for a new marketing hire, output as a folder of five .docx files (Onboarding Plan, Competitors, Product Portfolio, Customer, and a blank Weekly Status Report template) — never plain text or an artifact. Requires the new hire's department (Aesthetics or Vision) up front, since three of the five files are pulled from that business unit's own skill content. Builds toward the new hire producing their own first marketing plan by day 90, with weekly status reports along the way. Use when the user wants a new-hire onboarding plan, 30-60-90 plan, or wants to edit an existing one.
---

# Onboarding plan writer

Builds a 30-60-90 day onboarding plan for a new hire joining the marketing org. The plan is genuinely different by role — a field-facing product marketer and an internal marketing-ops hire don't get the same introductions or learning path — so role drives most of the content, not just the header. The plan is for the new hire and not for a person onboarding them. We should not be mentioning their resume or background.

**Key outcome — the point of the plan is not just orientation.** By day 90 the new hire should be sharp on the portfolio, the category, and the competitive landscape, and should have turned that into a robust marketing plan that does two specific things: (1) takes a point of view on how Lumenis should move as the market and consumer behavior move — not just a description of where things stand today — and (2) visibly applies the expertise _they themselves_ brought to Lumenis, named explicitly rather than left implicit. Every learning module below builds toward that outcome, and none of it is read-only — see **Feedback loop** below. Reading without reporting back doesn't count as progress.

## Input

Always required — ask if not given:

- **New hire name**
- **Department — Aesthetics or Vision.** Required before drafting, not inferred from the role title: three of the five output files (Competitors, Product Portfolio, Customer) are pulled directly from that business unit's own skill content, so the skill cannot proceed without knowing which one applies. If the role genuinely spans both or sits outside either (e.g. a corporate/shared-services role), say so rather than guessing — don't default to one.
- **Role** — the title. This drives almost everything else; see **Role shapes the plan** below.
- **Start date**
- **Manager**

Ask the user directly rather than guessing — these are decisions only they can make:

- **Next New Hire Training date**, so it can be placed in the plan. If they don't know it, note it in the plan as "TBD — confirm with Bill" rather than inventing a date.
- **Meeting** — the new hire needs to know what meetings they will be apart of; ask what meetings they need to be a part of and what is the cadence of the meetings.
- **Product Manager / BU personnel** worth introducing this new hire to — ask which ones make sense, don't guess from the title alone.
- **What the new hire already brings** — prior industry, role, or domain expertise the manager is hiring for. This is what the learning modules and the day-90 marketing plan should explicitly build on (see **Market, category & competitive learning**) — without it, the plan can only teach Lumenis, not connect Lumenis to what this person already knows.

Nice to have — use if the user provides them, otherwise leave a clearly-marked placeholder rather than inventing a name:

- **Resume** — if the user supplies one (pasted or a file), read it in full and use it in place of a verbal summary for "what the new hire already brings": it grounds **Resume-informed tasks** (see Output) in specific, real evidence — named employers, tools, campaign types, quantified results — rather than a general impression. If both a resume and a verbal description are given, the resume is the more precise source for specifics; the verbal description still matters for anything the resume wouldn't show (soft skills, why they were hired, team fit).
- Local sales rep (for the video call and ride-along)
- Specific vendor contacts (PR, Marketing Agency, Event Production, AV, Social)

## Role shapes the plan

- If a job description exists for this role, use it to learn realistic responsibilities, tools, and who the role actually works with — check [create-job-description's examples](../create-job-description/examples/) for a role that matches, or ask the user to paste the real JD. Use this to decide which sections below genuinely apply, rather than including everything by default.
- **Products & market learning** — the portfolio is large, so give every hire a breadth pass and only some hires real depth. The Department input (Aesthetics or Vision) settles which business unit's [core:aesthetics](../../../core/skills/aesthetics/SKILL.md) or [core:vision](../../../core/skills/vision/SKILL.md) content to pull — full business-unit portfolio, technology platforms, and condition/treatment categories, regardless of seniority, is the breadth layer everyone gets. Then go deep on whichever `core:product-*` skill(s) the role is actually tied to (most Vision products besides OptiLIFT/OptiLIGHT don't have a dedicated product skill yet — `core:vision` is the fallback there, not an invented one).
- **Sales exposure** — every hire gets a video call with a local sales rep. Only roles with broader remit (director+, or a role that shapes sales-facing programs) should also meet Regional Sales Managers or the VP of Sales — don't add senior sales leadership to every plan by default.
- **Vendor introductions** — only for roles that would plausibly own or touch a vendor relationship (events, PR, advertising, AV). Skip entirely for roles with no vendor-facing scope rather than including it as a formality.

## Output

**A folder, not a single document** — never plain text, never one combined file, never a design artifact. The folder contains exactly five `.docx` files:

1. `Onboarding Plan.docx`
2. `Product Portfolio.docx`
3. `Competitors.docx`
4. `Customer.docx`
5. `Weekly Status Report Template.docx`

Name the folder `<New Hire Name> Onboarding/`. Files 2-4 are not written from scratch — they're each generated from the matching business-unit skill file for the Department given in Input, so the same source of truth used everywhere else in this repo is what the new hire reads too:

| File                     | Source (Aesthetics)                                                                          | Source (Vision)                                                                      |
| ------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `Product Portfolio.docx` | [core:aesthetics/product-portfolio.md](../../../core/skills/aesthetics/product-portfolio.md) | [core:vision/product-portfolio.md](../../../core/skills/vision/product-portfolio.md) |
| `Competitors.docx`       | [core:aesthetics/competitors.md](../../../core/skills/aesthetics/competitors.md)             | [core:vision/competitors.md](../../../core/skills/vision/competitors.md)             |
| `Customer.docx`          | [core:aesthetics/customers.md](../../../core/skills/aesthetics/customers.md)                 | [core:vision/customers.md](../../../core/skills/vision/customers.md)                 |

Convert the source file's content faithfully — this is the same content that already lives in the business-unit skill, reformatted for a standalone read, not a rewrite or a summary. Carry over its caveats as-is (e.g. Vision's `competitors.md` says outright that it's an unresearched placeholder — that caveat must survive into `Competitors.docx`, not get smoothed away in the conversion). If the source file has since changed and this skill's own copy of its guidance is stale, trust the live file over anything described here.

`Weekly Status Report Template.docx` is different from the other three — it isn't department-specific and isn't generated from a business-unit skill. It's converted straight from this skill's own [templates/weekly-status-report-template.md](templates/weekly-status-report-template.md), the same for every new hire regardless of department.

### File 1: Onboarding Plan.docx

Written **to the new hire, in their own voice** — this is a document they own and report from, not a file written about them. Address them directly ("you," "your") throughout the phase write-ups, the report prompts, and the tasks/meetings/introductions sections — never in the third person ("they will," "the new hire should"). The only exception is the header block immediately below, which is reference data, not narrative.

Structure exactly as follows, organized around the three onboarding phases — there is one integrated 30/60/90 track, with both "operational onboarding" section and "learning" sections. Each phase mixes the operational tasks (access, cadence, tools) and the market/category/competitive learning due in that same window. Omit a bullet only when **Role shapes the plan** says it genuinely doesn't apply — don't pad with filler to keep every section present.

**30-60-90 Onboarding Plan**

- Open with new hire name, department, role, start date, manager.
- Note the next New Hire Training date if the user provided one (or flag it TBD).

**Days 1-30**

- Platform access needed (HubSpot / Salesforce / Smartsheet / Asana / SharePoint / OneDrive / DropBox / other).
- Overview of sprint planning & reporting cadence.
- Overview of project management and tracking (tools/process the team actually uses).
- Read `Product Portfolio.docx` and `Customer.docx` in full. Cover the energy-based device (EBD) category itself — what it is, how it's regulated, how it's sold — as the umbrella category Lumenis competes in.
- If there is outside expertise (from Input), note early where it maps or doesn't map to this category — that comparison is itself useful onboarding output, not busywork.
- Closes with a day-30 checkpoint with your manager, on top of the weekly status reports you've already been sending (see **Feedback loop**).

**Days 31-60**

- Read `Competitors.docx`.
- Produce a short SWOT per Tier-1 (or otherwise role-relevant) competitor — this is work you build yourself (with guidance/review from your manager), not something handed to you pre-filled, since building it is how the learning actually happens. Don't invent one from a one-paragraph "everyone else" mental model where the source file only gives that much — those are intentionally shallow, not SWOT-ready.
- Closes with a day-60 checkpoint where you walk your manager through the SWOTs — by now your weekly status reports should already show a point of view forming, not just a summary of what was learned.

**Days 61-90**

- Draft a first marketing plan that (1) takes an explicit position on how Lumenis should shape the market and respond to it as consumer behavior and the competitive/category landscape move — not a static snapshot of where things stand today — and (2) visibly applies the expertise you came in with (see Input): name specifically how your prior background shapes this plan (a fresh angle, a channel you already know, a gap you're positioned to spot) rather than leaving "apply your skillset" implicit.
- This plan _is_ the day-90 deliverable — set a review checkpoint with your manager for it before day 90 closes out.

**Feedback loop — weekly status reports**

This track is not read-only. Every week, submit a Weekly Status Report to your manager using the template delivered as the fifth file in your onboarding folder (see **File 5: Weekly Status Report Template.docx** below) — so your progress is visible week over week, not just checked at day 30/60/90 or a final deliverable. The template has four sections:

- **What You Did** — milestones or tasks finished this week, with quantifiable results where you have them, not just narrative updates.
- **What's Blocked** — current hurdles or risks, plus the action or support you need from your manager or another stakeholder to clear them.
- **What's Next** — your top 1-3 priorities for the coming week, plus any deadlines or deliverables to watch.
- **What Surprised You** — something that didn't match your expectations this week, about the product, the market, the team, or the work itself. This is where the point-of-view-forming signal from **Key outcome** shows up in real time, week over week, instead of only every 30 days.

The day-30, day-60, and day-90 checkpoints above still stand as their own bigger milestones — the weekly report is the connective tissue between them, not a replacement for them. If the user specifies a different cadence (e.g. biweekly) or format (e.g. a live readout instead of written), use that instead of weekly — don't assume everyone wants the same rhythm.

**Tasks** — only when a resume was supplied (see Input):

A short list of specific, real tasks or stretch assignments you could plausibly take on during the 90 days, each tied to a concrete line from your resume — a named tool ("ran HubSpot workflows at [prior company]" → own a workflow audit by day 45), a channel or campaign type you've actually run, an industry/competitor adjacency, or a quantified result you've delivered before. This is the most concrete form of "applying your skillset" from **Key outcome** above, so treat it as load-bearing, not a nice-to-have list.

- Do not mention the resume in any capacity.
- Every task must trace to something actually in the resume — don't infer a capability from a job title alone (a "Marketing Manager" title doesn't itself imply SEO experience unless the resume says so), and don't pad the list to look thorough.
- Sequence by confidence, not ambition: something you've clearly done before can start earlier (even inside the first 30 days) and doesn't need heavy oversight; something adjacent to your experience but not identical belongs later, paired with a check-in.
- Keep the list short (2-5 tasks) and specific enough that you and your manager could each independently point to the resume line behind it. A vague task ("bring fresh perspective to campaigns") isn't resume-informed — it's filler wearing this section's name.
- If no resume was supplied, omit this subsection entirely rather than writing a thin version from the verbal "what they bring" answer — that input still feeds the day-90 capstone framing, just not this specific task list.

**Meetings**

- List the recurring meetings you should join.
- Always include the sales-marketing meeting, with the cadence/timing the user provided.

**Planned Introductions**

- Cap at **4 introductions per week** across the full 90-day period (roughly 13 weeks from the start date) — spread across the plan, not front-loaded into week one.
- Lay this out as a real calendar, not a phase label: compute Week 1 as the calendar week containing the start date given in Input, number the weeks sequentially through week ~13, and assign each introduction to a specific week (a table works well — Week | Week of [date] | Introduction | Category). Distribute the categories below across that span rather than clustering one category into a single week.
- **Vendors** (PR, Marketing Agency, Event Production, AV, Social) — only where role-relevant per **Role shapes the plan**.
- **Sales** — video call with a local sales rep for every hire; Regional Sales Manager / VP of Sales only where role-relevant. Schedule a ride-along with a local sales rep sometime within the 90-day window.
- **Business Unit** — Product Manager / BU personnel, per what the user specified.
- **Marketing** — calls with teammates to learn their function and the systems they use day to day.

**Key Contacts**

| Person      | Role      | For What                            |
| ----------- | --------- | ----------------------------------- |
| [Manager]   | Manager   | Day-to-day guidance                 |
| [VP Sales]  | Sales     | Questions on sales                  |
| [RSM 1]     | Sales     | Regional Sales Manager for [Region] |
| [Teammates] | Marketing | Questions, culture, navigation      |

Fill in names where the user gave them; leave the bracketed placeholder where they didn't, rather than inventing a name.

### File 5: Weekly Status Report Template.docx

A blank, reusable template — not a filled-in report for any specific week. Convert [templates/weekly-status-report-template.md](templates/weekly-status-report-template.md) as-is, keeping every bracketed placeholder (`[Date]`, `[Completed task or shipped feature]`, etc.) intact, including the `[Name]` field in the header — leave it as a placeholder rather than filling in the new hire's actual name, since this one file gets reused (copied fresh, or its fields cleared) every week for all 90 days rather than regenerated per week. If a job description or the user's own team already has a preferred weekly-status format, ask before substituting it for this one rather than assuming this template is mandatory.

### Generating the five `.docx` files

Write each file's content as clean Markdown first, then convert:

1. If `pandoc` is available (`which pandoc`), run `pandoc <file>.md -o "<file>.docx"` for each of the five.
2. Otherwise, use `python-docx` (`pip install python-docx` if not already installed) with a short script that maps headers to Word heading styles, tables to real Word tables, and bullets to Word list items for each file — don't hand back a `.docx` that's just a plain-text dump with no real formatting, and don't collapse the tables in `Product Portfolio.docx`/`Competitors.docx` into plain paragraphs.
3. Confirm all five files were created inside the named folder and tell the user its path — don't just claim success.

## Notes

- If department, role, or manager is missing, ask before drafting — the plan (and three of the five files) is genuinely different per department/role, and guessing produces a folder that has to be redone rather than lightly edited.
- Editing an existing plan: treat what's already in it (dates, names, decisions already made) as source of truth. Make the requested change to the relevant file(s); don't regenerate all five from scratch. If only `Onboarding Plan.docx` needs a change, leave the other four untouched.

---
name: asana-report
description: Produce a weekly "what happened / what's next / what's at risk" digest of Asana activity across tasks the user follows (or a named project/portfolio) — who did what in the last 7 days, the next upcoming tasks and who owns them, and which deadlines look like they're slipping. Use when the user asks for a weekly Asana status, "what changed in Asana last week," a project pulse check, or wants this run on a recurring schedule.
---

# Asana weekly digest

Turns Asana activity into a short status report: what got done last week and by whom, what's coming up next and who owns it, and which deadlines need a nudge. Built to run **unattended on a schedule** — every step below must resolve on its own from sensible defaults, without asking the user anything mid-run.

## Scope

Default: tasks the current user **follows**, workspace-wide (`followers_any=me`) — this is the natural "things I'm tracking" scope and doesn't require enumerating every project by hand. If the invocation names specific project(s)/portfolio(s) instead, scope to those (`projects_any=<gid>`) and drop the follower filter. Never stop to ask which scope to use — if nothing is specified, use the follows-based default.

## Step 1 — Define the look-back window

**Look-back window**: the 7 days ending "today" (use the actual current date, never assume). This is what "last week" means for Step 2-3.

If the user or schedule invocation specifies a different cadence (e.g. "since last Monday" for a run that slipped), honor that explicitly — otherwise always use the rolling trailing 7 days above, so a slightly-late scheduled run doesn't need gap-tracking logic.

There's no equivalent look-_ahead_ window — Step 4 ("what's next") is deliberately unbounded going forward. A fixed "due in the next 7 days" filter is too narrow in practice: it's common for nothing to be due in exactly the next week even though there's an obvious next set of deadlines a bit further out (seen firsthand — a real run returned zero "due this week" tasks while several tasks sat 2-8 weeks out with no owner-visible next-up list at all).

## Step 2 — Pull tasks with recent activity

Use `search_tasks` (Premium-only; confirmed available in this workspace) with:

- `followers_any=me` (or `projects_any=<gid>` per Scope)
- `modified_at_after=<start of look-back window, ISO 8601>`
- `completed` left unset — include both open and completed tasks; a task closed out last week is exactly the kind of thing worth reporting
- `sort_by=modified_at`, `sort_ascending=false`
- `opt_fields=name,assignee.name,completed,completed_at,due_on,modified_at,projects.name,permalink_url`
- `limit=100`

If the result count hits the limit, say so in the output rather than silently truncating, and consider re-running per-project to get full coverage.

If `search_tasks` isn't available (non-Premium workspace), fall back to `get_tasks` per project with `modified_since=<start of look-back window>` — this requires a project list first (`get_projects`), so ask which project(s) to cover only in this fallback case, since there's no follows-based equivalent for `get_tasks`.

## Step 3 — Pull what actually happened, per task

For every task Step 2 returned, call `get_task_stories` with `opt_fields=created_at,created_by.name,resource_subtype,text,type`. Filter to stories whose `created_at` falls inside the look-back window — Step 2 can surface a task that's old but had exactly one comment this week, so don't report its whole history, only the recent slice.

Turn each in-window story into one attributed digest line (`created_by.name` did what):

- `comment_added` → the comment text, trimmed to a sentence — summarize rather than quoting a long comment in full
- `assigned` → who it was (re)assigned to
- `due_date_changed` → old date → new date (also feeds Step 5's slip check)
- `marked_complete` / `marked_incomplete` → status flip
- `added_to_project` → skip unless it's the _only_ activity on the task — usually noise
- anything else without a clean human-readable summary → skip rather than guessing at what it means

Group the resulting lines by project, then by task within project.

## Step 4 — What's next

Run a second, independent `search_tasks` in the same scope: `completed=false`, `due_on_after=<today - 1 day>` (no `due_on_before` — don't bound the top end), `sort_by=due_date`, `sort_ascending=true`, `opt_fields=name,assignee.name,due_on,projects.name,permalink_url`, `limit=15`. This is the queue of what actually needs to happen next, regardless of whether it happens to fall within any particular calendar week — report the nearest ~10-15 upcoming tasks with their due date and assignee, not just whatever happens to be due in the next 7 days. Independent of Step 2 on purpose — a task due soon may not have been touched at all last week, and that's itself worth surfacing.

If the list is dominated by tasks far out (e.g. everything is 2+ months away), that's a legitimate finding too — say so rather than padding the list artificially.

## Step 5 — Flag deadline risk

Cross-reference Steps 2-4 to _flag_ items, not just list them:

- **Overdue** — run `search_tasks` with the Scope filter, `completed=false`, `due_on_before=<today>`, `due_on_after=<today - 90 days>`, `sort_by=due_date`, `sort_ascending=true`. **Do not drop the `due_on_after` bound** — a plain "overdue, not completed" query against a workspace this old returns years of dead clutter (recurring "PTO request" stub tasks, ancient webinar/email tasks with no project, tasks from 2020-2024) nobody ever intended to close out. If something genuinely important is stale-overdue beyond 90 days, it'll keep resurfacing every week rather than vanishing — the bound is about signal-to-noise, not about hiding old work. Cap the reported list (~15) with a "+N more, all older" note if it's longer.
- **Up next, gone quiet** — among the nearest few (say, top 5) tasks in Step 4, one with zero lines from Step 3 — nothing has moved on it in a week despite it being next in line.
- **Up next, unowned** — among the nearest few Step 4 tasks, one with `assignee` null.
- **Deadline slipping** — a `due_date_changed` story from Step 3 where the new date is later than the old one. Call this out explicitly in its own line rather than letting it blend into the general activity log — a quietly-slipping deadline is the main thing this digest exists to catch.

## Step 6 — Output

Produce a single report, in this shape:

```
# Asana Weekly Digest — <look-back start> to <today>

## Needs attention
- [flag type] [<task name>](<permalink>) (<project>) — <one-line why>,
  ... one line per Step 5 flag, most urgent first (overdue > slipping > gone quiet > unowned)
  If nothing was flagged, say so explicitly ("Nothing at risk this week") rather than omitting the section.

## What happened last week
### <Project name>
- **[<Task name>](<permalink>)**
  - <Person>: <what they did> (<day>)
  - ... one line per Step 3 story, chronological
... repeat per project, skip projects with zero in-window activity

## What's next
| Due | Task | Project | Assignee |
|---|---|---|---|
... one row per Step 4 task, sorted by due date ascending. If the list was capped by the limit, say "+N more beyond this list" rather than implying this is everything.
```

Keep it scannable — this is meant to be read in under a minute, not a full report. Don't add narrative summary/analysis paragraphs unless asked; the three sections above are the default output.

## Delivery (destination is decided per invocation, not hardcoded here)

This skill's job ends at producing the report above. Where it goes depends on how it's invoked:

- **Ad hoc / chat**: just return the report as the response.
- **Scheduled/unattended run**: the invocation should specify a destination. If it says to post to Asana as a Project Status Update (`create_project_status_update`), note that this posts to exactly _one_ project or portfolio GID — if Scope is the multi-project follows-based default, either post one status update per project (only for projects that had Step 3 activity or Step 5 flags) or narrow Scope to a single project/portfolio for that run. Map the report to the tool's fields: `title` = "Weekly Digest — <date>", `color` = `red` if any overdue/slipping flags exist, `yellow` if only gone-quiet/unowned flags, else `green`, `text` = the report body in plain text (or `html_text` using only its allowed tags if richer formatting is wanted).
- If no destination is specified anywhere in the invocation, default to returning the report as chat output — don't guess at posting it somewhere the user didn't ask for.

## Notes for future runs

- Never call `AskUserQuestion` mid-run — this skill is meant to run unattended on a schedule. Resolve every ambiguity via the defaults above.
- `search_tasks` requires a Premium workspace; if it starts failing where it previously worked, check that before assuming the scope/query is wrong.
- A story's `resource_subtype` set may grow over time (Asana adds new activity types) — if an unfamiliar one shows up with a usable `text`/summary field, include it rather than dropping it; only skip when there's genuinely nothing human-readable to report.

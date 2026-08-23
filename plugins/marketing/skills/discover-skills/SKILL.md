---
name: discover-skills
description: Analyze a claude.ai conversation export to find repeatable usage patterns, then propose (and optionally build) new skills or updates to existing ones for this repo. Use when the user wants to "figure out what skills to build," "analyze my Claude usage," "what should I turn into a skill," or otherwise wants this skill library grown from real usage rather than guesswork. Produces a category breakdown and a ranked skill shortlist as an actual markdown file, not just a chat summary. Work-scope only — never surfaces or builds skills from personal/non-work usage.
---

# Discover skills from usage

Turns a person's real claude.ai conversation history into: (1) a breakdown of what they actually use Claude for, (2) a ranked shortlist of repeatable patterns worth turning into skills, and (3) optionally, the skills themselves — grounded in real past conversations rather than generic best-guess structure.

**This is a work skill library.** Personal/non-work usage never becomes a skill suggestion here, regardless of how frequent or high-leverage it looks in the data — see the hard rule in Step 4.

## What the user needs to do first

This skill needs the person's own claude.ai data export — there's no API for this, so walk them through it rather than assuming they have it:

1. Go to claude.ai → **Settings → Account → Export data**, and request the export. It takes roughly 24 hours to generate.
2. When it's ready, they'll get an email/notification with a **manifest** — a JSON file listing several one-time-use download URLs (typically `conversations`, `light_metadata`, `projects`, and sometimes `design_chats`). Each URL only works once and requires an authenticated browser session — it cannot be fetched programmatically (Cloudflare will block a bare `curl`/script request). Ask the user to open each relevant URL in their browser and save the resulting zip(s) somewhere you can read them.
3. At minimum you need `conversations-*.zip` (contains `conversations.json`, the full message history) — `light_metadata` and `projects` are optional/supplementary, `design_chats` is usually not needed for this analysis.
4. Treat the manifest file and the raw zips as sensitive — they contain the account holder's private conversation history and one-time auth-bearing URLs. Extract them into a scratchpad/temp location, never into the repo working tree, and delete the manifest/zips once extracted so single-use links and raw exports don't linger in the project directory or get committed.

## Step 1 — Ingest & parse

Unzip `conversations.json` and normalize into one row per conversation: `id, created_at, title, message_count, human_message_count, full_text` (concatenated human turns — that's usually enough signal to categorize and find patterns without needing assistant text). Filter out trivial/empty threads (e.g. a single short human turn under ~40 characters) so they don't skew percentages.

## Step 2 — Categorize

Draft a candidate taxonomy from a first skim of titles/snippets — don't reuse a fixed taxonomy from a prior run, since it should reflect what this person actually does. Categorize every conversation into one primary category; for a large corpus (100+), delegate the read-and-classify pass to a subagent (or several, chunked) rather than doing it in the main context — this is high-volume, low-judgment-per-item work that otherwise burns a lot of context for little benefit. Spot-check a sample and fix miscategorizations (a common failure mode: classifying by topic/subject matter instead of by task type — e.g. an email about compensation should be categorized as email drafting, not HR strategy, if the actual ask was "help me word this").

## Step 3 — Produce the breakdown, and write it to a file

Count conversations per category, % of total, and cut a second way by recency (e.g. last 30/90 days vs. all-time) to see if usage is shifting. Show this in chat, **and** write it to an actual markdown file — don't only display it inline. Structure:

```
# Claude Usage Analysis — [date]

## Category breakdown
| Category | Count | % of total | Count (last 90d) | % of last 90d |
|---|---|---|---|---|
...

## Notable shifts
[recency changes worth calling out]

## Skill candidates
[ranked shortlist — see Step 4]
```

**Where to save it**: this file contains a real breakdown of someone's private usage — don't default to committing it into this (likely public) repo. Save it to the user's scratchpad/local filesystem and tell them the path; only add it to the repo if they explicitly ask, and if so, run the same sensitivity check as [propose-plugin-change](../../../../.claude/skills/propose-plugin-change) before doing so.

## Step 4 — Surface skill candidates

**Hard rule: never propose a skill for personal/non-work usage, no matter how frequent or high-leverage the pattern is.** This is a work skill library — categories like personal admin, individual career/job-search activity, family/personal correspondence, or other non-Lumenis-work usage are out of scope entirely. Don't rank them, don't mention them as "a candidate we're choosing not to build," don't include them in the shortlist even with a caveat — exclude them from Step 4 outright. (They can still appear in the Step 3 category breakdown by name/count, since that's just usage transparency — the line is at *suggesting or building* something from them.) If a category is ambiguous (e.g. it mixes work and personal use), split it further rather than defaulting it in.

For each remaining, work-relevant category, starting with the largest by %:

1. Pull 5-10 representative conversations (mix of recent and older).
2. Look for a repeated *shape*: same kind of input → same kind of output, recurring more than a couple times, structured enough to templatize.
3. **Check this repo's existing skills first** (read the `SKILL.md` frontmatter `description` under each `plugins/*/skills/*/`) — don't propose rebuilding something that already exists; instead note whether an existing skill should be *extended* rather than a new one created.
4. Rank remaining candidates by frequency × leverage (how much manual context-setting Claude currently has to redo each time — tone, format, structure, persona).
5. Drop one-off/bespoke requests even from a large category — skills are for repeatable patterns, not raw volume. Say so explicitly rather than forcing a candidate out of a category that doesn't have one.

Report the ranked shortlist to the user and get their sign-off on which to build before proceeding — this is a judgment call about what's worth the repo's maintenance surface, not a decision to make unilaterally.

## Step 5 — Build or update the chosen skill(s)

This is the step where grounding in real history matters most — a skill built from generic assumptions about "what a KOL email probably needs" is measurably worse than one built from what this person actually asked for and corrected, repeatedly, in their real drafts. If a candidate reaching this step turns out to be personal/non-work after all (something Step 4 should have already caught), stop and drop it rather than building it. For each skill being built or updated:

1. Pull the full text (both human asks *and* assistant responses where available) of the representative conversations identified in Step 4 — not just titles/snippets.
2. Extract concrete, evidenced patterns: what did they actually emphasize, what tone corrections did they make repeatedly (quote or closely paraphrase the literal asks — "make it less robotic," "soften without being accusatory" are stronger signal than an assumed tone), what structure did the output actually take.
3. Write the skill (or the update) grounded in that evidence, following this repo's existing house pattern (frontmatter description with trigger phrases, then instructions — see any file under `plugins/marketing/skills/` or `plugins/core/skills/` for the shape).
4. **Sensitivity check before writing anything to the repo**: real conversation history can surface named individuals, compensation figures, health/personal details, or other content that shouldn't land in what may be a public repo. Generalize — carry over the *pattern* (e.g. "wants continuity spelled out concretely after a departure") without the *specifics* (names, figures, incidents). If it's unclear whether something is safe to generalize-and-include, say so and ask rather than guessing.
5. Validate by re-running the new/updated skill against one of the source conversations' original input and comparing output quality to what actually happened.
6. Ship via [propose-plugin-change](../../../../.claude/skills/propose-plugin-change) — split into separate PRs by feature area if multiple unrelated skills changed, one PR if they're tightly coupled (e.g. a skill and the shared reference file it depends on).

## Notes

- This is a periodic/occasional skill, not something to run on every session — re-run it every so often (e.g. quarterly, or when usage patterns feel like they've shifted) rather than treating one analysis as permanent.
- If the export is old or a prior analysis exists, prefer fresh data — usage patterns shift (a category that was dominant six months ago may be dormant now, and vice versa) — and say so if a proposed skill's underlying pattern looks stale in the new data.

## Platform notes

Steps 1-4 (ingest, categorize, breakdown + shortlist) need file/code execution but not repo or git access — they can run wherever that's available. Steps 5-6 (writing skill files into this repo, committing, opening a PR) need a real working tree plus `git`/`gh` — that's Claude Code only (CLI, VS Code extension, or desktop with repo access).

- **Claude Code** (this repo checked out locally): the full pipeline runs as written above, including shipping a PR via [propose-plugin-change](../../../../.claude/skills/propose-plugin-change).
- **claude.ai / Claude Desktop without a filesystem+git MCP connection**: no access to this repo's working tree, no `git`/`gh`, and no equivalent to the `Agent` tool for offloading a large classification pass. Steps 1-4 still work — the user uploads the export zip(s) directly into the chat, and the code-execution tool does the unzip/parse/categorize/breakdown. Adjust the deliverable accordingly:
  - Output the breakdown, shifts, and ranked shortlist (Step 3-4) as **plain markdown text in the reply**, not a file — there's no shared filesystem to save it to or point the user at.
  - For Step 5 (build/update), draft the proposed skill content as plain markdown in the reply too — frontmatter, instructions, the same house pattern — since there's nothing to commit to.
  - In place of Step 6 (opening a PR), point the user to the repo's GitHub Issues page (`https://github.com/laarnicayetano/lumenis-ai/issues/new`) to file the proposed skill content as an issue, or tell them to paste it into a Claude Code session so it can actually be committed and shipped from there. Don't imply a PR was opened — it wasn't, and can't be, from this platform.
- **Claude Desktop with an MCP filesystem/git server connected**: capability depends on what that server exposes — closer to Code's ceiling, but not guaranteed to include everything (e.g. `gh` for PRs specifically); check what's actually wired up rather than assuming.

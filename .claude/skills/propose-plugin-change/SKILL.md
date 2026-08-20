---
name: propose-plugin-change
description: Publish edits made in this repo (lumenis-ai) by opening a GitHub PR with a suggested version-bump label. Use when the user says "ship this", "publish this change", "release this", "open a PR", or has finished editing a skill and wants it live. This is a repo-local skill for maintaining lumenis-ai itself — not something distributed to plugin installers.
---

# Propose a Lumenis plugin change

The person invoking this is often not a developer (e.g. a marketer editing a
skill's wording or examples). Do the git work for them — don't ask them to
run commands themselves unless something is genuinely ambiguous. This skill
opens a PR for human review; it never pushes straight to `master`. Version
bumping, zip rebuilding, and publishing a GitHub Release happen automatically
via `.github/workflows/version-bump.yml` once the PR is merged — this skill
does not run `bump_version.py` or `build_zips.py` itself.

## Steps

1. **See what changed.** Run `git status` and `git diff` (or `git diff --staged`
   if things are already staged) to see which files changed.

2. **Check for sensitive content before doing anything else.** This repo is
   public — read the actual diff content (not just filenames) and look for:
   - API keys, tokens, passwords, or credentials (e.g. `sk-`, `AKIA`, `-----BEGIN
     PRIVATE KEY-----`, bearer tokens, `.env`-style `KEY=value` secrets)
   - Real customer/personal data (names + emails, phone numbers, addresses,
     account IDs) rather than placeholder/example data
   - Internal-only material that reads as confidential (unreleased pricing,
     unannounced product names, internal strategy docs, financial figures)

   If you find any of this, **stop — do not commit, push, or open a PR.**
   Tell the user plainly what you found and where, and let them decide
   whether to remove it or confirm it's safe to publish. Don't guess or
   silently redact; a false positive costs one clarifying question, a false
   negative publishes a leak.

3. **Map changes to plugin(s).** Any changed file under `plugins/<name>/`
   affects that plugin. Ignore changes outside `plugins/` (e.g. README edits)
   for bump-level purposes, but still include them in the PR.

4. **Pick one suggested bump level for the whole PR.** Default to **patch**.
   Use your judgment on the diff, and don't ask unless it's genuinely
   unclear:
   - **none** — nothing under `plugins/` changed (docs, workflow, repo
     tooling only)
   - **patch** — wording tweaks, corrections, small examples, bug fixes
   - **minor** — a new skill added, a new capability, a meaningfully expanded
     skill
   - **major** — a skill removed or renamed in a way that breaks existing
     references, restructured plugin layout
   If truly ambiguous, ask the user in one short sentence rather than
   guessing on a major bump. If a single PR touches multiple plugins, this
   one level applies to all of them — split into separate PRs first if they
   genuinely need different bump levels.

5. **Create a branch and commit.**
   ```
   git checkout -b claude/<short-slug>
   git add <changed files>
   git commit -m "<plain-language summary of the change>"
   git push -u origin claude/<short-slug>
   ```
   Do not touch `plugin.json` or run the version scripts — that happens
   automatically after merge.

6. **Open the PR** with the bump label attached:
   ```
   gh pr create --title "<summary>" --body "<what changed and why>" \
     --label "bump:<level>"
   ```
   (Labels `bump:none` / `bump:patch` / `bump:minor` / `bump:major` already
   exist on the repo.)

7. **Report back in plain language**, e.g.:
   > Opened a PR: <url>. I've labeled it `bump:patch`, but you (or a
   > reviewer) can change the label before merging if a different bump makes
   > more sense. Once it's merged, the version bump and a GitHub Release with
   > the new zip happen automatically.

## Notes

- Never invent content changes — only publish what the user actually edited.
- If nothing changed at all, say so rather than opening an empty PR.
- This skill's job ends at opening the PR. Merging, approving, and the
  resulting version bump are handled by a human + CI, not by this skill.

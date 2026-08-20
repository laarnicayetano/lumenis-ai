---
name: release-plugin
description: Publish edits made in this repo (lumenis-ai) — bump the right plugin version(s), rebuild the zips, commit, and push. Use when the user says "ship this", "publish this change", "release this", "update the marketplace", or has finished editing a skill and wants it live. This is a repo-local skill for maintaining lumenis-ai itself — not something distributed to plugin installers.
---

# Release a Lumenis plugin change

The person invoking this is often not a developer (e.g. a marketer editing a
skill's wording or examples). Do the git/versioning work for them — don't ask
them to run commands themselves unless something is genuinely ambiguous.

## Steps

1. **See what changed.** Run `git status` and `git diff` (or `git diff --staged`
   if things are already staged) to see which files changed.

2. **Map changes to plugin(s).** Any changed file under `plugins/<name>/`
   affects that plugin. A single edit can affect multiple plugins — handle
   each independently. Ignore changes outside `plugins/` (e.g. README edits)
   for versioning purposes, but still include them in the commit.

3. **Pick a version bump per affected plugin.** Default to **patch**. Use
   your judgment on the diff, and don't ask unless it's genuinely unclear:
   - **patch** — wording tweaks, corrections, small examples, bug fixes
   - **minor** — a new skill added, a new capability, a meaningfully expanded
     skill
   - **major** — a skill removed or renamed in a way that breaks existing
     references, restructured plugin layout
     If truly ambiguous, ask the user in one short sentence rather than
     guessing on a major bump.

4. **Bump each affected plugin:**

   ```
   python3 scripts/bump_version.py <plugin-name> <patch|minor|major>
   ```

5. **Rebuild the zips:**

   ```
   python3 scripts/build_zips.py
   ```

6. **Commit.** Stage the changed source files plus the bumped `plugin.json`
   file(s) (not `dist/`, which is gitignored). Write a plain-language commit
   message describing what changed, e.g.:
   `core: v0.2.0 — clarified brand voice guidelines`
   For multiple plugins in one change, one commit is fine; mention each
   plugin and its new version in the message.

7. **Push** to `origin` on the current branch.

8. **Report back in plain language**, e.g.:
   > Published `core` v0.2.0. If anyone's on an individual plan (not Claude
   > Code), send them `dist/core-v0.2.0.zip` to re-upload in Customize →
   > Plugins.

## Notes

- If nothing under `plugins/` changed, there's nothing to version — just
  mention that plainly rather than bumping anyway.
- Never invent content changes — only version and publish what the user
  actually edited.
- This repo is public (see README's Privacy section) — never commit secrets,
  API keys, or internal-only material while doing this.

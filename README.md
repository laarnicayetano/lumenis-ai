# Lumenis AI

Shared Lumenis skills, organized as a plugin marketplace.

## Plugins

| Plugin      | Install                | Description                                                                                |
| ----------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| `core`      | `core@lumenis-ai`      | Brand context, global design system, per-product context/design skills. **Install first.** |
| `marketing` | `marketing@lumenis-ai` | Positioning, new-product generator, image/HubSpot workflows.                               |

## Installing

**claude.ai / Desktop / Cowork (individual plans):** Download each plugin's zip file
from [releases page](../../releases) and upload them in Customize → Plugins → "+" →
upload a plugin file.

**Claude Code (git access required):**

```
/plugin marketplace add laarnicayetano/lumenis-ai
/plugin install core@lumenis-ai
/plugin install marketing@lumenis-ai
```

## Making a change (with Claude Code)

If you're working in this repo with Claude Code, just edit the skill file(s)
you want to change, then tell Claude **"ship this"** (or "publish this
change"). A repo-local skill
([.claude/skills/propose-plugin-change](.claude/skills/propose-plugin-change/SKILL.md))
opens a GitHub PR for you, labeled with a suggested version bump
(`bump:patch` / `bump:minor` / `bump:major` / `bump:none`). You don't need to
know git or semantic versioning.

A reviewer checks the PR (and can change the bump label if needed), then
merges it. Once merged, `.github/workflows/version-bump.yml` automatically
bumps the affected plugin's `plugin.json`, rebuilds its zip, and publishes a
GitHub Release with the zip attached — nothing manual to do after approval.

Each plugin's `plugin.json` description leads with its version (e.g. "v0.2.0 —
..."), so anyone can check their installed version against the latest by
comparing what's in Customize → Plugins to the [releases page](../../releases)
or this repo.

If you're on an individual plan (not Claude Code), grab the zip from the
plugin's [GitHub Release](../../releases) and send it to people to re-upload
in Customize → Plugins.

## Privacy

The repo is public, so `plugin.json` and everything under `plugins/` is
world-readable. Since everything is public we should take special care NOT to add sensitive material.

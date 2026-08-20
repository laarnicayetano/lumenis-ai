# lumenis-ai

Shared Lumenis skills, organized as a plugin marketplace.

## Plugins

| Plugin      | Install                | Description                                                                                |
| ----------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| `core`      | `core@lumenis-ai`      | Brand context, global design system, per-product context/design skills. **Install first.** |
| `marketing` | `marketing@lumenis-ai` | Positioning, new-product generator, image/HubSpot workflows, version checker.              |

## Installing

**claude.ai / Desktop / Cowork (individual plans):** distribute the built zips
from `dist/` and have each person upload them in Customize → Plugins → "+" →
upload a plugin file.

**Claude Code (git access required):**

```
/plugin marketplace add laarnicayetano/lumenis-ai
/plugin install core@lumenis-ai
/plugin install marketing@lumenis-ai
```

## Making a change (no git/CLI knowledge needed)

If you're working in this repo with Claude Code, just edit the skill file(s)
you want to change, then tell Claude **"ship this"** (or "publish this
change"). A repo-local skill
([.claude/skills/release-lumenis-plugin](.claude/skills/release-lumenis-plugin/SKILL.md))
takes it from there: it figures out which plugin(s) you touched, bumps the
version automatically, rebuilds the zips, and commits + pushes for you. You
don't need to know git, semantic versioning, or the scripts below.

Anyone can ask Claude "am I on the latest plugins?" to check they're current.

If you're on an individual plan (not Claude Code), Claude will tell you which
zip in `dist/` to redistribute after publishing — send that to people to
re-upload in Customize → Plugins.

### Manual steps (what the skill does under the hood)

1. Edit the skill(s).
2. Bump the plugin version: `python3 scripts/bump_version.py core minor`
3. Rebuild zips: `python3 scripts/build_zips.py`
4. Commit and push `plugin.json` — the version-check skill reads it straight
   from GitHub, so pushing is what makes the new version visible.
5. Redistribute the changed zip from `dist/`; people re-upload it.

## Adding a product

Ask (with the `marketing` plugin installed): "set up a skill for a new
product." The `new-product-skill` generator writes a context + design skill
pair into `core/skills/product-<slug>/`, matching `product-example`. Then say
"ship this" to publish it.

## Privacy

The repo is public, so the version-check skill reads each plugin's
`plugin.json` straight from GitHub. Since everything is public we should take special care NOT to add sensitive material.

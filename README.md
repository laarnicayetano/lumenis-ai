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

## Updating (individual plans — manual)

1. Edit the skill(s).
2. Bump the plugin version: `python scripts/bump_version.py core minor`
3. Rebuild zips: `python scripts/build_zips.py`
4. Commit and push `plugin.json` — the version-check skill reads it straight
   from GitHub, so pushing is what makes the new version visible.
5. Redistribute the changed zip from `dist/`; people re-upload it.

Anyone can ask Claude "am I on the latest plugins?" to check.

## Adding a product

Ask (with the `marketing` plugin installed): "set up a skill for a new
product." The `new-product-skill` generator writes a context + design skill
pair into `core/skills/product-<slug>/`, matching `product-example`. Then bump
core, rebuild, redistribute.

## Privacy

The repo is public, so the version-check skill reads each plugin's
`plugin.json` straight from GitHub. If this repo goes private later, that
skill will need read access to still work — see `plugins/marketing/skills/version-check/SKILL.md`.

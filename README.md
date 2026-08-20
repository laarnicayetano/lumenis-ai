# lumenis-ai

Shared Lumenis skills for Claude, organized as a plugin marketplace.

## Plugins

| Plugin      | Install                | What it gives Claude                                                                       |
| ----------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| `core`      | `core@lumenis-ai`      | Brand context, global design system, per-product context/design skills. **Install first.** |
| `marketing` | `marketing@lumenis-ai` | Positioning, new-product generator, image/HubSpot workflows, version checker.              |

## Installing

**claude.ai / Desktop / Cowork (individual plans):** distribute the built zips
from `dist/` and have each person upload them in Customize → Plugins → "+" →
upload a plugin file.

**Claude Code (git access required):**

```
/plugin marketplace add <owner>/lumenis-ai
/plugin install core@lumenis-ai
/plugin install marketing@lumenis-ai
```

## Updating (individual plans — manual)

1. Edit the skill(s).
2. Bump the plugin version: `python scripts/bump_version.py core minor`
3. Rebuild zips: `python scripts/build_zips.py`
4. Redistribute the changed zip from `dist/`; people re-upload it.
5. Push `dist/VERSIONS.json` to wherever `LATEST_MANIFEST_URL` points so the
   version-check skill can see the new latest.

Anyone can ask Claude "am I on the latest Lumenis plugins?" to check.

## Adding a product

Ask Claude (with the `marketing` plugin installed): "set up a skill for a new
product." The `new-product-skill` generator writes a context + design skill
pair into `core/skills/product-<slug>/`, matching `product-example`. Then bump
core, rebuild, redistribute.

## Privacy

Repo can be private. `dist/VERSIONS.json` holds only plugin names + version
numbers and may be published (e.g. a public Gist) so the version-check skill can
read it without exposing the private content.

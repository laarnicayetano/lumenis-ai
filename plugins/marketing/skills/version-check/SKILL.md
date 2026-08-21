---
name: lumenis-version-check
description: Check whether the installed Lumenis plugins are up to date. Use when the user asks "am I on the latest version", "is my Lumenis plugin current", "check for plugin updates", or mentions their skills seeming out of date. Compares the installed plugin's plugin.json against the plugin.json on GitHub.
---

# Lumenis version check

Tells the user whether their installed Lumenis plugins match the latest
published versions.

## How versions are tracked

Each plugin's version lives in its own `.claude-plugin/plugin.json`, both in
the installed copy and in the repo (public:
`https://github.com/laarnicayetano/lumenis-ai`).

- Installed version: read `version` from the installed plugin's
  `.claude-plugin/plugin.json`.
- Latest version: fetch each plugin's `plugin.json` directly, e.g.:

  `https://raw.githubusercontent.com/laarnicayetano/lumenis-ai/master/plugins/<plugin-name>/.claude-plugin/plugin.json`

## What to do when invoked

1. For each installed Lumenis plugin, read `version` from its
   `.claude-plugin/plugin.json`.
2. Fetch that plugin's `plugin.json` from the URL above (substitute the
   plugin's name) and read its `version` field.
3. Compare each installed version against the fetched latest version.
4. Report clearly:
   - Up to date: "core is current (v0.3.0)."
   - Behind: "core is v0.2.0 — latest is v0.3.0. Ask the maintainer for the new
     zip, then re-upload it in Customize -> Plugins."
5. If a plugin.json URL can't be reached, say so plainly and tell the user to
   check with the plugin maintainer — do not guess.

## Notes

- Can't force an update; on individual plans updates are manual re-uploads.

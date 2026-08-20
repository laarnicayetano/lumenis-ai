---
name: lumenis-version-check
description: Check whether the installed Lumenis plugins are up to date. Use when the user asks "am I on the latest version", "is my Lumenis plugin current", "check for plugin updates", or mentions their skills seeming out of date. Compares the VERSION file shipped inside each installed plugin against the published VERSIONS.json manifest.
---

# Lumenis version check

Tells the user whether their installed Lumenis plugins match the latest
published versions.

## How versions are tracked

Each plugin ships a `VERSION` file (written by scripts/build_zips.py) recording
the version it was built at. Latest versions for every plugin are published in a
single manifest, `VERSIONS.json`.

- Installed version: read the `VERSION` file inside each installed plugin.
- Latest version: fetch the published manifest at:

  `LATEST_MANIFEST_URL` <!-- replace with your raw manifest URL, e.g.
       https://raw.githubusercontent.com/laarnicayetano/lumenis-claude/main/dist/VERSIONS.json
       This one small file may be public even if the repo is private; it holds
       only plugin names and version numbers. -->

## What to do when invoked

1. For each installed Lumenis plugin, read its `VERSION` file (name + version).
2. Fetch the latest manifest from `LATEST_MANIFEST_URL`.
3. Compare each installed version against `latest[name]`.
4. Report clearly:
   - Up to date: "core is current (v0.3.0)."
   - Behind: "core is v0.2.0 — latest is v0.3.0. Ask the maintainer for the new
     zip, then re-upload it in Customize -> Plugins."
5. If the manifest URL can't be reached, say so plainly and tell the user to
   check with the plugin maintainer — do not guess.

## Notes

- Can't force an update; on individual plans updates are manual re-uploads.
- If no `VERSION` file is found, the plugin predates versioning — recommend
  re-installing the latest zip.

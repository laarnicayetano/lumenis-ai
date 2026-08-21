#!/usr/bin/env python3
"""
Bump a plugin's semantic version in its plugin.json.
Usage: python scripts/bump_version.py <plugin-name> [patch|minor|major]
Defaults to patch. Run build_zips.py afterward.
"""
import json, re, sys
from pathlib import Path

VERSION_PREFIX = re.compile(r"^v\d+\.\d+\.\d+ — ")

def bump(version, part):
    major, minor, patch = (int(x) for x in version.split("."))
    if part == "major": return f"{major+1}.0.0"
    if part == "minor": return f"{major}.{minor+1}.0"
    return f"{major}.{minor}.{patch+1}"

def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: bump_version.py <plugin-name> [patch|minor|major]")
    name = sys.argv[1]
    part = sys.argv[2] if len(sys.argv) > 2 else "patch"
    manifest = Path("plugins") / name / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        raise SystemExit(f"Not found: {manifest}")
    data = json.loads(manifest.read_text())
    old = data["version"]; data["version"] = bump(old, part)
    data["description"] = VERSION_PREFIX.sub(
        f"v{data['version']} — ", data["description"], count=1
    )
    manifest.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{name}: {old} -> {data['version']}\nNow run: python scripts/build_zips.py")

if __name__ == "__main__":
    main()

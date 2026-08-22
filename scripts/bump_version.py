#!/usr/bin/env python3
"""
Bump a plugin's semantic version in its plugin.json.
Usage: python scripts/bump_version.py <plugin-name> [patch|minor|major]
Defaults to patch. Run build_zips.py afterward.
"""
import json, re, sys
from pathlib import Path

VERSION_PREFIX = re.compile(r"^v\d+\.\d+\.\d+ — ")
VERSION_SUFFIX = re.compile(r" v\d+\.\d+\.\d+$")

def bump(version, part):
    major, minor, patch = (int(x) for x in version.split("."))
    if part == "major": return f"{major+1}.0.0"
    if part == "minor": return f"{major}.{minor+1}.0"
    return f"{major}.{minor}.{patch+1}"

def set_version_prefix(description, version):
    stripped = VERSION_PREFIX.sub("", description, count=1)
    return f"v{version} — {stripped}"

def title_case(name):
    return " ".join(word.capitalize() for word in name.split("-"))

def set_version_suffix(display_name, version):
    stripped = VERSION_SUFFIX.sub("", display_name, count=1)
    return f"{stripped} v{version}"

def update_marketplace_entry(name, version):
    marketplace_path = Path(".claude-plugin") / "marketplace.json"
    if not marketplace_path.exists():
        return
    data = json.loads(marketplace_path.read_text())
    for entry in data.get("plugins", []):
        if entry.get("name") == name:
            entry["description"] = set_version_prefix(entry["description"], version)
            entry["displayName"] = set_version_suffix(
                entry.get("displayName", title_case(name)), version
            )
            break
    marketplace_path.write_text(json.dumps(data, indent=2) + "\n")

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
    data["description"] = set_version_prefix(data["description"], data["version"])
    manifest.write_text(json.dumps(data, indent=2) + "\n")
    update_marketplace_entry(name, data["version"])
    print(f"{name}: {old} -> {data['version']}\nNow run: python scripts/build_zips.py")

if __name__ == "__main__":
    main()

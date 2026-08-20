#!/usr/bin/env python3
"""
Build distributable plugin zips for the lumenis-claude marketplace.

For each plugin under plugins/, this:
  1. reads version from its .claude-plugin/plugin.json
  2. writes a VERSION file into the plugin (installed copy carries its version)
  3. zips it to dist/<name>-v<version>.zip
  4. writes dist/VERSIONS.json — the "latest version" manifest the
     version-check skill reads.

Usage: python scripts/build_zips.py [--repo-root .] [--out dist]
No third-party dependencies.
"""
import argparse, json, zipfile
from datetime import date
from pathlib import Path

def load_plugin_version(plugin_dir):
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text())
    name, version = data.get("name"), data.get("version")
    if not name or not version:
        raise ValueError(f"{manifest} missing 'name' or 'version'")
    return name, version

def stamp_version_file(plugin_dir, name, version):
    stamp = {"name": name, "version": version, "built": date.today().isoformat()}
    (plugin_dir / "VERSION").write_text(json.dumps(stamp, indent=2) + "\n")

def zip_plugin(plugin_dir, name, version, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{name}-v{version}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(plugin_dir.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(plugin_dir.parent))
    return zip_path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    plugins_dir = root / "plugins"
    out_dir = root / args.out
    if not plugins_dir.is_dir():
        raise SystemExit(f"No plugins/ dir at {plugins_dir}")
    versions, built = {}, []
    for plugin_dir in sorted(p for p in plugins_dir.iterdir() if p.is_dir()):
        if not (plugin_dir / ".claude-plugin" / "plugin.json").exists():
            print(f"skip (no manifest): {plugin_dir.name}"); continue
        name, version = load_plugin_version(plugin_dir)
        stamp_version_file(plugin_dir, name, version)
        zip_path = zip_plugin(plugin_dir, name, version, out_dir)
        versions[name] = version
        built.append((name, version, zip_path.name))
        print(f"built {zip_path.name}")
    (out_dir / "VERSIONS.json").write_text(json.dumps(
        {"marketplace": "lumenis-claude", "generated": date.today().isoformat(),
         "latest": versions}, indent=2) + "\n")
    print(f"\nwrote {out_dir / 'VERSIONS.json'}\n\nSummary:")
    for name, version, fname in built:
        print(f"  {name:24} v{version:8} -> {fname}")

if __name__ == "__main__":
    main()

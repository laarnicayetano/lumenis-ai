---
name: image-webp
description: Convert images (PNG, JPG) to responsive WebP derivatives (640w/1280w/1920w) using the bundled converter. Use when the user wants to create .webp files, optimize images for web, or batch-convert a folder of images. Runs the bundled converter script.
---

# Image → WebP converter

## Usage
```
python scripts/convert.py <input_path> [output_dir] [--quality 82]
```
- `<input_path>`: a single image file or a directory (converts every PNG/JPG found, recursively).
- `[output_dir]`: optional; defaults alongside the source.
- `--quality`: 0–100, default 82.

Each source image produces up to three files: `<name>-640w.webp`,
`<name>-1280w.webp`, `<name>-1920w.webp`. Widths wider than the source are
skipped (never upscaled), so a narrower source produces fewer, smaller
outputs.

## Notes
- Requires Pillow (`pip install Pillow`); the script reports if missing.
- Skips input files already in .webp.
- Honors EXIF orientation (auto-rotates) before resizing.
- Strips embedded source metadata — output files carry no EXIF.
- Skips regenerating an output file that already exists at that width.

---
name: image-webp
description: Convert images (PNG, JPG) to WebP format using the bundled converter. Use when the user wants to create .webp files, optimize images for web, or batch-convert a folder of images. Runs the bundled converter script.
---

# Image → WebP converter

## Usage
```
python scripts/convert.py <input_path> [output_dir] [--quality 80]
```
- `<input_path>`: a single image file or a directory.
- `[output_dir]`: optional; defaults alongside the source.
- `--quality`: 0–100, default 80.

## Notes
- Requires Pillow (`pip install Pillow`); the script reports if missing.
- Skips files already in .webp.

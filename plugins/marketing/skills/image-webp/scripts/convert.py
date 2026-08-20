#!/usr/bin/env python3
"""Convert PNG/JPG images to WebP. Placeholder — replace with Nicholas's version."""
import sys, argparse
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Convert images to WebP")
    p.add_argument("input_path")
    p.add_argument("output_dir", nargs="?", default=None)
    p.add_argument("--quality", type=int, default=80)
    args = p.parse_args()
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow is required. Install with: pip install Pillow")
    src = Path(args.input_path)
    exts = {".png", ".jpg", ".jpeg"}
    files = [src] if src.is_file() else [f for f in src.rglob("*") if f.suffix.lower() in exts]
    if not files:
        sys.exit(f"No images found at {src}")
    for f in files:
        if f.suffix.lower() == ".webp":
            continue
        out_dir = Path(args.output_dir) if args.output_dir else f.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / (f.stem + ".webp")
        Image.open(f).save(out, "WEBP", quality=args.quality)
        print(f"{f} -> {out}")

if __name__ == "__main__":
    main()

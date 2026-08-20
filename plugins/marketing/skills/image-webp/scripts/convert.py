#!/usr/bin/env python3
"""Convert PNG/JPG images to WebP at responsive widths (640/1280/1920)."""
import sys, argparse
from pathlib import Path

WIDTHS = (640, 1280, 1920)

def main():
    p = argparse.ArgumentParser(description="Convert images to WebP at 640w/1280w/1920w")
    p.add_argument("input_path")
    p.add_argument("output_dir", nargs="?", default=None)
    p.add_argument("--quality", type=int, default=82)
    args = p.parse_args()
    try:
        from PIL import Image, ImageOps
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

        with Image.open(f) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if image.mode in ("P", "LA") else "RGB")
            source_width, source_height = image.size
            widths = sorted({min(w, source_width) for w in WIDTHS})
            for width in widths:
                out = out_dir / f"{f.stem}-{width}w.webp"
                if out.exists():
                    print(f"{f} -> {out} (skipped, already exists)")
                    continue
                if width == source_width:
                    resized = image
                else:
                    height = round(source_height * width / source_width)
                    resized = image.resize((width, height), Image.LANCZOS)
                resized.save(out, "WEBP", quality=args.quality, method=5)
                print(f"{f} -> {out}")

if __name__ == "__main__":
    main()

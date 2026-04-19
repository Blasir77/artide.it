"""Compress images in preview/assets/img to webp ≤1200px wide for preview only.

Original sources remain untouched in _source/; this only affects preview.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "preview/assets/img"

MAX_WIDTH = 1200
QUALITY = 78

def convert(p: Path):
    try:
        im = Image.open(p)
    except Exception as e:
        print(f"!! cannot open {p.name}: {e}")
        return

    # Keep transparency if the source has it (logos are white-on-transparent —
    # flattening onto a white background makes them vanish).
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    if has_alpha:
        im = im.convert("RGBA")
    elif im.mode != "RGB":
        im = im.convert("RGB")

    w, h = im.size
    if w > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, int(h * MAX_WIDTH / w)), Image.LANCZOS)
    dest = p.with_suffix(".webp")
    im.save(dest, "WEBP", quality=QUALITY, method=4, lossless=False)
    if dest != p:
        p.unlink()

def main():
    files = [p for p in IMG_DIR.iterdir() if p.is_file() and p.suffix.lower() != ".ico"]
    files.sort(key=lambda p: -p.stat().st_size)
    before = sum(p.stat().st_size for p in files)
    print(f"Compressing {len(files)} images (starting from {before/1024/1024:.1f} MB)…")
    for p in files:
        convert(p)
    after = sum(p.stat().st_size for p in IMG_DIR.iterdir() if p.is_file() and p.suffix.lower() != ".ico")
    print(f"Done. Before {before/1024/1024:.1f} MB → After {after/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()

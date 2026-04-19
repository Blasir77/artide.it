"""Collect and dedupe media assets for preview.

For each image ID directory (e.g. 200000011-90bdd90be0), select a single variant
(preferring 700px webp, falling back to 450 or full), and copy it under
preview/assets/img/<id>.<ext>. Also emit build/media_map.json mapping the
original HTML paths (like "67be54ee.../200000011-90bdd90be0/450/logo.webp?ph=X")
to the final preview path.
"""
import json
import re
import shutil
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
IMG_ROOT = ROOT / "_source/extracted/www.artide.it/67be54ee7dfaae1e955c05a76e69ace8"
OUT_DIR = ROOT / "preview/assets/img"
OUT_DIR.mkdir(parents=True, exist_ok=True)
MAP_PATH = ROOT / "build/media_map.json"


def main():
    groups = defaultdict(list)
    for f in IMG_ROOT.rglob("*"):
        if f.is_file():
            rel = f.relative_to(IMG_ROOT)
            id_ = rel.parts[0]
            groups[id_].append(f)

    def rank(f: Path) -> tuple:
        rel = f.relative_to(IMG_ROOT)
        parts = rel.parts
        # size score: prefer 700, then 450, then full (no size dir)
        if len(parts) > 2 and parts[1].isdigit():
            var = int(parts[1])
            size_score = abs(var - 700)
        else:
            size_score = 1500
        fmt_score = 0 if f.suffix.lower() == ".webp" else 1
        return (size_score, fmt_score, f.stat().st_size)

    media_map: dict[str, str] = {}
    total_bytes = 0
    for id_, files in groups.items():
        best = min(files, key=rank)
        ext = best.suffix.lower()
        dest = OUT_DIR / f"{id_}{ext}"
        shutil.copy2(best, dest)
        total_bytes += dest.stat().st_size
        # Map ALL possible HTML references for this id to the same dest
        for f in files:
            rel = f.relative_to(IMG_ROOT).as_posix()
            src_html = f"67be54ee7dfaae1e955c05a76e69ace8/{rel}"
            media_map[src_html] = f"/assets/img/{id_}{ext}"

    MAP_PATH.write_text(json.dumps(media_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Copied {len(groups)} deduped images ({total_bytes/1024/1024:.1f} MB) → {OUT_DIR}")
    print(f"media map → {MAP_PATH}")


if __name__ == "__main__":
    main()

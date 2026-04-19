#!/usr/bin/env python3
"""Extract structured content from the Webnode export of artide.it."""
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = Path(__file__).resolve().parent.parent / "_source/extracted/www.artide.it"
OUT = Path(__file__).resolve().parent.parent / "build/content.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

SKIP_CLASSES = {"s-hm", "s-hm-hidden", "wnd-h-hidden", "s-ft", "l-f"}


def clean_text(s: str) -> str:
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def href_to_slug(href: str) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return href
    if href.startswith("http"):
        if "artide.it" not in href and "cdnwnd" not in href:
            return href
    # Strip host and leading slash
    href = re.sub(r"^https?://[^/]+/?", "/", href)
    href = href.split("?")[0].split("#")[0]
    if href.endswith("/index.htm"):
        href = href[: -len("index.htm")]
    if href.endswith(".htm"):
        href = href[:-4]
    if not href.startswith("/"):
        href = "/" + href
    return href


def extract_image_src(tag: Tag) -> str | None:
    """Return a relative local path for an <img> tag if it's a local asset."""
    src = (
        tag.get("data-src")
        or tag.get("data-original")
        or tag.get("src")
        or ""
    )
    if not src:
        # Look for srcset
        srcset = tag.get("srcset") or tag.get("data-srcset") or ""
        if srcset:
            src = srcset.split(",")[0].split()[0]
    if not src:
        return None
    # Normalize: take only the basename path inside the export dir if it looks local
    src = src.strip()
    # Remove scheme+host of cdnwnd
    src = re.sub(r"^https?://[^/]+/", "", src)
    src = src.split("?")[0]
    return src


def extract_page(html_path: Path, url: str) -> dict:
    html = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.find("title")
    title = clean_text(title_tag.get_text()) if title_tag else ""

    desc = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        desc = clean_text(meta_desc.get("content", ""))

    keywords = ""
    meta_kw = soup.find("meta", attrs={"name": "keywords"})
    if meta_kw:
        keywords = clean_text(meta_kw.get("content", ""))

    og_img = ""
    og = soup.find("meta", attrs={"property": "og:image"})
    if og:
        og_img = og.get("content", "")

    main = soup.find("main") or soup.body
    blocks = []
    seen_texts = set()

    if main:
        # Walk all content elements in order; emit blocks
        for el in main.descendants:
            if not isinstance(el, Tag):
                continue
            name = el.name
            cls = " ".join(el.get("class", []) or [])
            # Skip hidden
            if any(c in cls for c in SKIP_CLASSES):
                continue

            if name in {"h1", "h2", "h3", "h4"}:
                txt = clean_text(el.get_text(" ", strip=True))
                if txt and txt not in seen_texts:
                    seen_texts.add(txt)
                    blocks.append({"type": "heading", "level": int(name[1]), "text": txt})

            elif name == "p":
                # Skip if nested inside another block we'll emit separately
                if el.find_parent(["li"]):
                    continue
                txt = clean_text(el.get_text(" ", strip=True))
                if txt and len(txt) > 3 and txt not in seen_texts:
                    seen_texts.add(txt)
                    blocks.append({"type": "paragraph", "text": txt, "html": str(el)})

            elif name == "img":
                src = extract_image_src(el)
                if src:
                    blocks.append({
                        "type": "image",
                        "src": src,
                        "alt": clean_text(el.get("alt", "")),
                    })

            elif name == "ul" or name == "ol":
                items = []
                for li in el.find_all("li", recursive=False):
                    t = clean_text(li.get_text(" ", strip=True))
                    if t:
                        items.append(t)
                if items:
                    key = "|".join(items)
                    if key not in seen_texts:
                        seen_texts.add(key)
                        blocks.append({"type": "list", "ordered": name == "ol", "items": items})

            elif name == "a" and el.get("href"):
                # Only emit standalone CTAs (buttons), not inline text links
                cls = " ".join(el.get("class", []) or [])
                if any(c in cls for c in ["b-btn", "btn", "button", "wnd-btn"]):
                    txt = clean_text(el.get_text(" ", strip=True))
                    if txt:
                        blocks.append({
                            "type": "cta",
                            "text": txt,
                            "href": href_to_slug(el.get("href")),
                        })

    return {
        "url": url,
        "source_file": str(html_path.relative_to(SRC)),
        "title_original": title,
        "description_original": desc,
        "keywords_original": keywords,
        "og_image": og_img,
        "blocks": blocks,
    }


def main():
    pages = []
    # Collect all index.htm (subdir pages) + root index.htm
    for p in sorted(SRC.rglob("index.htm")):
        rel = p.relative_to(SRC)
        if rel.parent.as_posix() == ".":
            url = "/"
        else:
            url = "/" + rel.parent.as_posix()
        pages.append(extract_page(p, url))

    OUT.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extracted {len(pages)} pages → {OUT}")
    # Summary
    total_blocks = sum(len(p["blocks"]) for p in pages)
    type_count = {}
    for p in pages:
        for b in p["blocks"]:
            type_count[b["type"]] = type_count.get(b["type"], 0) + 1
    print("total blocks:", total_blocks)
    for t, c in sorted(type_count.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()

"""Apply SEO rewrite to the extracted content.

Outputs build/pages.json: a list of page dicts with SEO-clean fields, ready to
feed the static preview generator (and later the WP importer).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from seo_map import SEO_MAP, REDIRECTS, BLOG_ARTICLE_DEFAULTS  # noqa: E402


def clean(s: str) -> str:
    s = (s or "").replace("\xa0", " ")
    # normalise weird spacing inside words like "QUALIT À" → "QUALITÀ"
    s = re.sub(r"([a-zà-ÿ])\s+([A-ZÀ-Ÿ])(?=\s|$)", r"\1\2", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s


def title_case_preserving_brand(s: str) -> str:
    """Turn SCREAMING TEXT into Title Case, preserving acronyms like ISO, CE, UV, AIAQ."""
    if not s:
        return s
    acronyms = {"ISO", "CE", "UV", "UVC", "AIAQ", "MOCA", "RoHS", "OSA", "PLC",
                "RFID", "FAQ", "PDF", "HACCP", "WIKI", "IVA", "srl", "S.R.L.",
                "HTTPS", "URL"}
    words = re.split(r"(\s+|[-/])", s)
    out = []
    for w in words:
        if not w or w.isspace() or w in {"-", "/"}:
            out.append(w)
            continue
        if w.upper() in {a.upper() for a in acronyms}:
            # keep canonical casing from acronyms set
            canon = next((a for a in acronyms if a.upper() == w.upper()), w.upper())
            out.append(canon)
        elif w.isupper() and len(w) > 1:
            out.append(w.capitalize())
        else:
            out.append(w)
    return "".join(out)


def fix_typos(s: str) -> str:
    fixes = {
        r"\bPropietari": "Proprietari",
        r"\bRevamping\b": "Riqualificazione",
        r"\bScheider\b": "Schneider",
        r"\bParthner\b": "Partner",
    }
    for pat, repl in fixes.items():
        s = re.sub(pat, repl, s, flags=re.I)
    return s


def derive_blog_seo(page: dict) -> dict:
    """Auto-derive SEO for blog articles."""
    title = clean(page["title_original"])
    # Strip brand suffix
    for suffix in [" | Artide", " - Artide", " :: artide.it", " - artide.it"]:
        if title.endswith(suffix):
            title = title[: -len(suffix)]
    title = fix_typos(title)

    # H1 = cleaned title (max 70 chars)
    h1 = title if len(title) <= 70 else title[:67] + "…"

    # Title tag ≤ 60 chars: shorten + add brand suffix if room
    t = title
    if len(t) > 55:
        t = t[:52] + "…"
    title_tag = f"{t} | Artide"

    # Meta from existing desc or first paragraph
    meta = clean(page.get("description_original", ""))
    if not meta:
        for b in page["blocks"]:
            if b["type"] == "paragraph" and len(b["text"]) > 60:
                meta = b["text"]
                break
    meta = fix_typos(meta)
    if len(meta) > 158:
        meta = meta[:155] + "…"
    if len(meta) < 60:
        meta = f"{h1}. Approfondimento dal blog Artide su case dell'acqua, osmosi inversa e sostenibilità."[:158]

    return dict(
        h1=h1,
        title=title_tag,
        meta=meta,
        kw_primary=BLOG_ARTICLE_DEFAULTS["kw_primary"],
        kw_secondary=BLOG_ARTICLE_DEFAULTS["kw_secondary"],
        template=BLOG_ARTICLE_DEFAULTS["template"],
    )


def rewrite_blocks(blocks: list, page_seo: dict) -> list:
    """Apply block-level SEO cleanup: normalise headings, fix text, demote extra H1s."""
    out = []
    h1_seen = False
    for b in blocks:
        b = dict(b)  # copy
        if b["type"] == "heading":
            b["text"] = fix_typos(title_case_preserving_brand(clean(b["text"])))
            # Enforce single H1 per page: subsequent H1s become H2
            if b["level"] == 1:
                if h1_seen:
                    b["level"] = 2
                else:
                    h1_seen = True
            # Trim over-long H2/H3
            if b["level"] >= 2 and len(b["text"]) > 80:
                b["text"] = b["text"][:77] + "…"
        elif b["type"] == "paragraph":
            b["text"] = fix_typos(clean(b["text"]))
        elif b["type"] == "cta":
            b["text"] = clean(b["text"])
        elif b["type"] == "list":
            b["items"] = [fix_typos(clean(x)) for x in b["items"]]
        elif b["type"] == "image":
            if not b.get("alt"):
                # Derive alt from page H1 context
                b["alt"] = page_seo["h1"]
        out.append(b)
    return out


def merge_pages(primary: dict, extra: dict) -> dict:
    """Append extra.blocks to primary.blocks (skipping duplicate headings)."""
    seen = {b["text"] for b in primary["blocks"] if b["type"] == "heading"}
    merged = list(primary["blocks"])
    merged.append({"type": "heading", "level": 2, "text": "Approfondimento"})
    for b in extra["blocks"]:
        if b["type"] == "heading" and b["text"] in seen:
            continue
        # Demote H1s coming from the merged page
        if b["type"] == "heading" and b["level"] == 1:
            b = dict(b, level=2)
        merged.append(b)
    return {**primary, "blocks": merged}


def main():
    content_path = ROOT / "build/content.json"
    pages = json.loads(content_path.read_text(encoding="utf-8"))
    by_url = {p["url"]: p for p in pages}

    # Apply redirects: absorb content into target
    consolidated_sources = set()
    for src, dst in REDIRECTS.items():
        if src in by_url and dst in by_url:
            # For blog pagination duplicates, we drop (content is identical)
            if src.startswith("/blog/p-"):
                consolidated_sources.add(src)
                continue
            by_url[dst] = merge_pages(by_url[dst], by_url[src])
            consolidated_sources.add(src)

    # Also honour per-entry consolidate_from
    for url, seo in SEO_MAP.items():
        for src in seo.get("consolidate_from", []):
            if src in by_url and url in by_url:
                by_url[url] = merge_pages(by_url[url], by_url[src])
                consolidated_sources.add(src)

    output = []
    for url, page in by_url.items():
        if url in consolidated_sources:
            continue
        # Resolve SEO block
        if url in SEO_MAP:
            seo = {k: v for k, v in SEO_MAP[url].items() if k != "consolidate_from"}
        elif url.startswith("/l/blog-"):
            seo = derive_blog_seo(page)
        else:
            # Unknown page — skip (will be reviewed manually if any remains)
            print(f"  ! no SEO entry for {url}", file=sys.stderr)
            continue

        blocks = rewrite_blocks(page["blocks"], seo)
        output.append({
            "url": url,
            "h1": seo["h1"],
            "title": seo["title"],
            "meta": seo["meta"],
            "kw_primary": seo["kw_primary"],
            "kw_secondary": seo.get("kw_secondary", []),
            "template": seo["template"],
            "blocks": blocks,
            "source_file": page["source_file"],
        })

    # Stable order: home first, then alphabetical, but blog articles last
    def sort_key(p):
        u = p["url"]
        if u == "/":
            return (0, "")
        if u.startswith("/l/blog-"):
            return (3, u)
        if u == "/blog":
            return (2, u)
        return (1, u)

    output.sort(key=sort_key)

    out_path = ROOT / "build/pages.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    # Also write the redirects for later WP import
    redirects_path = ROOT / "build/redirects.json"
    redirects = [{"from": s, "to": d} for s, d in REDIRECTS.items()]
    redirects_path.write_text(json.dumps(redirects, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write a human-friendly SEO review CSV
    csv_path = ROOT / "build/seo-map.csv"
    import csv
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "template", "kw_primary", "h1", "title", "meta_len", "meta"])
        for p in output:
            w.writerow([p["url"], p["template"], p["kw_primary"], p["h1"],
                        p["title"], len(p["meta"]), p["meta"]])

    print(f"Rewrote {len(output)} pages → {out_path}")
    print(f"  redirects → {redirects_path}")
    print(f"  SEO CSV   → {csv_path}")


if __name__ == "__main__":
    main()

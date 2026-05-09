#!/usr/bin/env python3
"""Generate Gutenberg block markup for each simple internal page,
extracted from preview/<slug>/index.html.

Output: wp-assets/page-markup/<slug>.html
"""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

REPO_BRANCH = "claude/fix-wordpress-api-error-DaxZ9"
IMG_CDN = (
    f"https://raw.githubusercontent.com/Blasir77/artide.it/"
    f"{REPO_BRANCH}/preview/assets/img/"
)

PAGES = [
    "chi-siamo",
    "iso-9001", "iso-14001", "iso-22000",
    "aiaq", "ce", "moca", "osa", "rohs",
    "gestore-ambientale",
    "info-copyright", "citazioni-bibliografiche",
    "manutenzione", "automazione", "sanificazione",
    "incasso", "potabilizzazione", "progettazione",
    "sviluppo-software", "telecontrollo", "corsi",
    "trasformazione",
]


def clean_inline(s: str) -> str:
    """Strip Webnode wrappers, keep <strong>/<em>/<a>/<br>."""
    s = re.sub(r"</?(?:font|span)\b[^>]*>", "", s)
    s = re.sub(r"\s+(?:style|class|data-[\w-]+|id)=\"[^\"]*\"", "", s)
    s = re.sub(r"<a\s*>", "", s)
    s = s.replace("/artide.it/", "/")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def extract_first_image(section_html: str) -> str | None:
    """Find the first image filename inside a section."""
    m = re.search(r'src="[^"]*?/assets/img/([^"?]+)', section_html)
    if m:
        return m.group(1)
    m = re.search(r'srcset="[^"]*?/assets/img/([^"?\s]+)', section_html)
    if m:
        return m.group(1)
    return None


def extract_content_section(html: str) -> str:
    """Pick the first s-basic section that contains the H1 — the page content."""
    sections = re.findall(
        r'<section[^>]*class="s s-basic[^"]*"[^>]*>(.*?)</section>',
        html, re.S
    )
    for sec in sections:
        if re.search(r"<h1\b", sec):
            return sec
    return ""


def find_all_images(section_html: str) -> list[str]:
    """All image filenames from img/picture/source srcset within the section."""
    files: list[str] = []
    for m in re.finditer(r'/assets/img/([^"?\s]+\.(?:webp|jpg|jpeg|png|gif))',
                          section_html):
        fn = m.group(1)
        if fn not in files:
            files.append(fn)
    return files


def parse_blocks(section_html: str) -> list[tuple[str, str]]:
    """Walk the section and return ordered list of (kind, content).

    kind: 'h1' | 'h2' | 'h3' | 'p'
    content: cleaned HTML (with semantic tags preserved)

    Image positions are NOT preserved — we'll insert images at strategic
    points in the rendered Gutenberg output.
    """
    blocks: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    # Match top-level h1-h3 / p elements (ignoring nested ones inside other tags)
    pattern = re.compile(r"<(h[1-3]|p)\b[^>]*>(.*?)</\1>", re.S)
    for m in pattern.finditer(section_html):
        kind = m.group(1)
        raw = m.group(2)
        # Skip paragraphs that are only media/empty
        if re.search(r"<(?:source|picture|img)\b", raw):
            continue
        text = clean_inline(raw)
        plain = strip_tags(text)
        # Skip breadcrumb h3 with arrow
        if kind == "h3" and "→" in plain:
            continue
        # Skip empty/very short
        if len(plain) < 3:
            continue
        # Dedup
        key = (kind, plain[:80])
        if key in seen:
            continue
        seen.add(key)
        blocks.append((kind, text))

    return blocks


def build_breadcrumb(slug: str, h1_text: str) -> str:
    """Build a small breadcrumb 'Home / [Page Title]' line."""
    return (
        '<!-- wp:paragraph {"align":"center","style":{"color":{"text":"#999999"},'
        '"typography":{"fontSize":"13px","textTransform":"uppercase",'
        '"letterSpacing":"2px","fontWeight":"600"}}} -->\n'
        f'<p class="has-text-align-center" '
        f'style="color:#999999;font-size:13px;font-weight:600;'
        f'letter-spacing:2px;text-transform:uppercase">'
        f'<a href="/" style="color:inherit;text-decoration:none;">Home</a>'
        f' &nbsp;/&nbsp; {strip_tags(h1_text)[:60]}</p>\n'
        '<!-- /wp:paragraph -->'
    )


def build_h1(text: str) -> str:
    return (
        '<!-- wp:heading {"textAlign":"center","level":1,'
        '"style":{"typography":{"fontSize":"42px","fontWeight":"800",'
        '"lineHeight":"1.15"},"spacing":{"margin":{"top":"16px","bottom":"40px"}}}} -->\n'
        f'<h1 class="wp-block-heading has-text-align-center" '
        f'style="margin-top:16px;margin-bottom:40px;'
        f'font-size:42px;font-weight:800;line-height:1.15">{text}</h1>\n'
        '<!-- /wp:heading -->'
    )


def build_h2(text: str) -> str:
    return (
        '<!-- wp:heading {"level":2,"style":{"typography":{"fontSize":"28px",'
        '"fontWeight":"700","lineHeight":"1.25"},"spacing":{"margin":{"top":"40px",'
        '"bottom":"16px"}}}} -->\n'
        f'<h2 class="wp-block-heading" '
        f'style="margin-top:40px;margin-bottom:16px;'
        f'font-size:28px;font-weight:700;line-height:1.25">{text}</h2>\n'
        '<!-- /wp:heading -->'
    )


def build_h3(text: str) -> str:
    return (
        '<!-- wp:heading {"level":3,"style":{"typography":{"fontSize":"20px",'
        '"fontWeight":"700","lineHeight":"1.3"},"spacing":{"margin":{"top":"28px",'
        '"bottom":"12px"}}}} -->\n'
        f'<h3 class="wp-block-heading" '
        f'style="margin-top:28px;margin-bottom:12px;'
        f'font-size:20px;font-weight:700;line-height:1.3">{text}</h3>\n'
        '<!-- /wp:heading -->'
    )


def build_paragraph(text: str) -> str:
    return (
        '<!-- wp:paragraph {"align":"justify","style":{"typography":'
        '{"fontSize":"17px","lineHeight":"1.7"}}} -->\n'
        f'<p class="has-text-align-justify" '
        f'style="font-size:17px;line-height:1.7">{text}</p>\n'
        '<!-- /wp:paragraph -->'
    )


def build_image(filename: str, alt: str = "") -> str:
    url = IMG_CDN + filename
    return (
        '<!-- wp:image {"sizeSlug":"large","linkDestination":"none","style":'
        '{"border":{"radius":"8px"}}} -->\n'
        '<figure class="wp-block-image size-large has-custom-border" '
        'style="margin:32px 0;">'
        f'<img src="{url}" alt="{html_lib.escape(alt)}" '
        f'style="border-radius:8px;width:100%;height:auto;"/></figure>\n'
        '<!-- /wp:image -->'
    )


def build_page_markup(slug: str, source: Path) -> str:
    html = source.read_text(encoding="utf-8")
    section = extract_content_section(html)
    if not section:
        return ""

    images = find_all_images(section)
    blocks = parse_blocks(section)
    if not blocks:
        return ""

    # Compose the page
    out: list[str] = []

    # Wrap content in a centered constrained group
    out.append(
        '<!-- wp:group {"align":"full","style":{"spacing":{"padding":'
        '{"top":"60px","bottom":"80px","left":"20px","right":"20px"}}},'
        '"layout":{"type":"constrained","contentSize":"900px"}} -->\n'
        '<div class="wp-block-group alignfull" '
        'style="padding-top:60px;padding-right:20px;'
        'padding-bottom:80px;padding-left:20px">'
    )

    # Find the H1
    h1_block = next(((k, t) for k, t in blocks if k == "h1"), None)
    if h1_block:
        h1_text = h1_block[1]
        out.append(build_breadcrumb(slug, h1_text))
        out.append(build_h1(h1_text))

    # Insert first image after H1 (if available)
    if images:
        out.append(build_image(images[0], strip_tags(h1_block[1]) if h1_block else slug))

    # Then walk paragraphs and headings (skip the H1 we already used)
    img_used = 1
    para_count = 0
    for kind, text in blocks:
        if kind == "h1":
            continue
        if kind == "h2":
            out.append(build_h2(text))
        elif kind == "h3":
            out.append(build_h3(text))
        else:
            out.append(build_paragraph(text))
            para_count += 1
            # Insert next image after every 5 paragraphs
            if para_count % 5 == 0 and img_used < len(images):
                out.append(build_image(images[img_used], slug))
                img_used += 1

    # Close group
    out.append("</div>\n<!-- /wp:group -->")

    return "\n\n".join(out)


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    out_dir = repo_root / "wp-assets" / "page-markup"
    out_dir.mkdir(parents=True, exist_ok=True)

    for slug in PAGES:
        src = repo_root / "preview" / slug / "index.html"
        if not src.exists():
            print(f"  ✗ skip {slug}: no preview file")
            continue
        markup = build_page_markup(slug, src)
        if not markup:
            print(f"  ✗ skip {slug}: no extractable content")
            continue
        out_file = out_dir / f"{slug}.html"
        out_file.write_text(markup, encoding="utf-8")
        size_kb = out_file.stat().st_size / 1024
        print(f"  ✓ {slug:30} → {out_file.relative_to(repo_root)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()

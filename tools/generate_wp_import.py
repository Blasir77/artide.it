#!/usr/bin/env python3
"""Generate a WordPress WXR (eXtended RSS) import file with all Artide pages
and the Primary Menu structure already wired up."""

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

PREVIEW_DIR = Path(__file__).resolve().parent.parent / "preview"


def _clean_inline(s: str) -> str:
    """Strip Webnode-specific wrappers, keep semantic tags."""
    # Drop <font>, <span> wrappers but keep their content
    s = re.sub(r"</?(?:font|span)\b[^>]*>", "", s)
    # Drop inline style and class attributes
    s = re.sub(r'\s+(?:style|class|data-[\w-]+)="[^"]*"', "", s)
    # Drop empty <a> with no href
    s = re.sub(r"<a\s*>", "", s)
    # Rewrite preview-relative links to root-relative WordPress URLs
    s = s.replace("/artide.it/", "/")
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def extract_page_content(slug: str) -> str:
    """Return Gutenberg-block-formatted content for a preview page slug.

    Returns empty string if the page has no extractable content (home, blog,
    landing pages) so they can be filled by hand or by Strategy A overrides.
    """
    src = PREVIEW_DIR / slug / "index.html"
    if not src.exists():
        return ""
    raw = src.read_text(encoding="utf-8")

    # Pick the first s-basic section that contains an h1 — that's the content.
    sections = re.findall(
        r'<section[^>]*class="s s-basic[^"]*"[^>]*>(.*?)</section>', raw, re.S
    )
    body = ""
    for sec in sections:
        if re.search(r"<h1\b", sec):
            body = sec
            break
    if not body:
        return ""

    blocks: list[str] = []

    # H1 → Gutenberg heading level 1
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    if h1:
        text = _clean_inline(h1.group(1))
        text_only = _strip_tags(text)
        if text_only:
            blocks.append(
                f'<!-- wp:heading {{"level":1}} -->\n<h1 class="wp-block-heading">{text}</h1>\n<!-- /wp:heading -->'
            )

    # H2 / H3 (skip breadcrumb h3 which has the "AZIENDA →" pattern)
    for tag, level in (("h2", 2), ("h3", 3)):
        for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", body, re.S):
            text = _clean_inline(m.group(1))
            plain = _strip_tags(text)
            if not plain or "→" in plain:
                continue
            blocks.append(
                f'<!-- wp:heading {{"level":{level}}} -->\n<h{level} class="wp-block-heading">{text}</h{level}>\n<!-- /wp:heading -->'
            )

    # Paragraphs — skip those containing media elements
    for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S):
        if re.search(r"<(?:source|picture|img)\b", p):
            continue
        text = _clean_inline(p)
        plain = _strip_tags(text).strip()
        if len(plain) < 4:
            continue
        blocks.append(
            f"<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->"
        )

    # Lists
    for ul in re.findall(r"<ul[^>]*>(.*?)</ul>", body, re.S):
        items = re.findall(r"<li[^>]*>(.*?)</li>", ul, re.S)
        cleaned = [_clean_inline(li) for li in items]
        cleaned = [li for li in cleaned if _strip_tags(li).strip()]
        if not cleaned:
            continue
        list_html = "".join(f"<li>{li}</li>" for li in cleaned)
        blocks.append(
            f"<!-- wp:list -->\n<ul>{list_html}</ul>\n<!-- /wp:list -->"
        )

    return "\n\n".join(blocks)

SITE_TITLE = "Artide"
SITE_URL = "https://37.156.244.26/~artide1"
AUTHOR_LOGIN = "admin"
AUTHOR_EMAIL = "admin@artide.local"
NOW = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
NOW_SQL = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
MENU_NAME = "Menu Principale Artide"
MENU_SLUG = "menu-principale-artide"

# Pages: (id, slug, title, parent_id)
PAGES: list[tuple[int, str, str, int]] = [
    (10, "home", "Home", 0),
    (11, "chi-siamo", "Chi Siamo", 0),
    (12, "contatti", "Contatti", 0),
    (13, "blog", "Blog", 0),
    (14, "certificazioni", "Certificazioni", 11),
    (15, "aiaq", "AIAQ", 14),
    (16, "ce", "CE", 14),
    (17, "moca", "DM174, DM25, MOCA", 14),
    (18, "gestore-ambientale", "Gestore Ambientale", 14),
    (19, "iso-9001", "ISO 9001", 14),
    (20, "iso-14001", "ISO 14001", 14),
    (21, "iso-22000", "ISO 22000", 14),
    (22, "osa", "OSA", 14),
    (23, "rohs", "RoHS", 14),
    (24, "info-copyright", "Info & Copyright", 11),
    (25, "informativa-privacy", "Informativa Privacy", 11),
    (26, "citazioni-bibliografiche", "Citazioni Bibliografiche", 11),
    (27, "team", "Il Team", 11),
    (28, "prodotti", "Prodotti", 0),
    (29, "casa-dell-acqua", "Casa dell'Acqua", 28),
    (30, "casa-dell-acqua-collezione", "Collezione", 29),
    (31, "faq-casa-dell-acqua", "FAQ Casa dell'Acqua", 29),
    (32, "servizi", "Servizi", 0),
    (33, "automazione", "Automazione", 32),
    (34, "corsi", "Corsi di Formazione", 32),
    (35, "manutenzione", "Manutenzione", 32),
    (36, "incasso", "Incasso", 32),
    (37, "potabilizzazione", "Potabilizzazione", 32),
    (38, "progettazione", "Progettazione", 32),
    (39, "trasformazione", "Riqualificazione", 32),
    (40, "sanificazione", "Sanificazione", 32),
    (41, "sviluppo-software", "Sviluppo Software", 32),
    (42, "telecontrollo", "Telecontrollo", 32),
]

# Menu items: (id, label, parent_menu_item_id, page_slug_or_url, order)
# Order and content match the preview's RENDERED state, after the JS in
# preview-src/artide-overrides.js has run (top-level reorder, removal of
# SUPPORTO/WIKI/WIKI-* placeholders, ASSISTENZA → CONTATTI rename).
MENU_ITEMS: list[tuple[int, str, int, str, int]] = [
    (130, "PRODOTTI", 0, "prodotti", 1),
    (131, "Casa dell'Acqua", 130, "casa-dell-acqua", 1),
    (132, "Collezione", 131, "casa-dell-acqua-collezione", 1),
    (133, "FAQ", 131, "faq-casa-dell-acqua", 2),

    (140, "SERVIZI", 0, "servizi", 2),
    (141, "Automazione", 140, "automazione", 1),
    (142, "Corsi di Formazione", 140, "corsi", 2),
    (143, "Manutenzione", 140, "manutenzione", 3),
    (144, "Incasso", 140, "incasso", 4),
    (145, "Potabilizzazione", 140, "potabilizzazione", 5),
    (146, "Progettazione", 140, "progettazione", 6),
    (147, "Riqualificazione", 140, "trasformazione", 7),
    (148, "Sanificazione", 140, "sanificazione", 8),
    (149, "Sviluppo Software", 140, "sviluppo-software", 9),
    (150, "Telecontrollo", 140, "telecontrollo", 10),

    (110, "AZIENDA", 0, "chi-siamo", 3),
    (111, "Contatti", 110, "contatti", 1),
    (112, "Chi Siamo", 110, "chi-siamo", 2),
    (113, "Certificazioni", 110, "certificazioni", 3),
    (114, "AIAQ", 113, "aiaq", 1),
    (115, "CE", 113, "ce", 2),
    (116, "DM174, DM25, MOCA", 113, "moca", 3),
    (117, "Gestore Ambientale", 113, "gestore-ambientale", 4),
    (118, "ISO 9001", 113, "iso-9001", 5),
    (119, "ISO 14001", 113, "iso-14001", 6),
    (120, "ISO 22000", 113, "iso-22000", 7),
    (121, "OSA", 113, "osa", 8),
    (122, "RoHS", 113, "rohs", 9),
    (123, "Info & Copyright", 110, "info-copyright", 4),
    (124, "Informativa Privacy", 110, "informativa-privacy", 5),
    (125, "Citazioni Bibliografiche", 110, "citazioni-bibliografiche", 6),
    (126, "Il Team", 110, "team", 7),

    (100, "BLOG", 0, "blog", 4),
    (101, "Articoli del Blog", 100, "blog", 1),
    (102, "Articoli in Evidenza", 100, "blog", 2),

    (160, "CONTATTI", 0, "contatti", 5),
]

PAGE_BY_SLUG = {slug: pid for pid, slug, _, _ in PAGES}


def cdata(text: str) -> str:
    return f"<![CDATA[{text}]]>"


def page_xml(pid: int, slug: str, title: str, parent: int) -> str:
    link = f"{SITE_URL}/{slug}/"
    # Skip content extraction for landing/hub pages handled separately
    skip_content = {"home", "blog"}
    content = "" if slug in skip_content else extract_page_content(slug)
    return f"""\t<item>
\t\t<title>{html.escape(title)}</title>
\t\t<link>{link}</link>
\t\t<pubDate>{NOW}</pubDate>
\t\t<dc:creator>{cdata(AUTHOR_LOGIN)}</dc:creator>
\t\t<guid isPermaLink="false">{SITE_URL}/?page_id={pid}</guid>
\t\t<description></description>
\t\t<content:encoded>{cdata(content)}</content:encoded>
\t\t<excerpt:encoded>{cdata("")}</excerpt:encoded>
\t\t<wp:post_id>{pid}</wp:post_id>
\t\t<wp:post_date>{cdata(NOW_SQL)}</wp:post_date>
\t\t<wp:post_date_gmt>{cdata(NOW_SQL)}</wp:post_date_gmt>
\t\t<wp:post_modified>{cdata(NOW_SQL)}</wp:post_modified>
\t\t<wp:post_modified_gmt>{cdata(NOW_SQL)}</wp:post_modified_gmt>
\t\t<wp:comment_status>{cdata("closed")}</wp:comment_status>
\t\t<wp:ping_status>{cdata("closed")}</wp:ping_status>
\t\t<wp:post_name>{cdata(slug)}</wp:post_name>
\t\t<wp:status>{cdata("publish")}</wp:status>
\t\t<wp:post_parent>{parent}</wp:post_parent>
\t\t<wp:menu_order>0</wp:menu_order>
\t\t<wp:post_type>{cdata("page")}</wp:post_type>
\t\t<wp:post_password>{cdata("")}</wp:post_password>
\t\t<wp:is_sticky>0</wp:is_sticky>
\t</item>
"""


def menu_item_xml(mid: int, label: str, parent_mid: int, target: str, order: int) -> str:
    if target.startswith("url:"):
        url = target[4:]
        item_type = "custom"
        object_kind = "custom"
        object_id = mid
        link_url = url
    else:
        page_id = PAGE_BY_SLUG[target]
        item_type = "post_type"
        object_kind = "page"
        object_id = page_id
        link_url = f"{SITE_URL}/{target}/"

    return f"""\t<item>
\t\t<title>{html.escape(label)}</title>
\t\t<link>{link_url}</link>
\t\t<pubDate>{NOW}</pubDate>
\t\t<dc:creator>{cdata(AUTHOR_LOGIN)}</dc:creator>
\t\t<guid isPermaLink="false">{SITE_URL}/?p={mid}</guid>
\t\t<description></description>
\t\t<content:encoded>{cdata("")}</content:encoded>
\t\t<excerpt:encoded>{cdata("")}</excerpt:encoded>
\t\t<wp:post_id>{mid}</wp:post_id>
\t\t<wp:post_date>{cdata(NOW_SQL)}</wp:post_date>
\t\t<wp:post_date_gmt>{cdata(NOW_SQL)}</wp:post_date_gmt>
\t\t<wp:post_modified>{cdata(NOW_SQL)}</wp:post_modified>
\t\t<wp:post_modified_gmt>{cdata(NOW_SQL)}</wp:post_modified_gmt>
\t\t<wp:comment_status>{cdata("closed")}</wp:comment_status>
\t\t<wp:ping_status>{cdata("closed")}</wp:ping_status>
\t\t<wp:post_name>{cdata(str(mid))}</wp:post_name>
\t\t<wp:status>{cdata("publish")}</wp:status>
\t\t<wp:post_parent>0</wp:post_parent>
\t\t<wp:menu_order>{order}</wp:menu_order>
\t\t<wp:post_type>{cdata("nav_menu_item")}</wp:post_type>
\t\t<wp:post_password>{cdata("")}</wp:post_password>
\t\t<wp:is_sticky>0</wp:is_sticky>
\t\t<category domain="nav_menu" nicename="{MENU_SLUG}">{cdata(MENU_NAME)}</category>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_type")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata(item_type)}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_menu_item_parent")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata(str(parent_mid))}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_object_id")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata(str(object_id))}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_object")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata(object_kind)}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_target")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata("")}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_classes")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata('a:1:{i:0;s:0:"";}')}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_xfn")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata("")}</wp:meta_value>
\t\t</wp:postmeta>
\t\t<wp:postmeta>
\t\t\t<wp:meta_key>{cdata("_menu_item_url")}</wp:meta_key>
\t\t\t<wp:meta_value>{cdata("")}</wp:meta_value>
\t\t</wp:postmeta>
\t</item>
"""


def build_xml() -> str:
    head = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
\txmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
\txmlns:content="http://purl.org/rss/1.0/modules/content/"
\txmlns:wfw="http://wellformedweb.org/CommentAPI/"
\txmlns:dc="http://purl.org/dc/elements/1.1/"
\txmlns:wp="http://wordpress.org/export/1.2/">
<channel>
\t<title>{SITE_TITLE}</title>
\t<link>{SITE_URL}</link>
\t<description>Import file with pages and primary menu</description>
\t<pubDate>{NOW}</pubDate>
\t<language>it-IT</language>
\t<wp:wxr_version>1.2</wp:wxr_version>
\t<wp:base_site_url>{SITE_URL}</wp:base_site_url>
\t<wp:base_blog_url>{SITE_URL}</wp:base_blog_url>
\t<wp:author>
\t\t<wp:author_id>1</wp:author_id>
\t\t<wp:author_login>{cdata(AUTHOR_LOGIN)}</wp:author_login>
\t\t<wp:author_email>{cdata(AUTHOR_EMAIL)}</wp:author_email>
\t\t<wp:author_display_name>{cdata(AUTHOR_LOGIN)}</wp:author_display_name>
\t\t<wp:author_first_name>{cdata("")}</wp:author_first_name>
\t\t<wp:author_last_name>{cdata("")}</wp:author_last_name>
\t</wp:author>
\t<wp:term>
\t\t<wp:term_id>2</wp:term_id>
\t\t<wp:term_taxonomy>nav_menu</wp:term_taxonomy>
\t\t<wp:term_slug>{MENU_SLUG}</wp:term_slug>
\t\t<wp:term_parent></wp:term_parent>
\t\t<wp:term_name>{cdata(MENU_NAME)}</wp:term_name>
\t</wp:term>
"""
    parts = [head]
    for pid, slug, title, parent in PAGES:
        parts.append(page_xml(pid, slug, title, parent))
    for mid, label, parent_mid, target, order in MENU_ITEMS:
        parts.append(menu_item_xml(mid, label, parent_mid, target, order))
    parts.append("</channel>\n</rss>\n")
    return "".join(parts)


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "artide-import.xml"
    out.write_text(build_xml(), encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
    print(f"Pages: {len(PAGES)}  Menu items: {len(MENU_ITEMS)}")


if __name__ == "__main__":
    main()

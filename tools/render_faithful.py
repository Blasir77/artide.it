"""Faithful preview generator.

Strategy:
- Start from each original Webnode HTML file in _source/extracted/www.artide.it/
- Keep the whole markup + CSS + fonts untouched (same visual design).
- Patch ONLY:
    1. <title>                 → SEO title from seo_map.py
    2. <meta name=description> → SEO description
    3. Headings                 → single H1 with keyword, clean H2/H3 hierarchy
    4. Text typos (Propietari, Revamping, Scheider, Parthner, stray spaces)
    5. Image <img src=…>       → /assets/img/<id>.webp (our compressed versions)
    6. Links to other pages     → clean absolute URLs (/chi-siamo/ not …/index.htm)
    7. CSS/JS/font URLs         → absolute URLs prefixed with BASE_PREFIX
- Prepend a small yellow preview banner.
- Remove tracking scripts (gtag, iubenda) from preview only.
- Apply the URL consolidation (redirects.json): for consolidated pages a short
  HTML refresh stub is written instead.

Output → preview/
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_source/extracted/www.artide.it"
OUT = ROOT / "preview"
sys.path.insert(0, str(ROOT / "tools"))
from seo_map import SEO_MAP, REDIRECTS, BLOG_ARTICLE_DEFAULTS  # noqa: E402
from seo_copy import get_copy as get_seo_copy  # noqa: E402

MEDIA_MAP = json.loads((ROOT / "build/media_map.json").read_text(encoding="utf-8"))
BASE = os.environ.get("BASE_PREFIX", "").rstrip("/")

# ─── helpers ────────────────────────────────────────────────────

def abs_path(p: str) -> str:
    """Prepend BASE prefix to a site-absolute path starting with /."""
    if not BASE or not p.startswith("/") or p.startswith("//"):
        return p
    return BASE + p


def url_to_outpath(url: str) -> Path:
    if url == "/":
        return OUT / "index.html"
    return OUT / url.strip("/") / "index.html"


def clean_heading(text: str) -> str:
    text = text.replace("\xa0", " ")
    # Merge 'QUALIT À' → 'QUALITÀ' (Webnode sometimes broke accented chars)
    text = re.sub(r"([A-Za-zàèéìòóùÀÈÉÌÒÓÙ])\s+([ÀÈÉÌÒÓÙàèéìòóù])(?=\s|$|[^A-Za-z])", r"\1\2", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


INLINE_TAGS = r"(?:strong|em|b|i|u|font|span|a|mark|sub|sup)"

# Matches: word-ending char + one-or-more inline open/close tags + word-starting char.
# Example matches in the Webnode output:
#   "una</font><a><strong>Garanzia"      → inserts a space after "una"
#   "vandalici</strong></a><font>del"    → inserts a space after "vandalici"
#   "manutenzione*</font><font>(<em>vedi"→ inserts a space after "manutenzione*"
_RE_TAG_CLUSTER = re.compile(
    r'([A-Za-zÀ-ÿ0-9\)\]\*\+!?.,;:])((?:\s*</?' + INLINE_TAGS + r'\b[^>]*>\s*)+)(?=[A-Za-zÀ-ÿ0-9(])',
    flags=re.I,
)


_RE_TRAILING_WS_INSIDE = re.compile(
    r'(\s+)(</' + INLINE_TAGS + r'>)',
    flags=re.I,
)
_RE_LEADING_WS_INSIDE = re.compile(
    r'(<' + INLINE_TAGS + r'\b[^>]*>)(\s+)',
    flags=re.I,
)


def fix_inline_spacing(html: str) -> str:
    """Normalise whitespace at the boundaries of inline tags.

    1. Move WHITESPACE that's just before the closing tag (e.g.
       ``<a>Artide  </a>``) to OUTSIDE the tag → ``<a>Artide</a>  ``.
       Same for whitespace just after an opening tag.
       This stops Webnode's text-decoration: underline on <a> from
       extending under trailing spaces, and it keeps drop-cap patterns
       like ``<strong>H  </strong>ai`` rendering correctly.

    2. Insert a single space wherever a cluster of inline tags sits
       between two word characters but has no whitespace between them
       (the legacy "una<font></font><a><strong>Garanzia" glue case).

    3. Apply known Italian misspellings.
    4. Split vowel+è glue ("qualitàè" → "qualità è").
    """
    # 1. Insert a space between glued tag-cluster boundaries first.
    #    This may temporarily place a whitespace INSIDE a closing tag
    #    (e.g. "Artide</a>è" → "Artide </a>è"); step 2 bubbles it out.
    html = _RE_TAG_CLUSTER.sub(r'\1 \2', html)
    html = _RE_TAG_CLUSTER.sub(r'\1 \2', html)

    # 2. Bubble trailing/leading whitespace OUT of every inline tag, so
    #    underline / accent decorations on <a>, <strong>, … don't extend
    #    over a stray space, and drop-cap patterns like "<strong>H  </strong>ai"
    #    don't render with a wide gap. Loop until a fixed point because
    #    nested tags need multiple passes.
    for _ in range(8):
        new = _RE_TRAILING_WS_INSIDE.sub(r'\2\1', html)
        new = _RE_LEADING_WS_INSIDE.sub(r'\2\1', new)
        if new == html:
            break
        html = new
    # Common Italian misspellings present in the original Webnode source.
    # Run BEFORE the vowel+è split so words like "Perchè" don't get
    # wrongly broken into "Perch è".
    html = _apply_known_misspellings(html)
    # Vowel + glued "è" → split with a space. Restricted to VOWELS only so
    # legitimate è-final words preceded by a consonant ("perché"-class) are
    # not affected. This handles real glue cases like "qualitàè", "Artideè",
    # "sitoè" → "qualità è", "Artide è", "sito è".
    html = re.sub(r'([aeiouàèéìòóù])è([a-zà-ÿA-ZÀ-Ÿ])', r'\1 è \2', html)
    html = re.sub(r'([aeiouàèéìòóù])è(?=\s|[,.!?;:]|$)', r'\1 è', html)
    return html


# ── Italian-language misspelling corrections ─────────────────────
# Centralised so both fix_typos (text-node level) and
# fix_inline_spacing (HTML level) apply the same fixes.
_KNOWN_MISSPELLINGS = [
    # (pattern, replacement, flags)
    (r"\bPerchè\b",        "Perché",         0),
    (r"\bperchè\b",        "perché",         0),
    (r"\bScegleire\b",     "Scegliere",      re.I),
    (r"\bprofessinista\b", "professionista", re.I),
    (r"\bprofessinisti\b", "professionisti", re.I),
    (r"\bPropietari",      "Proprietari",    re.I),
    (r"\bRevamping\b",     "RIQUALIFICAZIONE", re.I),
    # Force all capitalised "Riqualificazione" to full uppercase so it
    # matches the visual weight of other top-level menu / heading
    # labels (MANUTENZIONE, SANIFICAZIONE, …). Lowercase
    # "riqualificazione" inside running prose is left untouched.
    (r"\bRiqualificazione\b", "RIQUALIFICAZIONE", 0),
    (r"\bScheider\b",      "Schneider",      re.I),
    (r"\bParthner\b",      "Partner",        re.I),
    # Specific phrase that combined two errors ("quanto" → "quando" only
    # in this idiomatic phrase; we don't touch other "quanto" usages).
    (r"\bquanto\s+è\s+possibile\s+andare\b", "quando è possibile andare", re.I),
    # Detached uppercase accent ("QUALIT À" → "QUALITÀ"); also lowercase.
    (r"\bQUALIT\s+À\b",    "QUALITÀ",        0),
    (r"\bqualit\s+à\b",    "qualità",        0),
]


def _apply_known_misspellings(text: str) -> str:
    for pat, repl, flags in _KNOWN_MISSPELLINGS:
        text = re.sub(pat, repl, text, flags=flags)
    return text


def fix_typos(text: str) -> str:
    text = _apply_known_misspellings(text)
    # Generic vowel + glued "è" → split with a space (vowels only;
    # consonant+è words like "Perché" already corrected above).
    text = re.sub(r"([aeiouàèéìòóù])è(?=[\s,.;:!?]|$)", r"\1 è", text)
    return text


def url_for_original_file(rel_htm_path: str) -> str:
    """Map an original HTML path to a clean URL (no trailing slash except for '/')."""
    p = rel_htm_path.replace("\\", "/")
    if p in ("index.htm", "index-1.htm", ""):
        return "/"
    if p.endswith("/index.htm"):
        p = p[: -len("/index.htm")]
    elif p.endswith(".htm"):
        p = p[:-4]
    return "/" + p


def rewrite_anchor_href(href: str, source_url: str) -> str:
    """Normalise an <a href> found in the original HTML."""
    if not href:
        return href
    href = href.strip()
    # Mailto/tel/hash — unchanged
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return href
    # External
    if href.startswith("http"):
        # Self-links on artide.it? Convert to internal
        if "artide.it" in href:
            m = re.match(r"https?://[^/]*artide\.it(/.*)?", href)
            if m:
                href = m.group(1) or "/"
            else:
                return href
        else:
            return href
    # Strip query string preserving fragments? For internal, drop ?ph= noise
    href = href.split("?")[0]

    # Resolve relative path relative to source_url (our clean URL)
    if not href.startswith("/"):
        base_dir = source_url if source_url.endswith("/") else source_url.rsplit("/", 1)[0] + "/"
        # os.path.normpath keeps trailing slash info, handle manually
        parts = (base_dir + href).split("/")
        resolved = []
        for part in parts:
            if part == "" or part == ".":
                continue
            if part == "..":
                if resolved:
                    resolved.pop()
                continue
            resolved.append(part)
        href = "/" + "/".join(resolved)
        # Keep trailing slash for directory URLs
        if (base_dir + href).endswith("/"):
            pass

    # Strip /index.htm → /
    href = re.sub(r"/index(-1)?\.htm$", "/", href)
    if href.endswith(".htm"):
        href = href[:-4] + "/"
    # Ensure trailing slash for directory-like URLs (no file extension)
    if "." not in href.rsplit("/", 1)[-1] and not href.endswith("/"):
        href += "/"

    # Follow redirects at build time so navigation links never target a
    # 301 stub — eliminates internal redirects + guarantees the hrefs
    # are correct regardless of whether our client-side JS runs.
    # REDIRECTS keys are stored without a trailing slash; probe both.
    probe = href.rstrip("/") if href != "/" else href
    if probe in REDIRECTS:
        target = REDIRECTS[probe]
        href = target if target.endswith("/") or target == "/" else target + "/"

    return abs_path(href)


def rewrite_asset_href(href: str, source_url: str) -> str:
    """Normalise hrefs to files/, cs/, etc. — make them absolute site paths."""
    if not href:
        return href
    href = href.strip()
    if href.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:", "#")):
        return href
    # Strip ?ph=... version marker (used by Webnode cache-busting); we serve static files directly
    clean = href.split("?")[0]
    # Resolve relative
    if not clean.startswith("/"):
        base_dir = source_url if source_url.endswith("/") else source_url.rsplit("/", 1)[0] + "/"
        parts = (base_dir + clean).split("/")
        resolved = []
        for part in parts:
            if part == "" or part == ".":
                continue
            if part == "..":
                if resolved:
                    resolved.pop()
                continue
            resolved.append(part)
        clean = "/" + "/".join(resolved)
    return abs_path(clean)


def rewrite_img_src(src: str) -> str | None:
    """Map original image references to our compressed /assets/img/<id>.webp."""
    if not src:
        return None
    if src.startswith("data:"):
        return src
    from urllib.parse import unquote
    clean = unquote(src.split("?")[0])
    # Strip any leading ../
    key = re.sub(r"^(?:\.\./)+", "", clean).lstrip("/")
    # If src went through rewrite already and has our BASE, strip it
    if BASE and key.startswith(BASE.lstrip("/") + "/"):
        key = key[len(BASE.lstrip("/")) + 1:]
    mapped = MEDIA_MAP.get(key)
    if mapped:
        return abs_path(mapped)
    # Try also by matching by image ID (first folder segment after 67be54ee...)
    m = re.search(r"67be54ee7dfaae1e955c05a76e69ace8/([^/]+)/", key)
    if m:
        id_ = m.group(1)
        # find any media_map value for this id
        for k, v in MEDIA_MAP.items():
            if f"/{id_}/" in k:
                return abs_path(v)
    return None


# ─── banner ──────────────────────────────────────────────────────

def preview_banner_html(url: str, h1: str, kw: str) -> str:
    """Small dismissible preview badge pinned to bottom-right so it never
    interferes with the page layout or the header."""
    return f'''<div id="preview-banner" style="position:fixed;bottom:16px;right:16px;z-index:99999;background:#fff3cd;color:#7a5a00;padding:8px 14px;border-radius:10px;box-shadow:0 6px 20px rgba(0,0,0,0.14);font:600 12px/1.35 system-ui,-apple-system,sans-serif;border:1px solid #f3e2a0;max-width:420px">
<span style="opacity:0.85">Anteprima SEO</span>
<code style="background:rgba(0,0,0,0.05);padding:1px 6px;border-radius:4px;margin:0 4px">{url}</code>
<span style="opacity:0.6">· kw:</span> <b>{kw}</b>
<button onclick="document.getElementById('preview-banner').remove()" style="margin-left:10px;background:transparent;border:1px solid #b89a1a;border-radius:4px;padding:1px 7px;font:inherit;cursor:pointer;color:#7a5a00">×</button>
</div>'''


# ─── core patch routine ─────────────────────────────────────────

def apply_seo_patches(soup: BeautifulSoup, seo: dict, url: str) -> None:
    # <title>
    if soup.title is None:
        head = soup.head or soup
        new = soup.new_tag("title")
        head.append(new)
    soup.title.string = seo["title"]

    # <meta description>
    md = soup.find("meta", attrs={"name": "description"})
    if md is None:
        head = soup.head
        md = soup.new_tag("meta")
        md.attrs["name"] = "description"
        head.append(md)
    md.attrs["content"] = seo["meta"]

    # <meta og:title / og:description>
    for prop, content in [("og:title", seo["title"]), ("og:description", seo["meta"])]:
        t = soup.find("meta", attrs={"property": prop})
        if t is None:
            t = soup.new_tag("meta")
            t.attrs["property"] = prop
            soup.head.append(t)
        t.attrs["content"] = content

    # <meta keywords> — drop (not used by Google, noise)
    mk = soup.find("meta", attrs={"name": "keywords"})
    if mk:
        mk.decompose()

    # Canonical
    can = soup.find("link", attrs={"rel": "canonical"})
    canonical_url = url if url.endswith("/") or url == "/" else url + "/"
    if can is None:
        can = soup.new_tag("link", rel="canonical")
        soup.head.append(can)
    can.attrs["href"] = canonical_url

    # H1: single with new text; demote extras
    h1s = soup.find_all("h1")
    if h1s:
        first = h1s[0]
        # Preserve structure — only replace text contents
        first.clear()
        first.append(seo["h1"])
        for extra in h1s[1:]:
            extra.name = "h2"
    else:
        # Inject H1 at top of main if none exists
        main = soup.find("main") or soup.body
        if main:
            h1 = soup.new_tag("h1")
            h1.string = seo["h1"]
            main.insert(0, h1)

    # Clean and fix text of all headings + paragraphs
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "span", "li", "a"]):
        for child in list(tag.descendants):
            if isinstance(child, NavigableString) and not isinstance(child, type(soup.new_string(""))):
                pass
            if isinstance(child, NavigableString):
                new_text = fix_typos(clean_heading(str(child)))
                if new_text != child:
                    child.replace_with(new_text)


def strip_tracking(soup: BeautifulSoup) -> None:
    """Remove gtag + iubenda scripts so preview doesn't fire analytics."""
    for s in soup.find_all("script"):
        src = s.get("src", "")
        if any(t in src for t in ("gtag", "iubenda", "autoblocking")):
            s.decompose()
            continue
        if s.string and any(t in s.string for t in ("googletagmanager", "iubenda", "GTAG", "dataLayer")):
            s.decompose()


def rewrite_all_links(soup: BeautifulSoup, source_url: str) -> None:
    # <a href>
    for a in soup.find_all("a", href=True):
        a["href"] = rewrite_anchor_href(a["href"], source_url)

    # Forms
    for f in soup.find_all("form", action=True):
        f["action"] = rewrite_anchor_href(f["action"], source_url)

    # <link rel=stylesheet|icon|preload|...>
    for link in soup.find_all("link", href=True):
        link["href"] = rewrite_asset_href(link["href"], source_url)

    # <script src>
    for s in soup.find_all("script", src=True):
        s["src"] = rewrite_asset_href(s["src"], source_url)

    # <img src>
    for img in soup.find_all("img"):
        for attr in ("src", "data-src", "data-original"):
            val = img.get(attr)
            if not val:
                continue
            mapped = rewrite_img_src(val)
            if mapped:
                img[attr] = mapped
            else:
                img[attr] = rewrite_asset_href(val, source_url)
        # srcset: rewrite each URL
        srcset = img.get("srcset") or img.get("data-srcset")
        if srcset:
            new_parts = []
            for piece in srcset.split(","):
                piece = piece.strip()
                if not piece:
                    continue
                url_part, *rest = piece.split()
                mapped = rewrite_img_src(url_part) or rewrite_asset_href(url_part, source_url)
                new_parts.append(" ".join([mapped] + rest))
            img["srcset"] = ", ".join(new_parts)

    # <source src/srcset> (e.g. <picture>)
    for source in soup.find_all("source"):
        if source.get("src"):
            mapped = rewrite_img_src(source["src"]) or rewrite_asset_href(source["src"], source_url)
            source["src"] = mapped
        if source.get("srcset"):
            new_parts = []
            for piece in source["srcset"].split(","):
                piece = piece.strip()
                if not piece:
                    continue
                url_part, *rest = piece.split()
                mapped = rewrite_img_src(url_part) or rewrite_asset_href(url_part, source_url)
                new_parts.append(" ".join([mapped] + rest))
            source["srcset"] = ", ".join(new_parts)

    # Background-image in inline styles
    for el in soup.find_all(style=True):
        style = el["style"]
        def repl(m):
            u = m.group(1).strip().strip('"').strip("'")
            if u.startswith("data:"):
                return m.group(0)
            mapped = rewrite_img_src(u) or rewrite_asset_href(u, source_url)
            return f"url('{mapped}')"
        el["style"] = re.sub(r"url\(([^)]+)\)", repl, style)


def inject_shared_footer(soup: BeautifulSoup, block_html: str) -> None:
    """Append the shared footer block to the end of <main> (inside .sw > .sw-c)
    so it sits in the same DOM location as on the home page — otherwise
    scoped Webnode CSS targeting '.l-m > ...' wouldn't match and the
    styling would diverge between home and subpages.
    """
    sw_c = soup.select_one("main.l-m > .sw > .sw-c") or soup.select_one("main > .sw > .sw-c") or soup.find("main")
    if not sw_c:
        return
    fragment = BeautifulSoup(block_html, "lxml")
    block = fragment.find("div", class_="artide-footer-block")
    if not block:
        return
    # Move each section directly into sw-c so they render exactly like
    # the home page's final sections (not wrapped in an extra div).
    for section in list(block.find_all("section", recursive=False)):
        sw_c.append(section.extract())


def inject_seo_copy(soup: BeautifulSoup, url: str) -> None:
    """Insert keyword-rich intro and outro paragraphs sourced from
    tools/seo_copy.py. Boosts keyword density and adds an internal
    link towards a related page.
    """
    copy = get_seo_copy(url.rstrip("/")) or get_seo_copy(url)
    if not copy:
        return

    # Intro: insert as the first <p> of the first content block right
    # after the page H1.
    h1 = soup.find("h1")
    if h1 is not None:
        intro_p = soup.new_tag("p")
        intro_p["class"] = ["artide-seo-intro"]
        intro_p.string = copy["intro"]
        # Insert right after the H1 (after its parent block when possible)
        target = h1.parent.parent if h1.parent and h1.parent.parent else h1.parent or h1
        target.insert_after(intro_p)

    # ── Outro paragraph + internal link ────────────────────────
    # Append the outro INSIDE the last body section's editor zone so it
    # flows naturally as the closing paragraph of the page (right under
    # the existing CTA / button), instead of living in its own section
    # with extra Webnode spacing. This eliminates the empty band between
    # the page CTA and the footer water image.
    sw_c = soup.select_one("main.l-m > .sw > .sw-c") or soup.select_one("main > .sw > .sw-c") or soup.find("main")
    if sw_c is None:
        return

    p = soup.new_tag("p")
    # Center the closing paragraph regardless of which Webnode section
    # theme it lands in (sc-w, sc-acd, sc-m, …). Accent-dark themes
    # have specific typography rules that override .wnd-align-center,
    # so we ALSO bake an inline style with !important — inline styles
    # win over external CSS unless those use !important AND higher
    # specificity, which Webnode rules don't.
    p["class"] = ["artide-seo-outro__text", "wnd-align-center"]
    p["style"] = (
        "text-align:center !important;"
        "max-width:56rem;"
        "margin-left:auto !important;"
        "margin-right:auto !important;"
        "display:block !important;"
    )
    p.append(soup.new_string(copy["outro"] + " "))
    href, anchor = copy["related"]
    a = soup.new_tag("a", href=abs_path(href if href.endswith("/") else href + "/"))
    a.string = anchor
    a["class"] = ["artide-seo-outro__link"]
    p.append(a)
    p.append(soup.new_string("."))

    # Find the last content section that has a real .ez-c editor zone
    # (i.e. not the decorative bg-image footer or the dark address
    # block). The user wants the outro placed where it was in the
    # mid-page red claim banner, centred. We pick the LAST non-footer
    # content section regardless of theme (sc-w / sc-acd / sc-m all OK)
    # and force centering via inline style (see below) so accent themes
    # cannot override it.
    sections = sw_c.find_all("section", recursive=False)
    body_section = None
    for s in reversed(sections):
        cls = s.get("class") or []
        if "wnd-background-image" in cls or "sc-cd" in cls or "s-hm-hidden" in cls:
            continue
        body_section = s
        break

    if body_section is not None:
        ez_c = body_section.select_one(".ez-c") or body_section.select_one(".s-c")
        if ez_c is not None:
            # Wrap in a Webnode-style block so it inherits the editor
            # spacing (no extra outro section needed).
            block = soup.new_tag("div")
            block["class"] = ["b", "b-text", "cf", "artide-seo-outro-block"]
            block_inner = soup.new_tag("div")
            block_inner["class"] = ["b-c", "b-text-c", "b-cs", "cf"]
            block_inner.append(p)
            block.append(block_inner)
            # Insert IMMEDIATELY AFTER the last meaningful block (skipping
            # any trailing Webnode spacer blocks .b-sp). Without this, the
            # outro lands at the very end past the trailing spacer →
            # huge gap between the CTA above and the outro below.
            from bs4.element import Tag as _Tag
            last_meaningful = None
            for child in reversed(list(ez_c.children)):
                if isinstance(child, _Tag):
                    cls = child.get("class") or []
                    if "b-sp" in cls or "b-sp-placeholder" in cls:
                        continue
                    last_meaningful = child
                    break
            if last_meaningful is not None:
                last_meaningful.insert_after(block)
            else:
                ez_c.append(block)
            return

    # Fallback for pages without a sc-w wnd-w-default body section
    # (e.g. /automazione, /progettazione, /sviluppo-software,
    # /telecontrollo, /corsi which are made entirely of sc-acd claim
    # banners and bg-image sections). Build a clean white panel right
    # before the footer water-image. The outro <p> is wrapped in a
    # full Webnode b-text block chain so its CSS context is identical
    # to a normal body paragraph (centre-aligned, max-width, etc.).
    outro_section = soup.new_tag("section")
    outro_section["class"] = [
        "s", "s-basic", "cf",
        "sc-w", "wnd-w-default", "wnd-s-normal", "wnd-h-auto",
        "artide-seo-outro",
    ]
    s_w = soup.new_tag("div")
    s_w["class"] = ["s-w", "cf"]
    s_c = soup.new_tag("div")
    s_c["class"] = ["s-c", "cf"]
    ez = soup.new_tag("div")
    ez["class"] = ["ez", "cf", "wnd-no-cols"]
    ez_c = soup.new_tag("div")
    ez_c["class"] = ["ez-c"]
    block = soup.new_tag("div")
    block["class"] = ["b", "b-text", "cf", "artide-seo-outro-block"]
    block_inner = soup.new_tag("div")
    block_inner["class"] = ["b-c", "b-text-c", "b-cs", "cf"]
    block_inner.append(p)
    block.append(block_inner)
    ez_c.append(block)
    ez.append(ez_c)
    s_c.append(ez)
    s_w.append(s_c)
    outro_section.append(s_w)

    # Insert just BEFORE the trailing decorative water-image section
    # (wnd-background-image + wnd-w-wider — the full-bleed photo right
    # above the address columns). This is the only reliable anchor for
    # the bottom of the page on every layout. Walking from the END we
    # find that exact section even when other sections of the page also
    # have background images (e.g. /automazione has the hero AND a
    # mid-page bg-image section, both with wnd-background-image; only
    # the trailing one has wnd-w-wider).
    insert_target = None
    for s in reversed(sections):
        cls = s.get("class") or []
        if "wnd-background-image" in cls and "wnd-w-wider" in cls:
            insert_target = s
            break
    # Secondary fallback: insert before the address section (sc-cd).
    if insert_target is None:
        for s in reversed(sections):
            cls = s.get("class") or []
            if "sc-cd" in cls:
                insert_target = s
                break
    if insert_target is not None:
        insert_target.insert_before(outro_section)
    else:
        sw_c.append(outro_section)


def mark_external_links_nofollow(soup: BeautifulSoup) -> None:
    """Set rel='nofollow noopener' on every external <a href>."""
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.startswith(("http://", "https://")):
            continue
        # Internal links that resolve to artide.it self-references stay clean
        if "artide.it" in href or "blasir77.github.io" in href:
            continue
        existing = a.get("rel") or []
        if isinstance(existing, str):
            existing = existing.split()
        rel = set(existing) | {"nofollow", "noopener"}
        a["rel"] = " ".join(sorted(rel))


def inject_overrides(soup: BeautifulSoup, url: str) -> None:
    """Add the body class, base-data attribute, and override CSS/JS tags."""
    body = soup.body
    if body is None:
        return
    # Page-class markers used by the override CSS
    cls = body.get("class", []) or []
    if url == "/":
        cls = list(set(cls + ["is-home"]))
    else:
        cls = [c for c in cls if c != "is-home"]
    body["class"] = cls
    body["data-base"] = BASE  # JS reads this to resolve asset paths

    head = soup.head or soup
    # CSS override (last stylesheet wins)
    css = soup.new_tag("link", rel="stylesheet", href=abs_path("/assets/artide-overrides.css"))
    head.append(css)

    # JS override at end of body
    js = soup.new_tag("script", src=abs_path("/assets/artide-overrides.js"))
    js.attrs["defer"] = "defer"
    body.append(js)


def insert_banner(soup: BeautifulSoup, url: str, h1: str, kw: str) -> None:
    banner = BeautifulSoup(preview_banner_html(url, h1, kw), "lxml")
    # We only want the content (banner div + style), not the html/head/body added by lxml
    # Extract the top-level tags from body (lxml wraps)
    inserted = banner.body.contents[:] if banner.body else []
    for node in reversed(inserted):
        soup.body.insert(0, node.extract() if hasattr(node, "extract") else node)


def derive_blog_seo(title: str, desc: str, h1_current: str) -> dict:
    title = fix_typos(clean_heading(title))
    for suffix in [" | Artide", " - Artide", " :: artide.it", " - artide.it"]:
        if title.endswith(suffix):
            title = title[: -len(suffix)]
    h1 = title if len(title) <= 70 else title[:67] + "…"
    t = title if len(title) <= 55 else title[:52] + "…"
    title_tag = f"{t} | Artide"
    meta = fix_typos(clean_heading(desc or ""))
    if len(meta) > 158:
        meta = meta[:155] + "…"
    if len(meta) < 60:
        meta = f"{h1}. Approfondimento dal blog Artide su case dell'acqua, osmosi inversa e sostenibilità."[:158]
    return dict(h1=h1, title=title_tag, meta=meta,
                kw_primary=BLOG_ARTICLE_DEFAULTS["kw_primary"])


# ─── main ────────────────────────────────────────────────────────

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    # Copy static asset folders verbatim
    for sub in ["files", "cs", "client.fe", "platform", "eli", "vi", "it_IT", "s", "LexUriServ", "gtag", "autoblocking"]:
        src = SRC / sub
        if src.exists():
            shutil.copytree(src, OUT / sub, dirs_exist_ok=True)

    # Copy our design overrides (CSS + JS) from preview-src/ into preview/assets/
    overrides_src = ROOT / "preview-src"
    overrides_dst = OUT / "assets"
    overrides_dst.mkdir(parents=True, exist_ok=True)
    for name in ("artide-overrides.css", "artide-overrides.js"):
        src_file = overrides_src / name
        if src_file.exists():
            shutil.copy2(src_file, overrides_dst / name)

    # Copy favicon folder references — already in 67be54ee… but we use /assets/img/
    # Copy preview/assets from pre-compressed artefacts:
    src_assets = ROOT / "preview.assets-cache"  # unused; we re-run collect below
    # Use the already-built assets in a known location
    # (tools/collect_media.py produces preview/assets; we re-run it here)
    from collect_media import main as collect_main  # type: ignore
    # Not calling; we'll manually copy from the earlier run if present in git.
    # Instead, rebuild the deduped images:
    _rebuild_image_assets()

    # Apply client-supplied image overrides from _assets/overrides/img/.
    # Files dropped here replace same-named files inside preview/assets/img/
    # AFTER compression, so the rebuild step cannot overwrite them.
    overrides_img = ROOT / "_assets/overrides/img"
    if overrides_img.is_dir():
        dest_dir = OUT / "assets/img"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for src_file in overrides_img.iterdir():
            if src_file.is_file():
                shutil.copy2(src_file, dest_dir / src_file.name)
                print(f"  override applied: {src_file.name}")

    # Index original HTMLs → clean URLs
    html_files = sorted(SRC.rglob("index.htm"))

    # Extract a "shared footer block" from the home source: the last two
    # <section class="wnd-background-image"> sections + the final simple
    # address section. The renderer then injects this block into every
    # other page right before <footer class="l-f"> so the bottom of every
    # page looks identical to the home.
    home_path = SRC / "index.htm"
    shared_footer_block_html = ""
    # Safe marker: this exact CTA label only appears on the home page's
    # "La Nostra Storia" section. Using "Arquati" as a marker would
    # wrongly strip content from /chi-siamo, /azienda and /team, which
    # legitimately mention the founding family.
    history_section_text_markers = ("VIENI A SCOPRICI",)
    if home_path.exists():
        home_soup = BeautifulSoup(home_path.read_text(encoding="utf-8", errors="replace"), "lxml")
        rewrite_all_links(home_soup, "/")

        # Drop the "La Nostra Storia" section from the home soup so it
        # never ends up either in the shared footer block or in the
        # rendered home page (per client request).
        for s in home_soup.find_all("section"):
            txt = s.get_text(separator=" ", strip=True)
            if any(m in txt for m in history_section_text_markers):
                s.decompose()

        home_sections = home_soup.find_all("section")
        bg_candidates = []
        for s in home_sections:
            if s.find_parent("footer"):
                continue
            cls = s.get("class") or []
            if any(c.startswith("s-basic") or "wnd-background" in c for c in cls):
                bg_candidates.append(s)
        # Take the LAST 2 sections (decorative bg + address/links columns);
        # the history section is already gone.
        block_sections = bg_candidates[-2:]
        if block_sections:
            wrapper = home_soup.new_tag("div", attrs={"class": "artide-footer-block"})
            for s in block_sections:
                wrapper.append(s)
            shared_footer_block_html = str(wrapper)

    pages_done: list[str] = []
    redirects_written = 0
    for html_path in html_files:
        rel = html_path.relative_to(SRC).as_posix()
        url = url_for_original_file(rel)

        # Consolidated sources: write redirect stub instead
        if url in REDIRECTS:
            dst = REDIRECTS[url]
            dest_href = abs_path(dst if dst.endswith("/") or dst == "/" else dst + "/")
            outp = url_to_outpath(url)
            outp.parent.mkdir(parents=True, exist_ok=True)
            outp.write_text(
                f"""<!doctype html><meta charset="utf-8">
<title>Reindirizzamento…</title>
<meta http-equiv="refresh" content="0; url={dest_href}">
<link rel="canonical" href="{dest_href}">
<p>Questa pagina è stata consolidata in <a href="{dest_href}">{dest_href}</a>.</p>""",
                encoding="utf-8")
            redirects_written += 1
            continue

        # Determine SEO payload
        if url in SEO_MAP:
            seo = dict(SEO_MAP[url])
        elif url.startswith("/l/blog-"):
            # parse original title + desc
            tmp = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "lxml")
            orig_title = tmp.title.get_text() if tmp.title else ""
            md = tmp.find("meta", attrs={"name": "description"})
            orig_desc = md.get("content", "") if md else ""
            h1_orig = tmp.find("h1")
            seo = derive_blog_seo(orig_title, orig_desc, h1_orig.get_text() if h1_orig else "")
        else:
            # Not in the consolidation list but also not in SEO_MAP → skip silently
            continue

        # Render
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "lxml")
        # Remove the legacy home-only "La Nostra Storia" section from
        # every page. The marker is the unique CTA label "VIENI A
        # SCOPRICI" that appears only inside that section on the home.
        for s in list(soup.find_all("section")):
            txt = s.get_text(separator=" ", strip=True)
            if "VIENI A SCOPRICI" in txt:
                s.decompose()

        # Remove Webnode placeholder/demo paragraphs ("Il testo inizia
        # qui…" + Lorem ipsum) found on /produzione-tessere and
        # /erogatore-d-acqua pages.
        DEMO_MARKERS = (
            "Il testo inizia qui",
            "perspiciatis unde omnis iste",
            "Lorem ipsum",
        )
        for s in list(soup.find_all("section")):
            txt = s.get_text(separator=" ", strip=True)
            if any(m in txt for m in DEMO_MARKERS):
                s.decompose()
        apply_seo_patches(soup, seo, url)
        rewrite_all_links(soup, url)
        strip_tracking(soup)
        if url != "/" and shared_footer_block_html:
            inject_shared_footer(soup, shared_footer_block_html)
        inject_seo_copy(soup, url)
        mark_external_links_nofollow(soup)
        inject_overrides(soup, url)
        insert_banner(soup, url, seo["h1"], seo["kw_primary"])

        outp = url_to_outpath(url)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(fix_inline_spacing(str(soup)), encoding="utf-8")
        pages_done.append(url)

    print(f"Generated {len(pages_done)} pages + {redirects_written} redirects → {OUT}/")
    print(f"Base prefix: '{BASE}'")


def _rebuild_image_assets():
    """Deduplicate + compress images into preview/assets/img using tools already written."""
    import subprocess
    env = os.environ.copy()
    subprocess.run([sys.executable, str(ROOT / "tools/collect_media.py")], check=True, env=env)
    subprocess.run([sys.executable, str(ROOT / "tools/compress_images.py")], check=True, env=env)
    # Also rebuild media_map to reflect post-compression .webp
    code = """
import json
from pathlib import Path
ROOT = Path('.')
IMG_SRC = ROOT / '_source/extracted/www.artide.it/67be54ee7dfaae1e955c05a76e69ace8'
IMG_OUT = ROOT / 'preview/assets/img'
actual = {p.stem: p.name for p in IMG_OUT.iterdir() if p.is_file()}
media_map = {}
for f in IMG_SRC.rglob('*'):
    if f.is_file():
        rel = f.relative_to(IMG_SRC)
        id_ = rel.parts[0]
        if id_ in actual:
            src_ref = f'67be54ee7dfaae1e955c05a76e69ace8/{rel.as_posix()}'
            media_map[src_ref] = f'/assets/img/{actual[id_]}'
Path('build/media_map.json').write_text(json.dumps(media_map, ensure_ascii=False, indent=2), encoding='utf-8')
"""
    subprocess.run([sys.executable, "-c", code], check=True)
    # Reload MEDIA_MAP in this process
    global MEDIA_MAP
    MEDIA_MAP = json.loads((ROOT / "build/media_map.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

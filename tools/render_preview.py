"""Generate static HTML preview of all pages using the new theme.

Each page is rendered to preview/<slug>/index.html. Homepage to preview/index.html.
The preview includes:
  - a consistent header/footer (navigation built from the sitemap)
  - proper SEO tags (title, description, canonical) with the rewritten SEO data
  - a banner marking the preview as non-production
  - block-by-block rendering of content from build/pages.json
"""
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = json.loads((ROOT / "build/pages.json").read_text(encoding="utf-8"))
MEDIA = json.loads((ROOT / "build/media_map.json").read_text(encoding="utf-8"))
OUT = ROOT / "preview"
OUT.mkdir(parents=True, exist_ok=True)

# Prefix applied to every absolute site link — useful for GH Pages project
# deployments where the site lives under /REPO_NAME/. Set BASE_PREFIX env var.
BASE = os.environ.get("BASE_PREFIX", "").rstrip("/")


def apply_base(html_text: str) -> str:
    """Prefix BASE to every absolute site path in href/src/content attributes."""
    if not BASE:
        return html_text
    # Skip //, http://, https://, mailto:, tel:, #
    pattern = re.compile(r'(\b(?:href|src|content)=")(/[^"]*)"', re.I)
    def repl(m):
        p = m.group(2)
        # skip //, //protocol-relative
        if p.startswith("//"):
            return m.group(0)
        return f'{m.group(1)}{BASE}{p}"'
    return pattern.sub(repl, html_text)

# ── Primary navigation ───────────────────────────────────────────
NAV = [
    ("Case dell'Acqua", "/casa-dell-acqua"),
    ("Erogatori", "/erogatore-d-acqua"),
    ("Servizi", "/servizi"),
    ("Certificazioni", "/certificazioni"),
    ("Chi siamo", "/chi-siamo"),
    ("Blog", "/blog"),
    ("Contatti", "/contatti"),
]

FOOTER_COLS = [
    ("Prodotti", [
        ("Case dell'Acqua", "/casa-dell-acqua"),
        ("Collezione", "/casa-dell-acqua-collezione"),
        ("Erogatori", "/erogatore-d-acqua"),
        ("Totem pagamento", "/totem-casa-dell-acqua"),
        ("Tutti i prodotti", "/prodotti"),
    ]),
    ("Servizi", [
        ("Manutenzione", "/manutenzione"),
        ("Telecontrollo", "/telecontrollo"),
        ("Progettazione", "/progettazione"),
        ("Riqualificazione", "/trasformazione"),
        ("Sanificazione", "/sanificazione"),
    ]),
    ("Azienda", [
        ("Chi siamo", "/chi-siamo"),
        ("Team", "/team"),
        ("Certificazioni", "/certificazioni"),
        ("Wiki", "/wiki"),
        ("FAQ", "/faq-casa-dell-acqua"),
    ]),
]


def resolve_img(src: str) -> str | None:
    if not src:
        return None
    # Strip query string; media_map keys don't include ?ph=...
    key = src.split("?")[0]
    return MEDIA.get(key)


def render_blocks(blocks: list, page_url: str) -> str:
    """Render the list of blocks. The first heading level-1 is skipped because
    the page header already renders the H1."""
    parts = []
    skipped_h1 = False
    in_prose = False

    def open_prose():
        nonlocal in_prose
        if not in_prose:
            parts.append('<div class="prose">')
            in_prose = True

    def close_prose():
        nonlocal in_prose
        if in_prose:
            parts.append('</div>')
            in_prose = False

    for b in blocks:
        t = b["type"]
        if t == "heading":
            if b["level"] == 1 and not skipped_h1:
                skipped_h1 = True
                continue
            lvl = min(max(b["level"], 2), 4)
            close_prose()
            parts.append(f'<h{lvl}>{html.escape(b["text"])}</h{lvl}>')
        elif t == "paragraph":
            open_prose()
            parts.append(f'<p>{html.escape(b["text"])}</p>')
        elif t == "list":
            open_prose()
            tag = "ol" if b.get("ordered") else "ul"
            items = "".join(f'<li>{html.escape(i)}</li>' for i in b["items"])
            parts.append(f'<{tag}>{items}</{tag}>')
        elif t == "image":
            close_prose()
            resolved = resolve_img(b["src"])
            if resolved:
                alt = html.escape(b.get("alt") or "")
                parts.append(f'<figure class="figure"><img src="{resolved}" alt="{alt}" loading="lazy"/></figure>')
        elif t == "cta":
            close_prose()
            href = b.get("href") or "#"
            if isinstance(href, str) and href.startswith("/") and not href.endswith("/"):
                href = href + "/"
            parts.append(f'<div style="margin:2rem 0"><a class="btn btn-primary" href="{html.escape(href)}">{html.escape(b["text"])}</a></div>')
    close_prose()
    return "".join(parts)


def render_nav(current_url: str) -> str:
    items = []
    for label, href in NAV:
        cls = ' class="is-active"' if current_url == href or current_url.startswith(href + "/") else ""
        items.append(f'<li><a href="{href}/"{cls}>{label}</a></li>')
    return f'<nav class="site-nav"><ul>{"".join(items)}</ul></nav>'


def render_footer() -> str:
    cols_html = ""
    for title, items in FOOTER_COLS:
        li = "".join(f'<li><a href="{href}/">{label}</a></li>' for label, href in items)
        cols_html += f'<div><h4>{title}</h4><ul>{li}</ul></div>'
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="site-brand" style="color:#fff">Artide</div>
        <p style="margin-top:1rem;max-width:28em;opacity:0.85">
          Produttore italiano di case dell'acqua ed erogatori con osmosi inversa.
          Dal 2003 progettiamo, produciamo e manuteniamo soluzioni per comuni, aziende e mense.
        </p>
      </div>
      {cols_html}
    </div>
    <div class="fine">
      <div>© Artide srl — P.IVA 00000000000 — Tutti i diritti riservati</div>
      <div>
        <a href="/informativa-privacy/">Privacy</a> &middot;
        <a href="/info-copyright/">Copyright</a> &middot;
        <a href="/legal-content/">Note legali</a>
      </div>
    </div>
  </div>
</footer>"""


def breadcrumb(url: str, h1: str) -> str:
    if url == "/":
        return ""
    parts = [p for p in url.split("/") if p]
    items = ['<a href="/">Home</a>']
    for i, p in enumerate(parts):
        if i == len(parts) - 1:
            items.append(f'<span>{html.escape(h1[:50])}</span>')
        else:
            sub = "/" + "/".join(parts[: i + 1]) + "/"
            items.append(f'<a href="{sub}">{html.escape(p.replace("-", " ").title())}</a>')
    sep = '<span class="sep">›</span>'
    return f'<div class="breadcrumb container">{sep.join(items)}</div>'


def render_home(page: dict) -> str:
    blocks_html = render_blocks(page["blocks"], page["url"])
    # Hero + stats strip baked in for the home template
    return f"""
<section class="hero">
  <div class="container hero-inner">
    <div>
      <div class="eyebrow">Produttore italiano dal 2003</div>
      <h1>{html.escape(page["h1"])}</h1>
      <p class="lead">{html.escape(page["meta"])}</p>
      <div class="hero-cta-row">
        <a class="btn btn-primary" href="/casa-dell-acqua/">Scopri le case dell'acqua</a>
        <a class="btn btn-secondary" href="/contatti/">Richiedi un preventivo</a>
      </div>
    </div>
    <div>
      <img src="/assets/img/200000013-d7e63d7e66.webp" alt="Casa dell'acqua Artide" onerror="this.style.display='none'">
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="stats">
      <div><span class="stat-num">20+</span><span class="stat-label">Anni di esperienza</span></div>
      <div><span class="stat-num">13</span><span class="stat-label">Modelli di case dell'acqua</span></div>
      <div><span class="stat-num">300+</span><span class="stat-label">Case dell'acqua installate</span></div>
      <div><span class="stat-num">240k</span><span class="stat-label">Litri erogati al giorno</span></div>
    </div>
    {blocks_html}
  </div>
</section>
"""


def render_hub(page: dict, card_urls: list[tuple[str, str, str]]) -> str:
    """card_urls: list of (url, title, desc)."""
    cards = ""
    for url, title, desc in card_urls:
        cards += f'''<a href="{url}/" class="card" style="text-decoration:none;color:inherit">
          <h3>{html.escape(title)}</h3>
          <p>{html.escape(desc)}</p>
          <span class="card-link">Vai alla pagina</span>
        </a>'''
    blocks_html = render_blocks(page["blocks"], page["url"])
    return f"""
{page_header(page)}
<section class="section">
  <div class="container">
    {blocks_html}
    <div class="card-grid">{cards}</div>
  </div>
</section>
"""


def page_header(page: dict) -> str:
    eyebrow = ""
    tmpl = page.get("template", "")
    label = {
        "service": "Servizio",
        "product": "Prodotto",
        "certification": "Certificazione",
        "article": "Blog",
        "article_archive": "Blog",
        "about": "Azienda",
        "legal": "Informativa",
        "faq": "FAQ",
        "wiki": "Wiki",
        "team": "Team",
        "contact": "Contatti",
        "hub": "Panoramica",
    }.get(tmpl, "")
    if label:
        eyebrow = f'<div class="eyebrow">{label}</div>'
    return f"""
<header class="page-header">
  <div class="container">
    {eyebrow}
    <h1>{html.escape(page["h1"])}</h1>
    <p class="lead">{html.escape(page["meta"])}</p>
  </div>
</header>
{breadcrumb(page["url"], page["h1"])}
"""


def render_default(page: dict) -> str:
    return f"""
{page_header(page)}
<section class="section">
  <div class="container">
    {render_blocks(page["blocks"], page["url"])}
  </div>
</section>
"""


def page_html(page: dict, body: str) -> str:
    canonical = page["url"]
    if canonical == "/":
        canonical = "/"
    elif not canonical.endswith("/"):
        canonical += "/"
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page["title"])}</title>
<meta name="description" content="{html.escape(page["meta"])}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(page["title"])}">
<meta property="og:description" content="{html.escape(page["meta"])}">
<meta property="og:url" content="{canonical}">
<meta name="generator" content="Artide preview (pre-WordPress)">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<div class="preview-banner">
  <b>⚠ Anteprima non definitiva</b> — versione SEO-optimized pronta per la conversione in tema WordPress.
  Pagina: <code>{html.escape(page["url"])}</code> · Keyword: <b>{html.escape(page["kw_primary"])}</b>
</div>
<header class="site-header">
  <div class="container">
    <a href="/" class="site-brand">Artide</a>
    {render_nav(page["url"])}
    <a class="header-cta" href="/contatti/">Preventivo</a>
  </div>
</header>
<main>
{body}
</main>
{render_footer()}
</body>
</html>
"""


# ── Hub card sources ────────────────────────────────────────────
HUB_CARDS = {
    "/prodotti": [
        ("/casa-dell-acqua", "Case dell'Acqua", "Erogatori pubblici con osmosi inversa per comuni e aziende"),
        ("/casa-dell-acqua-collezione", "Collezione", "Oltre 13 modelli: urbani, compatti, a incasso"),
        ("/totem-casa-dell-acqua", "Totem di pagamento", "Ricarica tessere e pagamento contactless"),
        ("/erogatore-d-acqua", "Erogatori d'acqua", "Per mense, uffici e condomini"),
    ],
    "/servizi": [
        ("/manutenzione", "Manutenzione", "Contratti full-service con garanzia a vita"),
        ("/telecontrollo", "Telecontrollo", "Gestione remota 24/7 di tutti gli impianti"),
        ("/progettazione", "Progettazione", "Case dell'acqua su capitolato comunale"),
        ("/sanificazione", "Sanificazione", "Protocolli HACCP e ISO 22000"),
        ("/trasformazione", "Riqualificazione", "Revamping di case dell'acqua esistenti"),
        ("/sviluppo-software", "Software", "Piattaforma proprietaria di telecontrollo"),
        ("/automazione", "Automazione", "PLC e sensoristica industriale"),
        ("/potabilizzazione", "Potabilizzazione", "Impianti a osmosi inversa per acquedotti"),
        ("/corsi", "Corsi", "Formazione per operatori e tecnici"),
        ("/produzione-tessere", "Tessere RFID", "Badge personalizzati per utenze"),
        ("/incasso", "Incasso contante", "Gestione cassa conforme antiriciclaggio"),
        ("/assistenza", "Assistenza", "Numero verde e knowledge base"),
    ],
    "/certificazioni": [
        ("/iso-9001", "ISO 9001", "Sistema qualità aziendale certificato"),
        ("/iso-14001", "ISO 14001", "Gestione ambientale certificata"),
        ("/iso-22000", "ISO 22000", "Sicurezza alimentare HACCP"),
        ("/ce", "Marcatura CE", "Conformità direttive UE"),
        ("/moca", "MOCA", "Materiali a contatto con alimenti"),
        ("/rohs", "RoHS", "Sostanze pericolose vietate"),
        ("/osa", "OSA", "Operatore Settore Alimentare"),
        ("/aiaq", "AIAQ", "Associazione Acque Italiane di Qualità"),
        ("/gestore-ambientale", "Gestori Ambientali", "Iscrizione Albo Nazionale"),
    ],
    "/wiki": [
        ("/wiki-casa-dell-acqua", "Wiki Casa dell'Acqua", "Guide e manuali operativi"),
        ("/wiki-totem-pagamento", "Wiki Totem", "Documentazione sul totem di pagamento"),
        ("/faq-casa-dell-acqua", "FAQ", "Domande frequenti sulle case dell'acqua"),
        ("/citazioni-bibliografiche", "Citazioni", "Fonti e riferimenti scientifici"),
    ],
}


def main():
    # Index blog articles separately
    blog_articles = [p for p in PAGES if p["template"] == "article"]

    for page in PAGES:
        tmpl = page["template"]
        if tmpl == "home":
            body = render_home(page)
        elif tmpl == "hub" and page["url"] in HUB_CARDS:
            body = render_hub(page, HUB_CARDS[page["url"]])
        elif tmpl == "article_archive":
            # Render /blog with a list of articles
            cards = "".join(
                f'<a href="{a["url"]}/" class="card" style="text-decoration:none;color:inherit">'
                f'<h3>{html.escape(a["h1"])}</h3>'
                f'<p>{html.escape(a["meta"][:140])}</p>'
                f'<span class="card-link">Leggi l\'articolo</span>'
                f'</a>'
                for a in blog_articles
            )
            body = f"""
{page_header(page)}
<section class="section">
  <div class="container">
    <div class="card-grid">{cards}</div>
  </div>
</section>"""
        else:
            body = render_default(page)

        # Write file
        if page["url"] == "/":
            out = OUT / "index.html"
        else:
            out = OUT / page["url"].lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(apply_base(page_html(page, body)), encoding="utf-8")

    # Write redirect stubs for consolidated URLs
    redirects = json.loads((ROOT / "build/redirects.json").read_text(encoding="utf-8"))
    for r in redirects:
        src = r["from"]
        dst = r["to"]
        out = OUT / src.lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        dest_href = dst if dst.endswith("/") or dst == "/" else dst + "/"
        out.write_text(apply_base(f"""<!doctype html><meta charset="utf-8">
<title>Reindirizzamento…</title>
<meta http-equiv="refresh" content="0; url={dest_href}">
<link rel="canonical" href="{dest_href}">
<p>Questa pagina è stata consolidata in <a href="{dest_href}">{dest_href}</a>."""),
                         encoding="utf-8")

    print(f"Rendered {len(PAGES)} pages + {len(redirects)} redirects → {OUT}/")


if __name__ == "__main__":
    main()

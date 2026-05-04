# Nuovo sito artide.it — Progetto WordPress

Questo repository contiene tutto il materiale per ricostruire **www.artide.it** su WordPress con contenuti SEO-ottimizzati.

## Preview navigabile

Il ramo `main` contiene una **preview statica** del nuovo sito in `preview/`. Per vederla:

1. Abilita GitHub Pages: _Settings → Pages → Source: `main` branch, folder `/preview`_
2. Apri `https://blasir77.github.io/artide.it/`
3. Naviga le pagine come un vero sito

## Struttura del repository

```
tools/                # Script Python che generano la preview
  extract.py          # Parsa gli HTML Webnode originali → content.json
  rewrite.py          # Applica SEO rewrite → pages.json
  seo_map.py          # Mappa URL → H1/title/meta/keyword
  collect_media.py    # Seleziona 1 variante per immagine
  compress_images.py  # Comprime le immagini per la preview
  render_preview.py   # Genera HTML statico navigabile

build/                # Artefatti intermedi (JSON)
  content.json        # Contenuti estratti dal vecchio sito
  pages.json          # Pagine SEO-clean pronte per WP
  seo-map.csv         # Tabella di revisione SEO
  redirects.json      # Mapping vecchie URL → nuove URL consolidate
  media_map.json      # Mapping immagini originali → preview

preview/              # Output statico (servito da GitHub Pages)
  index.html          # Home
  <slug>/index.html   # Tutte le altre pagine
  assets/style.css    # Tema CSS
  assets/img/*.webp   # Immagini compresse per preview

skills/wordpress-pro/ # Skill Claude Code per sviluppare il tema WP
```

## Tabella SEO

Vedi `build/seo-map.csv` — una riga per pagina con H1, title, meta description e keyword primaria target.

## Prossimi step

1. Revisione grafica della preview (in corso)
2. Conversione a tema WordPress custom `artide`
3. Plugin installer con contenuti + media + menu
4. Pacchetto `.wpress` pronto per upload su SiteGround
5. Guida setup passo-passo

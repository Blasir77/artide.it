# Artide — Migrazione a WordPress: Stato del Progetto

> Documento di handoff per riprendere il lavoro in nuova sessione.
> Ultimo aggiornamento: 09/05/2026

---

## 1. Contesto del progetto

**Obiettivo**: migrare il sito Artide (`artide.it`) da Webnode a WordPress, replicando il design del preview esistente e aggiungendo supporto multilingua.

**Riferimento visivo**:
- Preview deployato: `https://blasir77.github.io/artide.it/`
- Sorgente preview locale: `preview/index.html` + `preview/<slug>/index.html`
- CSS/JS di riferimento Webnode→Artide: `preview-src/artide-overrides.css` e `preview-src/artide-overrides.js`

---

## 2. Ambiente di lavoro

| Risorsa | Valore |
|---|---|
| Repository | `Blasir77/artide.it` |
| Branch attivo | `claude/fix-wordpress-api-error-DaxZ9` |
| Server WP staging | `https://37.156.244.26/~artide1/` |
| Hosting | Vhosting (verificato) |
| WP version | 6.9.4 |
| Tema attivo | **Kadence** |

---

## 3. Plugin installati

| Plugin | Stato | Note |
|---|---|---|
| Advanced Custom Fields | Attivo | Default tema |
| Better Search Replace | Attivo | Per migrazione URL |
| Importatore WordPress | Attivo | Usato per import XML |
| JetBackup | Attivo | Backup |
| Kadence Blocks | Attivo | Blocchi pagina builder |
| LiteSpeed Cache | Attivo | Cache |
| **MetaSlider Slideshow** | Attivo | Hero slider home (ID **162**) |
| Redirection | Attivo | Per redirect 301 (da configurare) |
| Starter Templates by Kadence | Attivo | Template starter |
| WP Mail SMTP | Attivo | Email SMTP |
| Yoast SEO | Attivo | SEO (2 notifiche pendenti) |
| **Polylang** | Attivo | Multilingua IT/EN/FR/DE/ES |

---

## 4. Configurazione Header Kadence

### TOP ROW (riga bianca topbar)

- **Layout**: Standard
- **Altezza**: 38 px
- **Sfondo**: `#ffffff` (bianco)
- **Padding**: 0 / 30 / 0 / 30 px (top/right/bottom/left)
- **Sticky on scroll**: Attivo (Top + Main)

**Contenuto sinistra** — blocco **Social** (orientamento orizzontale):
- Facebook → `https://www.facebook.com/artideparma`
- Twitter/X → `https://www.twitter.com/artideparma`
- Instagram → `https://www.instagram.com/artideparma`
- LinkedIn → `https://www.linkedin.com/company/77855658`
- Pinterest → `https://www.pinterest.it/artidesrl/`
- TikTok → `https://www.tiktok.com/@artideparma`
- YouTube → `https://www.youtube.com/@Artidesrl`
- Stile: PIENO, no etichette, dimensione 0.9em
- Colori: Normale `#bebebe`, Hover `#666666`
- Sfondo: trasparente
- Border: nessuno

**Contenuto destra** — blocco **HTML** con stili inline (CSS Aggiuntivo / `<style>` filtrati da Kadence, quindi inline):
```
⏱ Lun ~ Ven | 9:30~12:00 | 14:30~16:00
✉︎ info@artide.info (rosso #ee1515 sottolineato)
☏ 0521 833 702 (grigio)
```
- Caratteri Unicode con variation selector `&#xFE0E;` per forzare rendering testo (non emoji)

### MAIN ROW (riga rossa con logo + menu)

- **Layout**: Standard
- **Altezza**: 90 px
- **Sfondo**: `#ee1515` (rosso Artide)
- **Padding**: 0 / 30 / 0 / 30 px

### Header trasparente in home

Configurazione speciale: in homepage, header completamente trasparente al top, materializza al scroll/hover. Topbar bianca SEMPRE visibile (anche al top in home).

---

## 5. Menu navigazione

**Nome**: `Menu Principale Artide`
**Posizione**: Primario
**ID**: 0 (default)

### Struttura (ordine post-JS overrides preview)

1. **PRODOTTI** → `/prodotti/`
   - Casa dell'Acqua → `/casa-dell-acqua/`
     - Collezione → `/casa-dell-acqua-collezione/`
     - FAQ → `/faq-casa-dell-acqua/`
2. **SERVIZI** → `/servizi/`
   - Automazione, Corsi di Formazione, Manutenzione, Incasso, Potabilizzazione, Progettazione, Riqualificazione (`/trasformazione/`), Sanificazione, Sviluppo Software, Telecontrollo
3. **AZIENDA** → `/chi-siamo/`
   - Contatti, Chi Siamo
   - Certificazioni → `/certificazioni/`
     - AIAQ, CE, DM174-DM25-MOCA, Gestore Ambientale, ISO 9001, ISO 14001, ISO 22000, OSA, RoHS
   - Info & Copyright, Informativa Privacy, Citazioni Bibliografiche, Il Team
4. **BLOG** → `/blog/`
   - Articoli del Blog, Articoli in Evidenza
5. **CONTATTI** → `/contatti/`

### Voci RIMOSSE dal menu (presenti nel preview HTML ma nascoste dal JS):
- HOME (la home si raggiunge dal logo)
- SUPPORTO
- WIKI, WIKI - Totem Ricarica, WIKI - Casa dell'Acqua

### Comportamento sottomenu
- Sfondo: nero `#000000`
- Hover: `#1a1a1a`
- Testo: bianco `#ffffff`
- Text-transform: UPPERCASE (via CSS Aggiuntivo)

---

## 6. Hero Slider home (MetaSlider)

**ID**: **162**
**Tipo**: Flex Slider
**Shortcode**: `[metaslider id="162"]`

### Configurazione
| Parametro | Valore |
|---|---|
| Effetto | Dissolvenza (fade) |
| Ritardo tra slide | 15000 ms (15s) |
| Velocità transizione | 800 ms |
| Riproduzione automatica | ON |
| Larghezza 100% | ON |
| Altezza | 700 px (override CSS a `calc(100vh - 38px)`) |
| Frecce | Nascoste |
| Navigazione | Punti |

### Slide attive (2 di 5 previste)

| # | Eyebrow | Titolo | CTA | Immagine |
|---|---|---|---|---|
| 1 | Produttore italiano dal 2003 | Case dell'Acqua ed erogatori con osmosi inversa | Scopri le Case dell'Acqua → `/casa-dell-acqua/` | artide-hero-1-case-acqua.webp |
| 2 | Più di 300 impianti installati | La casa dell'acqua come elemento d'arredo urbano | Vedi la collezione → `/casa-dell-acqua-collezione/` | artide-hero-2-collezione.webp |

### Slide DA AGGIUNGERE (file già nel repo `wp-assets/hero/`)
- 3: Manutenzione 24/7 / Garanzia a vita / `/manutenzione/`
- 4: Erogatori per mense / Acqua microfiltrata / `/erogatore-d-acqua/`
- 5: Riqualificazione impianti / Ridiamo vita... / `/trasformazione/`

### Caption HTML format usato
```html
<div class="hero-caption">
<span class="hero-eyebrow">[eyebrow text]</span>
<h1 class="hero-title">[title]</h1>
<p class="hero-subtitle">[subtitle]</p>
<a class="hero-cta" href="[url]">[cta label]</a>
</div>
```

---

## 7. Pagina Home — sezioni costruite

Tutte costruite via Gutenberg block markup (incollato in modalità Editor di codice), `Ctrl+Shift+Alt+M`.

### B1 — "Artide offre un prodotto"
- contentSize: 900px
- Eyebrow rosso `#ee1515`, H1 nero, paragrafo con bold "Garanzia a VITA" + link `/manutenzione/`

### B2 — "Sempre in Crescita" stats
- contentSize: 1200px
- Eyebrow rosso, H2 grande
- 4 colonne stats:
  - OLTRE 20 / ANNI DI ESPERIENZA
  - OLTRE 13 MODELLI / DI CASE DELL'ACQUA
  - OLTRE 300 / CASE DELL'ACQUA PRODOTTE
  - OLTRE 240.000 / LITRI EROGATI AL GIORNO
- Headings sotto numeri: NERI (`#1a1a1a`), non rossi
- Paragrafi: allineati a sinistra (NON justified)

### B3 — "Cosa Facciamo" 4 aree con icone
- contentSize: 1100px
- Griglia 2×2 con icone SVG inline rosse (#ee1515)
- Aree: Produzione Case dell'Acqua + Manutenzione ATTIVA + Riqualificazione + Acqua NON Potabile

### B4 — "Alcuni dei Nostri Clienti" testimonials
- contentSize: 1100px
- Eyebrow rosso, H2 "Alcuni dei Nostri Clienti"
- Widget ElfSight Reviews carousel con ID `97727eb7-85bf-41af-adba-3258dc304026` (stesso del preview, account ElfSight Artide)

### Separatori HR tra sezioni
- HTML diretto con `max-width: 1100px; margin: 0 auto;` (NON full-width)
- Colore `#e5e5e5`

---

## 8. Footer Kadence

### Footer Top Row (5 colonne)
- Layout: 5 colonne uguali
- Sfondo: `#0e0e10` (nero leggermente bluastro come preview)
- Padding: 60px top / 60px bottom / 40px L/R
- Spaziatura colonne: 40px
- Spaziatura widget: 30px
- Direzione colonna: COLONNA
- Colori link: bianco `#ffffff` (normale), oro `#ffba1b` (hover)

### Widget area contenuti

**Widget 1 — Artide srl info**:
- "Artide" `#ffba1b` 20px, "srl" piccolo 13px
- Indirizzo, telefono in **ORO** `#ffba1b` 18px
- Email/PEC/P.IVA in bianco bold

**Widget 2 — Servizi**: Manutenzione, Sanificazione, Gestione Incasso, Riqualificazione (link bianchi sottolineati)

**Widget 3 — Prodotti**: Casa dell'Acqua, Erogatore, Tessere, Totem (link bianchi sottolineati; quelli senza pagina rimandano a `/prodotti/`)

**Widget 4 — Site Link** (heading sottolineato): Contatti, Blog, Privacy Policy, Info sul Copyright

**Widget 5 — Ultime News dal Blog**: titolo articolo "Inaugura la 4° Casa dell'Acqua a RHO (MI)" + data 09.05.2025 corsivo

### Footer Bottom Row (Copyright)
- Già con elemento Copyright Kadence
- Testo: `<span style="color:#cccccc;">quanto contenuto nel sito è protetto da Copyright 2026, Tutti i diritti sono riservati</span> &nbsp;•&nbsp; <a href="https://www.iubenda.com/privacy-policy/29512787" ...>Privacy Policy</a> &nbsp;•&nbsp; <a href="https://www.iubenda.com/privacy-policy/29512787/cookie-policy" ...>Cookie Policy</a>`
- Privacy/Cookie Policy: BIANCHI sottolineati (override CSS Aggiuntivo per evitare oro inherit da `--ac-color`)
- iubenda account ID: **29512787** (di Artide)

### Linea "Artide srl © 2022 | ... | P.IVA"
- **NASCOSTA via JS preview**, NON inserita in WP per scelta cliente

---

## 9. CSS Aggiuntivo (Personalizza → CSS Aggiuntivo)

Sezioni principali presenti:
1. Sottomenu in MAIUSCOLO
2. Home: TOP ROW sempre visibile bianca
3. Home: LOGO invisibile al top
4. Home: MENU items invisibili al top
5. Scroll (sticky): tutto torna visibile
6. Hover sull'header: tutto si materializza
7. Slider altezza viewport (`calc(100vh - 38px)`)
8. Caption hero (eyebrow, title, subtitle, CTA con text-shadow per leggibilità)
9. Sfondo MAIN ROW rosso completo (no gap tra menu items)
10. Sottomenu sempre NERO (override broad selectors)
11. Footer hover oro
12. Privacy/Cookie iubenda link bianchi (override `--ac-color: gold`)

---

## 10. Multilingua (Polylang)

### Lingue configurate
| Codice | Nome | Default | Articoli |
|---|---|---|---|
| `it_IT` | Italiano | ⭐ Sì | 33 |
| `en_GB` | English | No | 1 |
| `fr_FR` | Français | No | 1 |
| `de_DE` | Deutsch | No | 1 |
| `es_ES` | Español | No | 1 |

### Configurazione moduli Polylang
- **Modifiche dell'URL**:
  - "La lingua viene impostata dal nome della directory nei pretty permalink" ✓
  - "Nascondi le informazioni relative alla lingua dall'URL per la lingua predefinita" ✓ (IT senza `/it/`)
  - "Rimuovi `/language/` dai pretty permalink" ✓
- **Individua la lingua del browser**: Attivo
- **Media**: Attivo (traduzione metadata)
- **Sincronizzazione** (campi sync tra lingue):
  - ✅ Tassonomie, Pagina genitore, Ordine pagine, Immagine in evidenza
  - ❌ Titolo, Contenuto, Estratto (vanno tradotti)
- **Switcher di lingua**: NON nel menu principale (rimosso). Da implementare in topbar.

### URL structure attesa
- IT: `artide.it/chi-siamo/` (no prefisso)
- EN: `artide.it/en/chi-siamo/`
- FR: `artide.it/fr/chi-siamo/`
- DE: `artide.it/de/chi-siamo/`
- ES: `artide.it/es/chi-siamo/`

---

## 11. Pagine WordPress importate (33 totali)

Importate via XML (`artide-import.xml`) con slug matching live site:

**Servizi (10)**: automazione, corsi, manutenzione, incasso, potabilizzazione, progettazione, trasformazione, sanificazione, sviluppo-software, telecontrollo

**Azienda (4)**: chi-siamo, info-copyright, informativa-privacy, citazioni-bibliografiche, team

**Certificazioni (10)**: certificazioni (parent), aiaq, ce, moca, gestore-ambientale, iso-9001, iso-14001, iso-22000, osa, rohs

**Prodotti (4)**: prodotti (parent), casa-dell-acqua, casa-dell-acqua-collezione, faq-casa-dell-acqua

**Altri (5)**: home, blog, contatti, servizi (parent)

### Stato contenuti pagine
- Tutte le pagine hanno **testo grezzo** (H1 + paragrafi) auto-estratto dal preview
- Manca: **immagini, formattazione, layout** (in fase di completamento)

---

## 12. Asset generati nel repo

```
wp-assets/
├── hero/                              5 immagini hero slider
│   ├── artide-hero-1-case-acqua.webp
│   ├── artide-hero-2-collezione.webp
│   ├── artide-hero-3-manutenzione.webp
│   ├── artide-hero-4-erogatori.webp
│   └── artide-hero-5-riqualificazione.webp
└── page-markup/                       22 file Gutenberg markup pagine semplici
    ├── README.md
    ├── chi-siamo.html
    ├── iso-9001.html, iso-14001.html, iso-22000.html
    ├── aiaq.html, ce.html, moca.html, osa.html, rohs.html
    ├── gestore-ambientale.html
    ├── info-copyright.html, citazioni-bibliografiche.html
    ├── manutenzione.html, automazione.html, sanificazione.html
    ├── incasso.html, potabilizzazione.html, progettazione.html
    ├── sviluppo-software.html, telecontrollo.html, corsi.html
    └── trasformazione.html

tools/
├── generate_wp_import.py     Genera artide-import.xml (33 pagine + menu)
└── generate_page_markup.py   Genera markup Gutenberg per pagine semplici

artide-import.xml              File XML import WordPress (versionato)
```

URLs raw immagini (per `<img src>` in markup):
`https://raw.githubusercontent.com/Blasir77/artide.it/claude/fix-wordpress-api-error-DaxZ9/preview/assets/img/<filename>`

---

## 13. Decisioni architetturali prese

| Decisione | Rationale |
|---|---|
| **Kadence** come tema | Free, page builder integrato, Header/Footer builder potenti |
| **MetaSlider Free** per hero | Plugin più popolare, 5 slide + autoplay 15s + fade transition copre il preview al 85% |
| **Slider 2 slide** invece di 5 | Test iniziale, poi user espanderà a 5 |
| **NO porting `artide-overrides.css/js`** as-is | Scritti per Webnode (`.l-h .s-hn`), non Kadence — incompatibili. Ricostruzione nativa Kadence Blocks. |
| **Polylang Free** invece di Pro/WPML | Gratuito, copre IT+EN+FR+DE+ES. Pro solo se servono shortcode/translate-slugs (non urgente). |
| **5 lingue** invece di 2 | Per SEO internazionale (B2B mercato europeo). Cinese rimosso (richiederebbe traduttore madrelingua). |
| **Sottocartelle `/en/` `/fr/` ecc.** | SEO friendly, no DNS, IT mantiene URL identico al live (zero impatto SEO esistente) |
| **ElfSight widget recensioni** stesso ID preview | Account ElfSight Artide già configurato con Google Reviews; widget ID `97727eb7-85bf-41af-adba-3258dc304026` |
| **Footer link → ORO `#ffba1b`** | Per richiesta cliente (override esplicito in preview-src CSS riga 1140-1146) |
| **Linea "Artide srl © 2022"** nascosta | Nascosta nel preview per richiesta cliente (`footer.l-f .s-f-cr { display: none }`) |
| **Switcher lingua in TOPBAR** invece che menu | Scelta UX: topbar bianca è più discreta, non sovraccarica menu rosso |

---

## 14. URL legacy live → setup redirect 301

Dopo go-live, configurare in **Strumenti → Redirection** (plugin già installato):

| URL vecchio | Punta a |
|---|---|
| `/assistenza/` | `/contatti/` |
| `/azienda/` | `/chi-siamo/` |
| `/blog-articoli/` | `/blog/` |
| `/blog-articoli-in-evidenza/` | `/blog/` (o creare pagina dedicata) |
| `/supporto/` | `/contatti/` |
| `/wiki/` | `/contatti/` |
| `/wiki-casa-dell-acqua/` | `/contatti/` |
| `/wiki-totem-pagamento/` | `/contatti/` |

**Importante**: i 33 slug WP corrispondono già 1:1 ai live URL → ZERO link rotti per pagine esistenti.

---

## 15. Stato a oggi e prossimi passi

### ✅ Completato
- Header completo (topbar + main row + comportamento trasparenza home)
- Menu navigazione 5 voci con sottomenu nidificati 3 livelli
- Hero slider 2 slide con caption custom
- Home: 4 sezioni complete (B1 + B2 + B3 + B4) con ElfSight reviews
- Footer 5 colonne + copyright iubenda
- Import 33 pagine WP (testo grezzo)
- Polylang installato e configurato per 5 lingue
- 22 markup Gutenberg pre-generati per pagine semplici

### 🔲 Da fare (in ordine di priorità)

#### Priorità ALTA — completamento contenuti IT
1. **Incollare i 22 markup Gutenberg** nelle pagine IT (lavoro user, ~1h)
2. **Pagine custom layout** (richiedono lavoro mirato):
   - `prodotti` — bento grid asimmetrica
   - `casa-dell-acqua` + `casa-dell-acqua-collezione` — gallery prodotto
   - `team` — griglia 16 membri con foto
   - `faq-casa-dell-acqua` — accordion 14 domande
   - `contatti` — form + mappa
3. **Aggiungere 3 slide mancanti** allo slider hero (3, 4, 5)

#### Priorità MEDIA — multilingua + functional
4. **Switcher lingua nella TOPBAR** (non nel menu) — Code Snippets PHP o widget area Kadence
5. **Traduzione strings struttura**: header topbar testi, footer widget HTML, copyright, slider caption
6. **Duplicazione pagine IT in EN/FR/DE/ES** via Polylang (creazione struttura, contenuti tradotti dopo)
7. **Form contatti** funzionante (WPForms Lite o Contact Form 7)

#### Priorità BASSA — pre-launch
8. **Yoast SEO**: completare 2 notifiche pendenti, configurare meta description e Open Graph per ogni pagina
9. **Ottimizzazione performance**: compressione immagini, regole LiteSpeed Cache
10. **Test mobile**: responsive check di tutte le sezioni (header sticky, slider 100vh, stats 4-col, footer 5-col)
11. **Pre-launch QA**: link checker, test form, test browser
12. **Go-live**: cambio dominio, SSL, redirect 301 (8 regole listate sopra), Google Search Console + Analytics

---

## 16. File da consultare per continuare

| File | Per cosa |
|---|---|
| `preview/index.html` | Riferimento home (struttura, testi) |
| `preview/<slug>/index.html` | Riferimento pagine interne |
| `preview-src/artide-overrides.css` | Stili custom Artide (colori, layout, brand) |
| `preview-src/artide-overrides.js` | Comportamenti dinamici (slider data, menu reorder, ecc.) |
| `wp-assets/page-markup/<slug>.html` | Markup Gutenberg pronto da incollare |
| `wp-assets/hero/*.webp` | Immagini hero slider rinominate |
| `tools/generate_wp_import.py` | Per rigenerare XML import (modifiche menu/pagine) |
| `tools/generate_page_markup.py` | Per rigenerare markup pagine (modifiche layout) |
| `artide-import.xml` | File XML pronto per import in WP (33 pagine + menu) |

---

## 17. Credenziali / accessi (NON nel repo per sicurezza)

- WordPress admin: `https://37.156.244.26/~artide1/wp-admin/`
- Account ElfSight (per widget reviews): da verificare con cliente
- Google Business Profile (per recensioni alimentate da ElfSight): collegato

---

## 18. Note di metodo emerse durante il lavoro

1. **WP filtra `<style>` e SVG** dai blocchi HTML widget. Soluzioni: stili inline con `!important`, oppure SVG in base64 nelle CSS background-image.
2. **CSS Aggiuntivo Customizer rifiuta markup** (`<svg>` interpretato come HTML). Workaround: SVG in base64 dentro url().
3. **Caratteri Unicode emoji** (es. `☎` `✉`) renderizzano colorati su alcuni OS. Forzare text rendering con `&#xFE0E;` (variation selector 15).
4. **FlexSlider fade transition** richiede `position: absolute` su `.slides > li`. Evitare di setttare `position: relative` lì (rompe transizione).
5. **Stacking context con FlexSlider**: l'overlay scuro su `.flexslider::after` viene sovrastato dalle slide attive. Soluzione: rinunciare a overlay container, usare solo `text-shadow` sui caption.
6. **Polylang Free**: niente shortcode `[language-switcher]` (è Pro). Per topbar serve PHP shortcode custom o widget area.
7. **Verifica preview prima di proporre**: il preview HTML statico differisce dal renderizzato dopo `artide-overrides.js`. Sempre controllare `preview-src/*.css/.js` per scoprire override (es. ordine menu, footer in oro non rosso, copyright nascosto).

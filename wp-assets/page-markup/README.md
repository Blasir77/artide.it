# Markup Gutenberg per pagine semplici

Una HTML per ogni pagina interna del sito Artide, pronto per essere
incollato in modalità "Editor di codice" di WordPress (Ctrl+Shift+Alt+M).

## Cosa contiene ogni file

Ogni `.html` qui dentro è il markup Gutenberg (block-level) della pagina
corrispondente:

- Breadcrumb "Home / [titolo]"
- Titolo H1 centrato grande
- Prima immagine (dal preview, via raw.githubusercontent CDN)
- Paragrafi giustificati con grassetti e link interni
- Eventuali H2/H3 sotto-sezioni
- Seconda immagine inserita ogni 5 paragrafi

## Come usarlo per ogni pagina

1. **WP admin → Pagine → Tutte le pagine** → clicca sulla pagina
2. **Ctrl+Shift+Alt+M** per passare a "Editor di codice"
3. **Ctrl+A** per selezionare tutto, poi **Canc** per cancellare
4. Apri il `.html` corrispondente in questo folder, copia tutto
5. Incolla nell'editor di codice
6. **Ctrl+Shift+Alt+M** per tornare in modalità visivo
7. Click **Aggiorna** in alto a destra

## Pagine generate

Servizi:
- automazione, corsi, incasso, manutenzione, potabilizzazione,
  progettazione, sanificazione, sviluppo-software, telecontrollo,
  trasformazione (= Riqualificazione)

Azienda:
- chi-siamo, info-copyright, citazioni-bibliografiche

Certificazioni:
- aiaq, ce, gestore-ambientale, iso-9001, iso-14001, iso-22000,
  moca, osa, rohs

## Note

- **Immagini** caricate via raw.githubusercontent.com — funzionano subito
  senza upload alla Media Library WP. Se in futuro vuoi le immagini
  sotto controllo WP (per ottimizzazione, CDN, ecc.) basta caricarle
  in **Media → Aggiungi** e sostituire le URL nelle pagine.

- **Pagine omesse** dalla generazione automatica (richiedono layout custom):
  - `team` — griglia con 16 foto membri
  - `faq-casa-dell-acqua` — accordion FAQ con 14 domande
  - `prodotti` — bento grid asimmetrica
  - `casa-dell-acqua` + `casa-dell-acqua-collezione` — gallery prodotto
  - `contatti` — richiede form + mappa
  - `blog` — è la pagina archivio articoli (gestita dal tema)

  Queste pagine le costruiremo con layout dedicati una alla volta.

## Rigenerare il markup

Se modifichi i preview HTML e vuoi rigenerare tutti i markup:

```bash
python3 tools/generate_page_markup.py
```

"""SEO mapping: URL → new H1, Title, Meta description, Primary keyword, Template.

Priority keywords to push:
  1. casa dell'acqua
  2. osmosi inversa
  3. depuratore acqua casa
  4. casa dell'acqua per comuni
  5. produttore case dell'acqua
  6. manutenzione case dell'acqua
  7. casa dell'acqua capitolato
  8. telecontrollo case dell'acqua
  9. erogatore acqua mensa
 10. riqualificazione case dell'acqua

Conventions:
- H1: one per page, ≤ 65 chars, primary keyword at start when natural.
- Title: ≤ 60 chars, primary keyword at start + brand suffix "| Artide".
- Meta description: 140–160 chars, CTA-oriented.
- slug: kept identical to original to avoid redirects (unless consolidation).
- template: hero | service | product | certification | legal | hub | article_archive | wiki | faq
"""

# url → dict(h1, title, meta, kw_primary, kw_secondary[], template, consolidate_from[])
SEO_MAP = {
    "/": dict(
        h1="Case dell'Acqua: produttore italiano di erogatori con osmosi inversa",
        title="Case dell'Acqua Artide | Produttore Italiano",
        meta="Artide progetta e produce Case dell'Acqua ed erogatori con osmosi inversa per comuni, aziende e mense. Garanzia a vita, manutenzione attiva.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua", "osmosi inversa", "erogatore acqua mensa"],
        template="home",
    ),

    # ── PRODOTTI ──────────────────────────────────────────────────────────
    "/casa-dell-acqua": dict(
        h1="Casa dell'Acqua: erogatori pubblici con osmosi inversa",
        title="Casa dell'Acqua | Erogatori Pubblici Artide",
        meta="Case dell'acqua Artide per comuni e aziende: osmosi inversa, acqua refrigerata liscia e gassata, telecontrollo integrato. Scopri i modelli.",
        kw_primary="casa dell'acqua",
        kw_secondary=["osmosi inversa", "casa dell'acqua per comuni"],
        template="product",
    ),
    "/casa-dell-acqua-collezione": dict(
        h1="Collezione Case dell'Acqua Artide: oltre 13 modelli",
        title="Collezione Case dell'Acqua | Modelli Artide",
        meta="Oltre 13 modelli di case dell'acqua: urbane, compatte, a incasso, per mense e condomini. Ogni modello è personalizzabile su capitolato comunale.",
        kw_primary="casa dell'acqua",
        kw_secondary=["casa dell'acqua capitolato", "casa dell'acqua per comuni"],
        template="product",
    ),
    "/totem-casa-dell-acqua": dict(
        h1="Totem di pagamento per case dell'acqua",
        title="Totem Pagamento Case dell'Acqua | Artide",
        meta="Totem di pagamento e ricarica tessere per case dell'acqua: contactless, contanti, app. Integrati con telecontrollo Artide.",
        kw_primary="casa dell'acqua",
        kw_secondary=["telecontrollo case dell'acqua"],
        template="product",
    ),
    "/erogatore-d-acqua": dict(
        h1="Erogatori d'acqua per mense, uffici e condomini",
        title="Erogatore Acqua Mensa, Uffici, Condomini | Artide",
        meta="Erogatori d'acqua Artide con osmosi inversa per mense, uffici e condomini. Depuratore acqua casa di qualità industriale, garanzia a vita.",
        kw_primary="erogatore acqua mensa",
        kw_secondary=["depuratore acqua casa", "osmosi inversa"],
        template="product",
    ),
    "/prodotti": dict(
        h1="Prodotti Artide: case dell'acqua, erogatori e totem",
        title="Prodotti Artide | Case dell'Acqua ed Erogatori",
        meta="Gamma completa Artide: case dell'acqua per comuni, erogatori per mense e uffici, totem pagamento, sistemi osmosi inversa. Scopri i cataloghi.",
        kw_primary="casa dell'acqua",
        kw_secondary=["erogatore acqua mensa", "osmosi inversa"],
        template="hub",
    ),

    # ── SERVIZI ───────────────────────────────────────────────────────────
    "/servizi": dict(
        h1="Servizi Artide per case dell'acqua ed erogatori",
        title="Servizi Artide | Case dell'Acqua ed Erogatori",
        meta="Dalla progettazione alla manutenzione case dell'acqua: telecontrollo, sanificazione, riqualificazione, sviluppo software. Un partner unico.",
        kw_primary="manutenzione case dell'acqua",
        kw_secondary=["telecontrollo case dell'acqua", "riqualificazione case dell'acqua"],
        template="hub",
    ),
    "/manutenzione": dict(
        h1="Manutenzione case dell'acqua: contratti e garanzia a vita",
        title="Manutenzione Case dell'Acqua | Artide",
        meta="Manutenzione case dell'acqua Artide: contratti full-service, garanzia a vita del prodotto, ricambi originali, interventi in 24–48 ore.",
        kw_primary="manutenzione case dell'acqua",
        kw_secondary=["casa dell'acqua", "telecontrollo case dell'acqua"],
        template="service",
    ),
    "/telecontrollo": dict(
        h1="Telecontrollo case dell'acqua: gestione remota in tempo reale",
        title="Telecontrollo Case dell'Acqua | Artide",
        meta="Telecontrollo case dell'acqua Artide: monitoraggio consumi, allarmi, ricariche tessere e report per comuni e gestori idrici, 24/7.",
        kw_primary="telecontrollo case dell'acqua",
        kw_secondary=["casa dell'acqua", "manutenzione case dell'acqua"],
        template="service",
    ),
    "/progettazione": dict(
        h1="Progettazione case dell'acqua su capitolato comunale",
        title="Progettazione Case dell'Acqua | Artide",
        meta="Progettazione case dell'acqua su capitolato: dimensionamento idraulico, architettura, allacci, domanda autorizzazioni. Risposta in 7 giorni.",
        kw_primary="casa dell'acqua capitolato",
        kw_secondary=["casa dell'acqua per comuni", "produttore case dell'acqua"],
        template="service",
    ),
    "/sanificazione": dict(
        h1="Sanificazione case dell'acqua ed erogatori",
        title="Sanificazione Case dell'Acqua | Artide",
        meta="Sanificazione periodica case dell'acqua ed erogatori con protocolli HACCP: analisi, igienizzazione UV, tracciabilità. Conformi ISO 22000.",
        kw_primary="manutenzione case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="service",
    ),
    "/sviluppo-software": dict(
        h1="Sviluppo software per case dell'acqua ed erogatori",
        title="Software Case dell'Acqua | Artide",
        meta="Software proprietario Artide per telecontrollo case dell'acqua, gestione tessere, dashboard comuni. Integrazione con i tuoi sistemi.",
        kw_primary="telecontrollo case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="service",
    ),
    "/automazione": dict(
        h1="Automazione industriale per case dell'acqua",
        title="Automazione Case dell'Acqua | Artide",
        meta="Automazione industriale Artide per case dell'acqua: PLC, sensoristica, controllo di processo con partner Schneider Electric.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua"],
        template="service",
    ),
    "/potabilizzazione": dict(
        h1="Potabilizzazione acqua con osmosi inversa",
        title="Potabilizzazione Acqua | Osmosi Inversa Artide",
        meta="Impianti di potabilizzazione Artide con osmosi inversa per acquedotti, condomini e mense. Acqua potabile certificata 24/7.",
        kw_primary="osmosi inversa",
        kw_secondary=["depuratore acqua casa", "erogatore acqua mensa"],
        template="service",
    ),
    "/trasformazione": dict(
        h1="Riqualificazione case dell'acqua esistenti",
        title="Riqualificazione Case dell'Acqua | Artide",
        meta="Riqualificazione case dell'acqua di altri produttori: sostituzione impianto osmosi inversa, telecontrollo, estetica. Garanzia totale Artide.",
        kw_primary="riqualificazione case dell'acqua",
        kw_secondary=["casa dell'acqua", "manutenzione case dell'acqua"],
        template="service",
    ),
    "/produzione-tessere": dict(
        h1="Tessere e badge per case dell'acqua",
        title="Tessere Case dell'Acqua | Artide",
        meta="Produzione tessere RFID e badge personalizzati per case dell'acqua: grafica su misura, stampa in alta definizione, consegna rapida.",
        kw_primary="casa dell'acqua",
        kw_secondary=["casa dell'acqua per comuni"],
        template="service",
    ),
    "/incasso": dict(
        h1="Incasso contante per case dell'acqua",
        title="Incasso Contante Case dell'Acqua | Artide",
        meta="Servizio di incasso contante per case dell'acqua: svuotamento cassa, conteggio, versamento. Conforme alla normativa antiriciclaggio.",
        kw_primary="casa dell'acqua",
        kw_secondary=["casa dell'acqua per comuni"],
        template="service",
    ),
    "/corsi": dict(
        h1="Corsi di formazione per case dell'acqua ed erogatori",
        title="Corsi Case dell'Acqua | Formazione Artide",
        meta="Corsi di formazione Artide per operatori e tecnici di case dell'acqua ed erogatori: manutenzione, sanificazione, telecontrollo.",
        kw_primary="manutenzione case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="service",
    ),
    # /assistenza and /supporto are now redirected to /contatti per client request.

    # ── AZIENDA ───────────────────────────────────────────────────────────
    "/chi-siamo": dict(
        h1="Chi siamo: produttore italiano di case dell'acqua",
        title="Chi Siamo | Produttore Case dell'Acqua Artide",
        meta="Artide srl: produttore italiano di case dell'acqua dal 2003. Oltre 300 installazioni attive, 240.000 litri erogati al giorno. Scopri la storia.",
        kw_primary="produttore case dell'acqua",
        kw_secondary=["casa dell'acqua", "casa dell'acqua per comuni"],
        template="about",
        consolidate_from=["/azienda"],
    ),
    "/team": dict(
        h1="Il team Artide: professionisti delle case dell'acqua",
        title="Team Artide | Case dell'Acqua ed Erogatori",
        meta="Il team Artide: ingegneri, tecnici e consulenti specializzati in case dell'acqua, osmosi inversa e telecontrollo. Conosci chi ti supporta.",
        kw_primary="produttore case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="team",
    ),
    "/export": dict(
        h1="Export case dell'acqua: Artide nel mondo",
        title="Export Case dell'Acqua | Artide",
        meta="Artide esporta case dell'acqua ed erogatori in Europa e Medio Oriente: progettazione su specifica locale, assistenza multilingua.",
        kw_primary="produttore case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="service",
    ),
    "/contatti": dict(
        h1="Contatti Artide: case dell'acqua ed erogatori",
        title="Contatti | Artide Case dell'Acqua",
        meta="Contatta Artide per preventivi case dell'acqua, erogatori, manutenzione e telecontrollo. Rispondiamo entro 24 ore lavorative.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua"],
        template="contact",
    ),

    # ── CERTIFICAZIONI ────────────────────────────────────────────────────
    "/certificazioni": dict(
        h1="Certificazioni Artide per case dell'acqua ed erogatori",
        title="Certificazioni Artide | Case dell'Acqua",
        meta="Certificazioni Artide: ISO 9001, 14001, 22000, CE, MOCA, RoHS, OSA, AIAQ, Albo Gestori Ambientali. Qualità e sicurezza verificate.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua"],
        template="hub",
    ),
    "/iso-9001": dict(
        h1="ISO 9001: qualità certificata nelle case dell'acqua",
        title="ISO 9001 | Case dell'Acqua Artide",
        meta="Artide è certificata ISO 9001 per la progettazione e produzione di case dell'acqua ed erogatori. Processi qualità tracciati.",
        kw_primary="produttore case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="certification",
    ),
    "/iso-14001": dict(
        h1="ISO 14001: gestione ambientale Artide",
        title="ISO 14001 | Gestione Ambientale Artide",
        meta="Artide è certificata ISO 14001 dal 2024: impatto ambientale misurato e ridotto lungo tutto il ciclo di vita della casa dell'acqua.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua"],
        template="certification",
    ),
    "/iso-22000": dict(
        h1="ISO 22000: sicurezza alimentare delle case dell'acqua",
        title="ISO 22000 | Sicurezza Alimentare Artide",
        meta="Case dell'acqua Artide conformi ISO 22000: HACCP, controlli microbiologici, tracciabilità. Acqua sicura per tutti i consumatori.",
        kw_primary="casa dell'acqua",
        kw_secondary=["manutenzione case dell'acqua"],
        template="certification",
    ),
    "/ce": dict(
        h1="Marcatura CE sulle case dell'acqua Artide",
        title="Marcatura CE | Case dell'Acqua Artide",
        meta="Tutti i prodotti Artide — case dell'acqua, erogatori, totem — sono conformi alla marcatura CE secondo le direttive UE applicabili.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua"],
        template="certification",
    ),
    "/aiaq": dict(
        h1="Artide membro AIAQ: Associazione Acque di Qualità",
        title="Artide AIAQ | Acque di Qualità Italia",
        meta="Artide è iscritta all'AIAQ (Associazione Acque Italiane di Qualità), a tutela degli standard di osmosi inversa e trattamento acque.",
        kw_primary="osmosi inversa",
        kw_secondary=["casa dell'acqua"],
        template="certification",
    ),
    "/moca": dict(
        h1="Conformità MOCA per case dell'acqua ed erogatori",
        title="MOCA | Case dell'Acqua Conformi | Artide",
        meta="Case dell'acqua Artide conformi al regolamento MOCA (Materiali e Oggetti a Contatto con Alimenti): sicurezza certificata.",
        kw_primary="casa dell'acqua",
        kw_secondary=["manutenzione case dell'acqua"],
        template="certification",
    ),
    "/osa": dict(
        h1="Artide è un OSA: Operatore del Settore Alimentare",
        title="OSA | Artide Case dell'Acqua",
        meta="Artide è registrata come OSA (Operatore del Settore Alimentare): case dell'acqua prodotte e manutenute sotto vigilanza sanitaria.",
        kw_primary="produttore case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="certification",
    ),
    "/rohs": dict(
        h1="Conformità RoHS delle case dell'acqua Artide",
        title="RoHS | Case dell'Acqua Artide",
        meta="Case dell'acqua Artide conformi alla direttiva RoHS: nessuna sostanza pericolosa nei componenti elettrici ed elettronici.",
        kw_primary="casa dell'acqua",
        kw_secondary=["produttore case dell'acqua"],
        template="certification",
    ),
    "/gestore-ambientale": dict(
        h1="Artide iscritta all'Albo Gestori Ambientali",
        title="Albo Gestori Ambientali | Artide",
        meta="Artide è iscritta all'Albo Nazionale Gestori Ambientali: gestione conforme dei rifiuti derivanti da manutenzione case dell'acqua.",
        kw_primary="manutenzione case dell'acqua",
        kw_secondary=["casa dell'acqua"],
        template="certification",
    ),

    # ── LEGAL ─────────────────────────────────────────────────────────────
    "/info-copyright": dict(
        h1="Informativa Copyright",
        title="Copyright | Artide",
        meta="Informativa copyright del sito Artide: diritti sui contenuti, testi e immagini relativi a case dell'acqua ed erogatori.",
        kw_primary="casa dell'acqua",
        kw_secondary=[],
        template="legal",
    ),
    "/informativa-privacy": dict(
        h1="Informativa sulla Privacy",
        title="Privacy | Artide",
        meta="Informativa privacy Artide: trattamento dati personali ai sensi del GDPR, cookie policy, diritti dell'interessato.",
        kw_primary="casa dell'acqua",
        kw_secondary=[],
        template="legal",
    ),
    "/legal-content": dict(
        h1="Note Legali",
        title="Note Legali | Artide",
        meta="Note legali del sito Artide: informazioni societarie, termini di utilizzo dei contenuti relativi a case dell'acqua ed erogatori.",
        kw_primary="casa dell'acqua",
        kw_secondary=[],
        template="legal",
    ),

    # ── WIKI / FAQ ────────────────────────────────────────────────────────
    "/wiki": dict(
        h1="Wiki Artide: guide su case dell'acqua ed erogatori",
        title="Wiki | Artide Case dell'Acqua",
        meta="Wiki Artide: guide, manuali e domande frequenti su case dell'acqua, erogatori, osmosi inversa e telecontrollo.",
        kw_primary="casa dell'acqua",
        kw_secondary=["osmosi inversa"],
        template="hub",
    ),
    "/wiki-casa-dell-acqua": dict(
        h1="Wiki Casa dell'Acqua: come funziona e come gestirla",
        title="Wiki Casa dell'Acqua | Guide | Artide",
        meta="Guide tecniche sulla casa dell'acqua: funzionamento osmosi inversa, sanificazione, telecontrollo, capitolato per comuni.",
        kw_primary="casa dell'acqua",
        kw_secondary=["osmosi inversa", "casa dell'acqua capitolato"],
        template="wiki",
    ),
    "/wiki-totem-pagamento": dict(
        h1="Wiki Totem di pagamento per case dell'acqua",
        title="Wiki Totem Pagamento | Case dell'Acqua | Artide",
        meta="Guide sul totem di pagamento per case dell'acqua: ricarica tessere, metodi di pagamento, gestione guasti.",
        kw_primary="casa dell'acqua",
        kw_secondary=["telecontrollo case dell'acqua"],
        template="wiki",
    ),
    "/faq-casa-dell-acqua": dict(
        h1="FAQ Casa dell'Acqua: domande e risposte",
        title="FAQ Casa dell'Acqua | Artide",
        meta="Le domande più frequenti sulle case dell'acqua Artide: costi, manutenzione, capitolato, osmosi inversa e tempi di installazione.",
        kw_primary="casa dell'acqua",
        kw_secondary=["manutenzione case dell'acqua", "casa dell'acqua capitolato"],
        template="faq",
    ),
    "/citazioni-bibliografiche": dict(
        h1="Citazioni bibliografiche sulle case dell'acqua",
        title="Citazioni Bibliografiche | Artide",
        meta="Fonti scientifiche e normative citate da Artide per case dell'acqua, osmosi inversa, sicurezza alimentare.",
        kw_primary="casa dell'acqua",
        kw_secondary=["osmosi inversa"],
        template="legal",
    ),

    # ── SUPPORTO (consolidato in /assistenza) ─────────────────────────────
    # /supporto is absorbed into /assistenza (see consolidate_from)

    # ── BLOG ──────────────────────────────────────────────────────────────
    "/blog": dict(
        h1="Blog Artide: novità su case dell'acqua ed erogatori",
        title="Blog Artide | Case dell'Acqua",
        meta="Comunicazioni ufficiali, inaugurazioni e approfondimenti su case dell'acqua, osmosi inversa, sostenibilità e consumo consapevole.",
        kw_primary="casa dell'acqua",
        kw_secondary=["osmosi inversa"],
        template="article_archive",
    ),
}

# Pages to redirect (slug_from → slug_to)
REDIRECTS = {
    "/azienda": "/chi-siamo",
    "/supporto": "/contatti",
    "/assistenza": "/contatti",
    "/blog-articoli": "/blog",
    "/blog-articoli-in-evidenza": "/blog",
    "/blog/p-q2odg5ma/1": "/blog",
    "/blog/p-q2odg5ma/2": "/blog",
    "/blog/p-q2odg5ma/3": "/blog",
    "/blog/p-q2odg5ma/4": "/blog",
}

# For blog articles (URLs starting with /l/blog-), apply an automatic SEO template
# (we'll fix titles and H1s algorithmically)
BLOG_ARTICLE_DEFAULTS = dict(
    template="article",
    kw_primary="casa dell'acqua",  # most articles revolve around it
    kw_secondary=["osmosi inversa", "manutenzione case dell'acqua"],
)

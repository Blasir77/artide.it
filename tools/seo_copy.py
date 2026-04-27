"""SEO copy module — intro and outro paragraphs for pages whose body
lacks keyword density. Tone: technical-professional Italian, 100%
Italian wording. Each entry adds:

  intro:       60–90 words, inserted right after the page H1
  outro:       50–70 words, inserted at the end of the main content
  related:     internal link target + anchor text (keyword-rich)

Keyword strategy reconciles the client's original 10 priority terms
with the 28 keywords identified by SEO Business S.R.L., focusing on
high-volume generic terms ("depuratore acqua", "casa dell acqua",
"potabilizzazione acqua") together with brand-specific long-tail
("manutenzione case dell'acqua", "casa dell'acqua capitolato",
"telecontrollo case dell'acqua", …).

The dict key is the URL (no trailing slash, '/' for the home).
"""

SEO_COPY = {
    # ── HUB / OVERVIEW ──────────────────────────────────────────────
    "/servizi": dict(
        intro=(
            "I servizi Artide coprono l'intero ciclo di vita di una casa dell'acqua "
            "e di un erogatore: dalla progettazione su capitolato comunale alla "
            "manutenzione case dell'acqua attiva 24 ore su 24, dal telecontrollo in "
            "tempo reale alla sanificazione periodica dell'impianto idrico. Operiamo "
            "su oltre 500 installazioni in Italia, con tecnici specializzati nella "
            "depurazione acqua, nella potabilizzazione e nella riqualificazione "
            "case dell'acqua di altri produttori, garantendo continuità operativa "
            "e conformità ISO 22000."
        ),
        outro=(
            "Scegliendo Artide come unico interlocutore, il committente affida la "
            "manutenzione case dell'acqua, la sanificazione serbatoio acqua potabile "
            "e il telecontrollo a un produttore italiano con vent'anni di esperienza. "
            "Per un preventivo su misura visita la pagina "
        ),
        related=("/contatti", "contatti"),
    ),

    "/certificazioni": dict(
        intro=(
            "Artide è un produttore italiano di case dell'acqua certificato secondo "
            "i principali standard di qualità, ambiente e sicurezza alimentare. "
            "Le nostre case dell'acqua e i nostri erogatori sono conformi a ISO 9001, "
            "ISO 14001, ISO 22000, marcatura CE, regolamento MOCA, direttiva RoHS, "
            "iscritti all'Albo Gestori Ambientali e al registro OSA. La conformità "
            "è ribadita in ogni capitolato di gara e accompagnata da documentazione "
            "tecnica completa."
        ),
        outro=(
            "Le certificazioni Artide tutelano il committente in tutto il ciclo di "
            "vita dell'impianto: produzione case dell'acqua, manutenzione case "
            "dell'acqua, sanificazione e gestione fine vita rispettano i requisiti "
            "di legge italiani ed europei. Per richiedere copia delle certificazioni "
            "scrivi alla pagina "
        ),
        related=("/contatti", "contatti"),
    ),

    # ── SERVIZI: MANUTENZIONE / SANIFICAZIONE / TELECONTROLLO ───────
    "/manutenzione": dict(
        intro=(
            "La manutenzione case dell'acqua è il servizio più richiesto da Comuni e "
            "gestori del servizio idrico integrato. Artide fornisce contratti full "
            "service di manutenzione case dell'acqua con interventi entro 24 ore, "
            "ricambi originali, sanificazione serbatoio acqua potabile programmata e "
            "monitoraggio remoto via telecontrollo. La manutenzione case dell'acqua "
            "Artide include anche depurazione acqua, sostituzione filtri a osmosi "
            "inversa e taratura impianti, nel rispetto delle normative ISO 22000 e "
            "MOCA."
        ),
        outro=(
            "Affidare la manutenzione case dell'acqua a un produttore italiano "
            "garantisce continuità del servizio e tempi di intervento certi. Per "
            "approfondire l'integrazione fra manutenzione e telecontrollo case "
            "dell'acqua consulta la pagina "
        ),
        related=("/telecontrollo", "telecontrollo case dell'acqua"),
    ),

    "/sanificazione": dict(
        intro=(
            "La sanificazione case dell'acqua e dei serbatoi di accumulo è una "
            "componente obbligatoria della manutenzione case dell'acqua. Artide "
            "esegue la sanificazione serbatoio acqua potabile con protocolli HACCP, "
            "trattamento acqua potabile a base di ozono e raggi UV, controlli "
            "microbiologici e tracciabilità documentale. La sanificazione delle "
            "cisterne acqua e dei circuiti idrici è certificata ISO 22000 e "
            "compatibile con il regolamento MOCA per i materiali a contatto con "
            "alimenti."
        ),
        outro=(
            "La sanificazione regolare prolunga la vita dei filtri a osmosi inversa "
            "e tutela la salute degli utenti. Inserisci la sanificazione serbatoio "
            "acqua potabile nel tuo piano di manutenzione case dell'acqua: scopri "
            "come integrarla con il servizio di "
        ),
        related=("/manutenzione", "manutenzione case dell'acqua"),
    ),

    "/telecontrollo": dict(
        intro=(
            "Il telecontrollo case dell'acqua è la piattaforma proprietaria Artide "
            "che monitora in tempo reale ogni casa dell'acqua e ogni erogatore "
            "installato. Il telecontrollo case dell'acqua misura litri erogati, "
            "stato dei filtri a osmosi inversa, temperatura dell'acqua refrigerata, "
            "saldo delle tessere RFID e allarmi tecnici. Il sistema di telecontrollo "
            "è accessibile via dashboard web ed è integrato con la manutenzione "
            "case dell'acqua per attivare interventi automatici prima del guasto."
        ),
        outro=(
            "Il telecontrollo case dell'acqua è incluso nei contratti di "
            "manutenzione full service Artide e abilita la rendicontazione mensile "
            "dei consumi a Comuni e municipalizzate. Per integrare il telecontrollo "
            "case dell'acqua con la sanificazione programmata visita la pagina "
        ),
        related=("/sanificazione", "sanificazione delle case dell'acqua"),
    ),

    "/progettazione": dict(
        intro=(
            "La progettazione case dell'acqua Artide parte dal capitolato di gara: "
            "dimensionamento del depuratore acqua a osmosi inversa, planimetria "
            "idraulica, allacci, autorizzazioni sanitarie, scelta dei materiali "
            "MOCA e definizione del telecontrollo case dell'acqua. Sviluppiamo "
            "casa dell'acqua capitolato per Comuni, municipalizzate e aziende, "
            "rispettando vincoli urbanistici, accessibilità e immagine "
            "istituzionale. La progettazione include sempre la fase di "
            "manutenzione case dell'acqua a vita."
        ),
        outro=(
            "Una progettazione corretta riduce drasticamente i costi di "
            "manutenzione case dell'acqua nel tempo. Per i requisiti tecnici "
            "minimi di un capitolato chiavi in mano consulta i nostri "
        ),
        related=("/prodotti", "prodotti Artide"),
    ),

    "/sviluppo-software": dict(
        intro=(
            "Artide sviluppa il software che pilota le proprie case dell'acqua: "
            "firmware embedded, dashboard di telecontrollo case dell'acqua, "
            "applicazioni per le tessere RFID, integrazioni con i gestionali dei "
            "Comuni. Il software Artide governa la depurazione acqua, "
            "l'erogazione, la fatturazione elettronica e gli allarmi della casa "
            "dell'acqua. Tutto il codice è scritto e mantenuto in Italia, con "
            "aggiornamenti firmati e procedure di backup conformi ai requisiti "
            "ISO 22000."
        ),
        outro=(
            "L'integrazione fra software e hardware è ciò che rende il telecontrollo "
            "case dell'acqua davvero affidabile. Per vedere come il software si "
            "interfaccia con la manutenzione case dell'acqua consulta la pagina "
        ),
        related=("/telecontrollo", "telecontrollo case dell'acqua"),
    ),

    "/automazione": dict(
        intro=(
            "L'automazione industriale Artide governa ogni casa dell'acqua tramite "
            "PLC, sensori di livello, valvole motorizzate e logiche di sicurezza "
            "ridondate. Lavoriamo con Schneider Electric come partner tecnologico "
            "per garantire continuità operativa al depuratore acqua e al sistema "
            "di potabilizzazione acqua, anche in scenari di cyber-resilienza. "
            "L'automazione è progettata per integrarsi con il telecontrollo case "
            "dell'acqua e con la manutenzione predittiva."
        ),
        outro=(
            "Un'automazione robusta abbatte le chiamate di manutenzione case "
            "dell'acqua e protegge l'investimento del Comune. Per vedere come "
            "l'automazione dialoga col software di gestione visita la pagina "
        ),
        related=("/sviluppo-software", "sviluppo software per case dell'acqua"),
    ),

    "/potabilizzazione": dict(
        intro=(
            "Gli impianti di potabilizzazione acqua Artide trasformano acque non "
            "conformi in acqua potabile certificata. Il trattamento acqua potabile "
            "si basa su filtrazione meccanica, osmosi inversa, microfiltrazione a "
            "0,5 µm e disinfezione UV. La potabilizzazione acqua è applicata sia "
            "nelle case dell'acqua sia in impianti di potabilizzazione delle acque "
            "per condomini, scuole e mense aziendali. Tutti i materiali sono "
            "conformi MOCA e ISO 22000."
        ),
        outro=(
            "La potabilizzazione acqua è il primo passo per offrire acqua "
            "microfiltrata gratuita o a basso costo agli utenti. Per scoprire i "
            "modelli di casa dell'acqua più adatti al tuo scenario visita la "
            "sezione "
        ),
        related=("/casa-dell-acqua-collezione", "collezione case dell'acqua"),
    ),

    "/trasformazione": dict(
        intro=(
            "La riqualificazione case dell'acqua è il servizio Artide che permette "
            "ai Comuni di rinnovare impianti esistenti senza demolirli. La "
            "riqualificazione case dell'acqua sostituisce il depuratore acqua a "
            "osmosi inversa, l'unità di telecontrollo, i totem di pagamento e la "
            "carrozzeria, riportando in garanzia anche case dell'acqua di altri "
            "produttori. Operiamo riqualificazione di case dell'acqua urbane, "
            "compatte e a incasso, salvando i componenti hardware ancora validi."
        ),
        outro=(
            "Una riqualificazione case dell'acqua ben fatta costa fino al 60% in "
            "meno di una nuova installazione. Per inserirla nel tuo piano di "
            "manutenzione case dell'acqua scrivici dalla pagina "
        ),
        related=("/contatti", "contatti"),
    ),

    "/corsi": dict(
        intro=(
            "I corsi Artide formano operatori comunali, tecnici di municipalizzate "
            "e personale di mensa sulla gestione della casa dell'acqua. I corsi "
            "trattano manutenzione case dell'acqua di primo livello, sanificazione "
            "serbatoio acqua potabile, sostituzione dei filtri a osmosi inversa, "
            "uso del telecontrollo case dell'acqua e gestione delle tessere RFID. "
            "Sono erogati in aula, on the job o in modalità e-learning, con "
            "rilascio di attestato di partecipazione."
        ),
        outro=(
            "Un team formato dimezza i tempi di intervento e migliora la qualità "
            "della manutenzione case dell'acqua. Per concordare un programma di "
            "formazione ad hoc contattaci dalla pagina "
        ),
        related=("/contatti", "contatti"),
    ),

    "/produzione-tessere": dict(
        intro=(
            "Artide produce tessere RFID e badge personalizzati per la casa "
            "dell'acqua: card contactless, portachiavi e bracciali compatibili "
            "con tutti i nostri erogatori. La produzione tessere case dell'acqua "
            "include grafica su misura per il Comune, codifica univoca, ricarica "
            "via app, totem o sportello e gestione anagrafica integrata col "
            "telecontrollo case dell'acqua. Le tessere RFID sono conformi al GDPR "
            "e tracciate end-to-end."
        ),
        outro=(
            "Le tessere RFID sono il principale strumento di rendicontazione "
            "consumi per Comuni e gestori. Per integrare le tessere con il "
            "totem di pagamento della casa dell'acqua visita "
        ),
        related=("/totem-casa-dell-acqua", "totem casa dell'acqua"),
    ),

    "/incasso": dict(
        intro=(
            "Il servizio di incasso contante Artide gestisce lo svuotamento "
            "periodico delle casse di ogni casa dell'acqua, il conteggio dei "
            "contanti, il versamento bancario e la rendicontazione al Comune. Il "
            "servizio è conforme alla normativa antiriciclaggio e si integra con "
            "il telecontrollo case dell'acqua per riconciliare incassi e litri "
            "erogati. La gestione incasso è inclusa nei contratti full service "
            "di manutenzione case dell'acqua."
        ),
        outro=(
            "Esternalizzando l'incasso il Comune azzera il rischio cassa e "
            "concentra le risorse sul servizio cittadino. Per attivare l'incasso "
            "insieme alla manutenzione case dell'acqua scrivici dalla "
        ),
        related=("/contatti", "pagina contatti"),
    ),

    "/erogatore-d-acqua": dict(
        intro=(
            "Gli erogatori d'acqua Artide forniscono acqua microfiltrata, "
            "refrigerata e gassata a uffici, mense, condomini e comunità "
            "residenziali. Ogni erogatore acqua mensa è equipaggiato con "
            "depuratore acqua a osmosi inversa, sanificazione UV automatica e "
            "telecontrollo da remoto. I distributori acqua a colonna o a "
            "incasso sono conformi MOCA e ISO 22000, garantiti a vita se "
            "abbinati al servizio di manutenzione case dell'acqua."
        ),
        outro=(
            "Gli erogatori Artide riducono fino al 95% l'uso di bottiglie di "
            "plastica nelle mense aziendali. Per il modello più adatto alle "
            "tue esigenze contatta i nostri tecnici dalla "
        ),
        related=("/contatti", "pagina contatti"),
    ),

    # ── AZIENDA ─────────────────────────────────────────────────────
    "/chi-siamo": dict(
        intro=(
            "Artide srl è un produttore italiano di case dell'acqua ed erogatori "
            "con sede a Sala Baganza (Parma). Dal 2003 progettiamo e manuteniamo "
            "case dell'acqua per Comuni, gestori del servizio idrico integrato e "
            "grandi realtà industriali. Come produttore case dell'acqua "
            "controlliamo internamente la depurazione acqua, l'osmosi inversa, "
            "il telecontrollo case dell'acqua e la riqualificazione case dell'acqua "
            "esistenti, garantendo i nostri prodotti a vita."
        ),
        outro=(
            "Essere un produttore case dell'acqua italiano significa essere unico "
            "responsabile di progettazione, produzione e manutenzione. Per scoprire "
            "le persone dietro al marchio Artide visita la pagina "
        ),
        related=("/team", "team Artide"),
    ),

    "/team": dict(
        intro=(
            "Il team Artide è composto da ingegneri idraulici, sviluppatori "
            "software, tecnici di manutenzione case dell'acqua e consulenti "
            "amministrativi specializzati nella gestione contratti con la "
            "pubblica amministrazione. Come produttore case dell'acqua copriamo "
            "internamente progettazione, depuratore acqua, telecontrollo case "
            "dell'acqua e riqualificazione case dell'acqua, senza esternalizzare "
            "le competenze chiave."
        ),
        outro=(
            "Un team integrato è la prima garanzia di continuità del servizio "
            "post-vendita. Per parlare direttamente con i nostri tecnici scrivici "
            "dalla "
        ),
        related=("/contatti", "pagina contatti"),
    ),

    # ── CERTIFICAZIONI SINGOLE ──────────────────────────────────────
    "/iso-9001": dict(
        intro=(
            "Artide è certificata ISO 9001 come produttore case dell'acqua: ogni "
            "fase — progettazione, produzione, depuratore acqua, manutenzione "
            "case dell'acqua e telecontrollo case dell'acqua — è documentata, "
            "verificata e tracciabile. La certificazione ISO 9001 è rilasciata "
            "da ente accreditato e rinnovata annualmente con audit di sorveglianza."
        ),
        outro=(
            "ISO 9001 garantisce al committente che il produttore case dell'acqua "
            "applica gli stessi standard di qualità a tutta la filiera. Tutte "
            "le certificazioni Artide sono raccolte nella sezione "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/iso-14001": dict(
        intro=(
            "La certificazione ISO 14001, conseguita ad aprile 2024, attesta che "
            "Artide produce e manutiene case dell'acqua riducendo l'impatto "
            "ambientale lungo l'intero ciclo di vita: scelta dei materiali, "
            "produzione, logistica, manutenzione case dell'acqua e dismissione. "
            "ISO 14001 si integra con la nostra iscrizione all'Albo Gestori "
            "Ambientali e con il sistema di telecontrollo case dell'acqua per "
            "ridurre gli sprechi idrici."
        ),
        outro=(
            "ISO 14001 è un requisito sempre più frequente nei capitolati "
            "comunali. Per la versione integrale del certificato, e di tutte le "
            "altre certificazioni Artide, visita la pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/iso-22000": dict(
        intro=(
            "ISO 22000 certifica che la casa dell'acqua Artide rispetta i "
            "requisiti di sicurezza alimentare lungo tutta la filiera: "
            "depuratore acqua a osmosi inversa, materiali a contatto con "
            "alimenti (MOCA), sanificazione serbatoio acqua potabile, "
            "tracciabilità dei lotti e procedure HACCP. ISO 22000 si applica "
            "anche al servizio di manutenzione case dell'acqua e alla "
            "sanificazione periodica."
        ),
        outro=(
            "Per Comuni e gestori del servizio idrico, ISO 22000 è la garanzia "
            "che l'acqua erogata dalla casa dell'acqua è sicura per il consumo. "
            "Tutte le certificazioni Artide sono consultabili nella sezione "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/ce": dict(
        intro=(
            "Tutte le case dell'acqua, gli erogatori e i totem prodotti da "
            "Artide sono conformi alla marcatura CE e alle direttive europee "
            "applicabili: macchine, bassa tensione, compatibilità "
            "elettromagnetica, MOCA. La marcatura CE è apposta su ogni casa "
            "dell'acqua dopo i test di conformità ed è documentata da "
            "dichiarazione di conformità UE."
        ),
        outro=(
            "La marcatura CE è obbligatoria per qualsiasi casa dell'acqua "
            "installata in Italia. Per le altre certificazioni del produttore "
            "case dell'acqua Artide visita la pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/moca": dict(
        intro=(
            "Le case dell'acqua Artide sono conformi al regolamento MOCA "
            "(Materiali e Oggetti a Contatto con Alimenti): tubi, raccordi, "
            "guarnizioni e membrane del depuratore acqua a osmosi inversa "
            "rispondono ai requisiti DM 174/2004 e CE 1935/2004. La conformità "
            "MOCA è garantita anche dopo ogni intervento di manutenzione case "
            "dell'acqua e di sanificazione serbatoio acqua potabile."
        ),
        outro=(
            "MOCA è un requisito imprescindibile per qualsiasi casa dell'acqua "
            "che eroga acqua destinata al consumo umano. Tutte le certificazioni "
            "Artide sono raccolte nella pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/osa": dict(
        intro=(
            "Artide è iscritta come OSA (Operatore del Settore Alimentare) presso "
            "l'ASL di competenza: ciò significa che il produttore case dell'acqua "
            "è soggetto a vigilanza sanitaria e ai controlli previsti dal "
            "regolamento europeo 178/2002. La qualifica OSA si applica sia alla "
            "produzione case dell'acqua sia alla manutenzione case dell'acqua e "
            "alla sanificazione."
        ),
        outro=(
            "La qualifica OSA è una garanzia ulteriore richiesta nei capitolati "
            "di Comuni e municipalizzate. Tutte le certificazioni e le "
            "autorizzazioni del produttore case dell'acqua Artide sono "
            "consultabili nella pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/rohs": dict(
        intro=(
            "Le case dell'acqua e gli erogatori Artide sono conformi alla "
            "direttiva RoHS (Restriction of Hazardous Substances): nessuna "
            "casa dell'acqua contiene piombo, mercurio, cadmio o altre sostanze "
            "vietate nelle apparecchiature elettriche ed elettroniche. La "
            "conformità RoHS si applica sia alle parti elettroniche del "
            "telecontrollo case dell'acqua sia ai componenti del depuratore "
            "acqua a osmosi inversa."
        ),
        outro=(
            "RoHS protegge gli utenti finali e il personale di manutenzione "
            "case dell'acqua dall'esposizione a sostanze pericolose. Le altre "
            "certificazioni del produttore case dell'acqua Artide sono "
            "consultabili nella pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/aiaq": dict(
        intro=(
            "Artide è iscritta all'AIAQ — Associazione Italiana Acque di "
            "Qualità — che riunisce i principali operatori italiani del "
            "trattamento acqua potabile, della depurazione acqua e degli "
            "impianti di potabilizzazione delle acque. L'adesione AIAQ è una "
            "garanzia di aggiornamento normativo continuo e di rispetto degli "
            "standard tecnici condivisi dal settore della casa dell'acqua."
        ),
        outro=(
            "AIAQ promuove la condivisione di buone pratiche fra produttori "
            "case dell'acqua e operatori della potabilizzazione acqua. Tutte "
            "le altre certificazioni Artide sono raccolte nella pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),

    "/gestore-ambientale": dict(
        intro=(
            "Artide è iscritta all'Albo Nazionale Gestori Ambientali per il "
            "trasporto e la gestione dei rifiuti derivanti dalla manutenzione "
            "case dell'acqua: filtri esausti del depuratore acqua a osmosi "
            "inversa, oli, carcasse elettroniche del telecontrollo case "
            "dell'acqua. L'iscrizione tutela il committente da responsabilità "
            "indirette nella gestione del fine-vita dell'impianto."
        ),
        outro=(
            "Affidare la manutenzione case dell'acqua a un gestore ambientale "
            "iscritto significa chiudere il cerchio della conformità "
            "normativa. Tutte le certificazioni Artide sono raccolte nella "
            "pagina "
        ),
        related=("/certificazioni", "certificazioni"),
    ),
}


def get_copy(url: str) -> dict | None:
    """Return SEO copy for a URL or None if not configured."""
    if url.endswith("/") and url != "/":
        url = url.rstrip("/")
    return SEO_COPY.get(url)

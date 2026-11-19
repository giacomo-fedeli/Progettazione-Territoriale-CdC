# Catalogo delle misure DAX

> **File generato** dallo script [`strumenti/genera_catalogo_misure.py`](strumenti/genera_catalogo_misure.py) leggendo i file del modello (TMDL) e del report (PBIR). Non modificarlo a mano: cambia il modello e rilancia lo script.

Il modello ha **299 misure**: **163 di calcolo** (questo catalogo, con formula DAX) e **136 di presentazione** (SVG delle card KPI, colori, testi dei sottotitoli: non calcolano numeri di business, vedi sezione M).

Per le definizioni dei KPI in linguaggio semplice leggi prima [04 – KPI e misure](04-kpi-e-misure.md). Questo catalogo serve a chi vuole la formula esatta.

**Come leggere le colonne**
- *Cosa misura*: descrizione scritta nel modello o, se manca, qui nello script.
- *Formato*: formato numerico DAX (`#,0` = intero con separatore, `0.0%` = percentuale con un decimale, …).
- *Dove si vede*: pagine del report che usano la misura in un visual. «Indiretta» = non è in un visual ma la usa un'altra misura. «Solo bozze» = compare solo nelle pagine nascoste di prova. «Non usata» = né in un visual né in altre misure.

Tutte le misure stanno nella tabella `_Misure`, tranne 10 che stanno nelle tabelle di supporto `FNL_Fasi`, `Medici Aggiuntivi`, `Soglia Attesa`, `Tempo Visita` (parametri what-if) e `Tab_Presenti_Ora_Istituto`.

## A. Volumi, pazienti e valore

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Accessi` | Numero di accessi: un accesso è una riga della tabella dei fatti (un episodio al Pronto Soccorso). | `#,0` | Direzionale, Domanda potenziale, Flussi, Territorio · + 3 sottopagine · card KPI di Direzionale |
| `Pazienti` | Pazienti distinti (conteggio distinto di FK_Paziente). Un paziente può avere più accessi. | `#,0` | Flussi |
| `Accessi per paziente` | Accessi divisi per pazienti distinti. | `0.00` | card KPI di Flussi |
| `Paziente top` | Codice del paziente con più accessi nel contesto di filtro. | – | non usata |
| `Max accessi per paziente` | Numero massimo di accessi di un singolo paziente. | `#,0` | non usata |
| `Valore €` | Somma del valore economico delle prestazioni. È una valorizzazione tariffaria, non un costo. | `#,0 €` | Direzionale, Flussi, Territorio · card KPI di Direzionale |
| `Accessi V+B` | Accessi con triage in INGRESSO verde o bianco (gruppo «Minore (V/B)»). Idea di partenza della sottoprova 2, non è un KPI. | `#,0` | indiretta (via % V+B) |
| `% V+B` | Quota di accessi con triage in ingresso verde o bianco. | `0.0%` | non usata |
| `Valore € V+B` | Valore delle prestazioni degli accessi con triage in ingresso verde o bianco. | `#,0 €` | non usata |
| `Fascia di picco` | Ora del giorno con più accessi nel contesto, come testo «hh:00». | – | non usata |
| `Prestazioni` | Somma del numero di prestazioni registrate. | `#,0` | Flussi |
| `Accessi medi giornalieri` | Accessi diviso i giorni del periodo selezionato (solo giorni con dati). Su un asse per ora o per giorno della settimana = arrivi medi al giorno. | `#,0.0` | Attese e code, Flussi · + 1 sottopagina · card KPI di Flussi |
| `Valore medio per accesso €` | Valore medio delle prestazioni per accesso (valorizzazione tariffaria, non costo). | `#,0.0 €` | Territorio · card KPI di Flussi |
| `Accessi femmine` | Accessi di pazienti femmine (lato destro della piramide per età). | `#,0` | Flussi |
| `Accessi maschi` | Accessi di pazienti maschi con segno meno, per disegnarli a sinistra nella piramide per età (il formato nasconde il segno). | `#,0;#,0;0` | Flussi |
| `% arrivi autonomi` | Quota di accessi arrivati con mezzi propri, sugli accessi con modalità di arrivo nota (esclusi «Non rilevato» e vuoti). Chi arriva da solo può scegliere una CdC. | `0.0%` | Flussi · card KPI di Flussi |
| `Prestazioni per accesso` | Numero medio di prestazioni erogate per accesso al PS. | `0.0` | card KPI di Flussi |
| `Media Mobile 7 Giorni` | Media mobile a 7 giorni degli accessi giornalieri (toglie l'effetto del giorno della settimana). | – | Flussi |
| `% ricovero o trasferimento` | Quota di accessi che finiscono in ricovero o trasferimento ad altra struttura: casi che una Casa di Comunità non può gestire. | `0.0%` | Flussi |

<details><summary>Formule DAX · A. Volumi, pazienti e valore</summary>

**Accessi**

```dax
COUNTROWS(Fact_PS_2022)
```

**Pazienti**

```dax
DISTINCTCOUNT(Fact_PS_2022[FK_Paziente])
```

**Accessi per paziente**

```dax
DIVIDE([Accessi], [Pazienti])
```

**Paziente top**

```dax
VAR t = ADDCOLUMNS(VALUES(Fact_PS_2022[FK_Paziente]), "n", [Accessi])
RETURN MAXX(TOPN(1, t, [n], DESC), Fact_PS_2022[FK_Paziente])
```

**Max accessi per paziente**

```dax
MAXX(
    VALUES(Fact_PS_2022[FK_Paziente]),
    [Accessi]
)
```

**Valore €**

```dax
SUM(Fact_PS_2022[Valore_economico_prestazioni_PS])
```

**Accessi V+B**

```dax
CALCULATE([Accessi], Dim_Triage_Ingresso[Gruppo] = "Minore (V/B)")
```

**% V+B**

```dax
DIVIDE([Accessi V+B], [Accessi])
```

**Valore € V+B**

```dax
CALCULATE([Valore €], Dim_Triage_Ingresso[Gruppo] = "Minore (V/B)")
```

**Fascia di picco**

```dax
VAR t = ADDCOLUMNS(VALUES(DIm_Fasce_Orarie_Accetazionee[Ora]), "n", [Accessi])
RETURN MAXX(TOPN(1, t, [n], DESC), DIm_Fasce_Orarie_Accetazionee[Ora]) & ":00"
```

**Prestazioni**

```dax
SUM(Fact_PS_2022[Numero_prestazioni_PS])
```

**Accessi medi giornalieri**

```dax
DIVIDE (
    [Accessi],
    COUNTROWS ( FILTER ( Dim_Calendario_Accettazione, Dim_Calendario_Accettazione[In_periodo_dati] = TRUE () ) )
)
```

**Valore medio per accesso €**

```dax
DIVIDE ( [Valore €], [Accessi] )
```

**Accessi femmine**

```dax
CALCULATE ( [Accessi], DIm_Pazienti[sesso_descrizione] = "Femmina" )
```

**Accessi maschi**

```dax
- CALCULATE ( [Accessi], DIm_Pazienti[sesso_descrizione] = "Maschio" )
```

**% arrivi autonomi**

```dax
DIVIDE (
    CALCULATE ( [Accessi], Dim_Mod_Arrivo[Etichetta_breve] = "Autonomo" ),
    CALCULATE ( [Accessi], NOT Dim_Mod_Arrivo[Etichetta_breve] IN { "Non rilevato" }, NOT ISBLANK ( Dim_Mod_Arrivo[Etichetta_breve] ) )
)
```

**Prestazioni per accesso**

```dax
DIVIDE ( [Prestazioni], [Accessi] )
```

**Media Mobile 7 Giorni**

```dax
AVERAGEX(
    DATESINPERIOD(
        Fact_PS_2022[data_accettazione],
        MAX(Fact_PS_2022[data_accettazione]),
        -7,
        DAY
    ),
    CALCULATE(
        COUNT(Fact_PS_2022[PK_ID_Episodio])
    )
)
```

**% ricovero o trasferimento**

```dax
DIVIDE (
    CALCULATE ( [Accessi], Dim_Esito_Trattamento[Etichetta_breve] IN { "Ricovero", "Trasferimento" } ),
    [Accessi]
)
```

</details>

## B. Codici bianchi e ticket

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `% codici bianchi` | Accessi con triage in USCITA bianco ÷ tutti gli accessi. | `0.0%` | Direzionale, Flussi · card KPI di Direzionale |
| `Accessi codice bianco` | Accessi con triage in USCITA = B (bianco). La traccia chiede il triage in uscita. | `#,0` | Flussi |
| `Ticket stimato €` | Accessi con codice bianco in uscita × importo del ticket (25 €). Stima della compartecipazione, non costo del servizio. | `#,0 €` | Flussi |
| `Ticket registrato €` | Importo del ticket effettivamente registrato nel flusso (Dim_Ticket[Importo_eur] tramite FK_Codice_Ticket). | `#,0 €` | Flussi |
| `Scostamento ticket €` | Ticket stimato − ticket registrato: differenza tra la stima della traccia (25 € × codici bianchi in uscita) e l'importo registrato nel flusso. | `#,0 €` | card KPI di Flussi |

<details><summary>Formule DAX · B. Codici bianchi e ticket</summary>

**% codici bianchi**

```dax
DIVIDE([Accessi codice bianco], [Accessi])
```

**Accessi codice bianco**

```dax
CALCULATE([Accessi], Dim_Triage_Uscita[Codice] = "B")
```

**Ticket stimato €**

```dax
[Accessi codice bianco]
   * CALCULATE(MAX(Dim_Ticket[Importo_eur]), ALL(Dim_Ticket))
```

**Ticket registrato €**

```dax
SUMX ( Fact_PS_2022, RELATED ( Dim_Ticket[Importo_eur] ) )
```

**Scostamento ticket €**

```dax
[Ticket stimato €] - [Ticket registrato €]
```

</details>

## C. Attese, permanenza e pazienti presenti

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Durata mediana (min)` | Mediana accettazione → dimissione, in minuti, calcolata riga per riga (solo accessi con dimissione). Il KPI ufficiale è «Permanenza mediana (min)». | `#,0` | non usata |
| `Attesa mediana (min)` | Mediana di (presa in carico − arrivo), in minuti. | `#,0` | Attese e code, Direzionale · + 1 sottopagina · card KPI di Direzionale |
| `Attesa P90 (min)` | 90° percentile di (presa in carico − arrivo), in minuti (PERCENTILE.INC). | `#,0` | Attese e code · card KPI di Attese |
| `Permanenza mediana (min)` | Mediana di (dimissione − arrivo), in minuti. Gli accessi senza dimissione non entrano. | `#,0` | Attese e code · card KPI di Attese |
| `Permanenza P90 (min)` | 90° percentile di (dimissione − arrivo), in minuti. Gli accessi senza dimissione non entrano. | `#,0` | Attese e code, Direzionale · card KPI di Direzionale |
| `Accessi senza dimissione` | Accessi senza data/ora di dimissione: esclusi dai tempi di permanenza, restano nei volumi. | `#,0` | Attese e code |
| `Pazienti in coda (media)` | Pazienti presenti in media in un'ora: arrivati prima della fine dell'ora e dimessi dopo l'inizio dell'ora. Media sui giorni del periodo scelto. Esclusi gli accessi senza dimissione. Il filtro Pronto Soccorso resta attivo. | – | non usata |
| `Pazienti presenti (P90)` | 90° percentile dei pazienti presenti nell'ora (stessa regola della media). | `#,0.0` | non usata |
| `Tempo medio permanenza (min)` | Media accettazione → dimissione (formato giorni, non minuti). Non usata nel report: si usano mediana e P90. | – | non usata |
| `Durata Minutti Accettazione-PresaInCarico (min)` | Media arrivo → presa in carico, in minuti. Non usata nel report (si usano mediana e P90). | – | solo bozze |
| `Durata Minutti Accettazione-Dimissione (min)` | Media arrivo → dimissione, in minuti. Non usata nel report. | – | solo bozze |
| `Durata Minutti PresaInCarico-Dimissione (min)` | Media presa in carico → dimissione, in minuti. Non usata nel report. | – | solo bozze |
| `Attesa mediana bianchi e verdi (min)` | Attesa mediana (accettazione → presa in carico) dei soli codici bianchi e verdi in ingresso: i casi a bassa priorità, candidati alle CdC. | `#,0` | card KPI di Attese |
| `Permanenza mediana bianchi e verdi (min)` | Permanenza mediana in PS dei soli codici bianchi e verdi in ingresso. | `#,0` | card KPI di Attese |
| `% attesa oltre 1 ora` | Quota di accessi che aspettano più di 1 ora tra accettazione e presa in carico (sugli accessi con il dato). Soglia scelta dal gruppo per la leggibilità. | `0%` | Attese e code |
| `% permanenza oltre 6 ore` | Quota di accessi che restano in PS più di 6 ore tra accettazione e dimissione (sugli accessi con dimissione registrata). Soglia scelta dal gruppo per la leggibilità. | `0%` | Attese e code |
| `Presenti (media)` | Pazienti presenti per ora, media sui giorni (tabella Tab_Presenti_Ora_Istituto). | – | non usata |
| `In coda (media)` | Pazienti arrivati ma non ancora presi in carico, in media per ora. | – | + 1 sottopagina |
| `Accessi (media per ora)` | Arrivi medi per ora e per PS (usata nello studio code). | – | non usata |
| `Personale (media)` | Personale presente in media per ora e per PS, dalla tabella dei turni. | – | non usata |
| `Personale (tab)` | Personale presente per ora, dalla tabella calcolata. | – | indiretta (via Coda per operatore) |
| `Coda per operatore` | Pazienti in coda ÷ personale presente. | – | + 1 sottopagina |

<details><summary>Formule DAX · C. Attese, permanenza e pazienti presenti</summary>

**Durata mediana (min)**

```dax
MEDIANX(
    FILTER(Fact_PS_2022, NOT ISBLANK(Fact_PS_2022[data_ora_dimissione])),
    DATEDIFF(Fact_PS_2022[data_ora_accettazione], Fact_PS_2022[data_ora_dimissione], MINUTE))
```

**Attesa mediana (min)**

```dax
ROUND(MEDIAN(Fact_PS_2022[durata_accettazione_prcar]) * 1440, 0)
```

**Attesa P90 (min)**

```dax
ROUND(PERCENTILE.INC(Fact_PS_2022[durata_accettazione_prcar], 0.9) * 1440, 0)
```

**Permanenza mediana (min)**

```dax
ROUND(MEDIAN(Fact_PS_2022[durata_accettazione_dimissione]) * 1440, 0)
```

**Permanenza P90 (min)**

```dax
ROUND(PERCENTILE.INC(Fact_PS_2022[durata_accettazione_dimissione], 0.9) * 1440, 0)
```

**Accessi senza dimissione**

```dax
CALCULATE ( [Accessi], ISBLANK ( Fact_PS_2022[data_ora_dimissione] ) )
```

**Pazienti in coda (media)**

```dax
VAR h = SELECTEDVALUE ( Fact_PS_2022[ora_intera_accettazione] )
RETURN
    IF (
        NOT ISBLANK ( h ),
        AVERAGEX (
            CALCULATETABLE (
                VALUES ( Dim_Calendario_Accettazione[Data] ),
                Dim_Calendario_Accettazione[In_periodo_dati] = TRUE ()
            ),
            VAR inizio = Dim_Calendario_Accettazione[Data] + h / 24
            VAR fine = inizio + 1 / 24
            RETURN
                CALCULATE (
                    COUNTROWS ( Fact_PS_2022 ),
                    REMOVEFILTERS ( Dim_Calendario_Accettazione ),
                    REMOVEFILTERS ( Fact_PS_2022[ora_intera_accettazione] ),
                    Fact_PS_2022[data_ora_accettazione] < fine,
                    Fact_PS_2022[data_ora_prcar] > inizio
                ) + 0
        )
    )
```

**Pazienti presenti (P90)**

```dax
VAR giorni = CALCULATETABLE ( VALUES ( Dim_Calendario_Accettazione[Data] ), Dim_Calendario_Accettazione[In_periodo_dati] = TRUE () )
RETURN
    PERCENTILEX.INC (
        FILTER ( Ore_presenza, Ore_presenza[Data] IN giorni ),
        VAR i = Ore_presenza[Inizio]
        VAR f = Ore_presenza[Fine]
        RETURN
            CALCULATE (
                COUNTROWS ( Fact_PS_2022 ),
                REMOVEFILTERS ( Dim_Calendario_Accettazione ),
                Fact_PS_2022[data_ora_accettazione] < f,
                Fact_PS_2022[data_ora_dimissione] > i
            ) + 0,
        0.9
    )
```

**Tempo medio permanenza (min)**

```dax
CALCULATE (
    AVERAGE ( Fact_PS_2022[durata_accettazione_dimissione] ),
    NOT ISBLANK ( Fact_PS_2022[data_ora_dimissione] )
)
```

**Durata Minutti Accettazione-PresaInCarico (min)**

```dax
AVERAGE ( Fact_PS_2022[durata_accettazione_prcar] ) * 1440
```

**Durata Minutti Accettazione-Dimissione (min)**

```dax
AVERAGE ( Fact_PS_2022[durata_accettazione_dimissione] ) * 1440
```

**Durata Minutti PresaInCarico-Dimissione (min)**

```dax
AVERAGE ( Fact_PS_2022[durata_prcar_dimissione] ) * 1440
```

**Attesa mediana bianchi e verdi (min)**

```dax
CALCULATE ( [Attesa mediana (min)], Dim_Triage_Ingresso[Codice] IN { "B", "V" } )
```

**Permanenza mediana bianchi e verdi (min)**

```dax
CALCULATE ( [Permanenza mediana (min)], Dim_Triage_Ingresso[Codice] IN { "B", "V" } )
```

**% attesa oltre 1 ora**

```dax
DIVIDE (
    CALCULATE ( [Accessi], Fact_PS_2022[durata_accettazione_prcar] > 1 / 24 ),
    CALCULATE ( [Accessi], NOT ISBLANK ( Fact_PS_2022[durata_accettazione_prcar] ) )
)
```

**% permanenza oltre 6 ore**

```dax
DIVIDE (
    CALCULATE ( [Accessi], Fact_PS_2022[durata_accettazione_dimissione] > 6 / 24 ),
    CALCULATE ( [Accessi], NOT ISBLANK ( Fact_PS_2022[durata_accettazione_dimissione] ) )
)
```

**Presenti (media)**

```dax
AVERAGEX (
    VALUES ( Tab_Presenti_Ora_Istituto[Giorno_sett_num] ),
    CALCULATE ( SUM ( Tab_Presenti_Ora_Istituto[Pazienti_presenti_media] ) )
)
```

**In coda (media)**

```dax
AVERAGEX (
    VALUES ( Tab_Presenti_Ora_Istituto[Giorno_sett_num] ),
    CALCULATE ( SUM ( Tab_Presenti_Ora_Istituto[Pazienti_in_coda_media] ) )
)
```

**Accessi (media per ora)**

```dax
VAR h = SELECTEDVALUE ( Tab_Presenti_Ora_Istituto[Ora] )
VAR ist = VALUES ( Tab_Presenti_Ora_Istituto[Istituto] )
VAR gg = VALUES ( Tab_Presenti_Ora_Istituto[Giorno_sett_num] )
VAR accessi =
    CALCULATE (
        COUNTROWS ( Fact_PS_2022 ),
        Fact_PS_2022[ora_intera_accettazione] = h,
        TREATAS ( ist, Fact_PS_2022[FK_Codice_Identificativo_PS] ),
        TREATAS ( gg, Dim_Calendario_Accettazione[Giorno_sett_num] ),
        Dim_Calendario_Accettazione[In_periodo_dati] = TRUE ()
    )
VAR giorni =
    CALCULATE (
        COUNTROWS ( Dim_Calendario_Accettazione ),
        TREATAS ( gg, Dim_Calendario_Accettazione[Giorno_sett_num] ),
        Dim_Calendario_Accettazione[In_periodo_dati] = TRUE ()
    )
RETURN
    IF ( NOT ISBLANK ( h ), DIVIDE ( accessi, giorni ) )
```

**Personale (media)**

```dax
VAR h = SELECTEDVALUE ( Tab_Presenti_Ora_Istituto[Ora] )
VAR ist = VALUES ( Tab_Presenti_Ora_Istituto[Istituto] )
VAR gg = VALUES ( Tab_Presenti_Ora_Istituto[Giorno_sett_num] )

VAR giorniSel =    
    CALCULATETABLE (        
        SELECTCOLUMNS (            
            VALUES ( Dim_Calendario_Accettazione[Data] ),            
            "GiornoData", Dim_Calendario_Accettazione[Data]        ),        
        TREATAS ( gg, Dim_Calendario_Accettazione[Giorno_sett_num] ),        
        Dim_Calendario_Accettazione[In_periodo_dati] = TRUE ()    )

RETURN    
    IF (        
        NOT ISBLANK ( h ),        
        AVERAGEX (            
            giorniSel,            
            CALCULATE (                    
                SUM ( Dim_Turni_Accettazione[Totale_Personale] ),                    
                REMOVEFILTERS ( Dim_Calendario_Accettazione ),                    
                TREATAS ( ist, Dim_Turni_Accettazione[codice_istituto] ),                    
                FILTER (
                    Dim_Turni_Accettazione,
                    VAR hIni = HOUR ( Dim_Turni_Accettazione[Inizio_Turno] )
                    VAR hFin = HOUR ( Dim_Turni_Accettazione[Fine_Turno] )
                    RETURN
                        IF ( 
                            hIni < hFin, 
                            h >= hIni && h < hFin,   -- Turno diurno normale (es. 07:00 - 14:00)
                            h >= hIni || h < hFin    -- Turno notturno a cavallo di mezzanotte (es. 21:00 - 07:00)
                        )
                )
            ) + 0        )    )
```

**Personale (tab)**

```dax
AVERAGEX (
    VALUES ( Tab_Presenti_Ora_Istituto[Giorno_sett_num] ),
    CALCULATE ( SUM ( Tab_Presenti_Ora_Istituto[Personale_media] ) )
)
```

**Coda per operatore**

```dax
DIVIDE ( [In coda (media)], [Personale (tab)] )
```

</details>

## D. Territorio

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Accessi per 1.000 ab.` | Accessi ogni 1.000 residenti del comune (popolazione ISTAT 2022). La popolazione è contata una sola volta per comune: nei comuni nati da fusione la dimensione ha più codici con la stessa popolazione ripetuta. | `#,0.0` | Territorio · + 1 sottopagina |
| `Comuni con accessi` | Numero di comuni di residenza con almeno un accesso. | `#,0` | Territorio · card KPI di Territorio |
| `Quota accessi sul totale` | Accessi del comune / accessi totali del contesto (ignora il filtro sui comuni). | `0.0%` | Territorio |
| `Quota accessi top 10 comuni` | Quota di accessi che arriva dai 10 comuni con piu' accessi. | `0.0%` | Territorio · card KPI di Territorio |
| `% accessi da fuori provincia` | Quota di accessi di residenti fuori dalla provincia di Varese (estero compreso), sugli accessi con residenza nota. | `0.0%` | card KPI di Territorio |
| `Accessi per 1.000 ab. provincia Varese` | Accessi dei residenti in provincia di Varese ogni 1.000 abitanti della provincia (ISTAT 2022). Fissa la provincia: è il bacino dell'ASST e l'unico con popolazione completa. | `#,0.0` | card KPI di Territorio |
| `Accessi per 1.000 ab. comuni da 3.000 ab.` | Accessi ogni 1.000 residenti solo per i comuni con almeno 3.000 abitanti: nei paesi piccoli pochi accessi fanno oscillare molto il tasso. | `#,0` | Territorio |

<details><summary>Formule DAX · D. Territorio</summary>

**Accessi per 1.000 ab.**

```dax
VAR pop =
    SUMX (
        SUMMARIZE ( Dim_Comuni_Residenze, Dim_Comuni_Residenze[Comune], Dim_Comuni_Residenze[Popolazione_2022] ),
        Dim_Comuni_Residenze[Popolazione_2022]
    )
RETURN
    DIVIDE ( [Accessi], pop ) * 1000
```

**Comuni con accessi**

```dax
CALCULATE ( DISTINCTCOUNT ( Fact_PS_2022[FK_Codice_Comune_Residenza] ), NOT ISBLANK ( Fact_PS_2022[FK_Codice_Comune_Residenza] ) )
```

**Quota accessi sul totale**

```dax
DIVIDE ( [Accessi], CALCULATE ( [Accessi], REMOVEFILTERS ( Dim_Comuni_Residenze ) ) )
```

**Quota accessi top 10 comuni**

```dax
VAR top10 = TOPN ( 10, VALUES ( Dim_Comuni_Residenze[PK_Codice_Comune] ), [Accessi] )
RETURN DIVIDE ( SUMX ( top10, [Accessi] ), CALCULATE ( [Accessi], REMOVEFILTERS ( Dim_Comuni_Residenze ) ) )
```

**% accessi da fuori provincia**

```dax
DIVIDE (
    CALCULATE ( [Accessi], NOT ISBLANK ( Dim_Comuni_Residenze[Provincia] ), NOT Dim_Comuni_Residenze[Provincia] IN { "Non trovato", "Varese" } ),
    CALCULATE ( [Accessi], NOT ISBLANK ( Dim_Comuni_Residenze[Provincia] ), Dim_Comuni_Residenze[Provincia] <> "Non trovato" )
)
```

**Accessi per 1.000 ab. provincia Varese**

```dax
CALCULATE ( [Accessi per 1.000 ab.], Dim_Comuni_Residenze[Provincia] = "Varese" )
```

**Accessi per 1.000 ab. comuni da 3.000 ab.**

```dax
VAR pop =
    SUMX (
        SUMMARIZE ( Dim_Comuni_Residenze, Dim_Comuni_Residenze[Comune], Dim_Comuni_Residenze[Popolazione_2022] ),
        Dim_Comuni_Residenze[Popolazione_2022]
    )
RETURN IF ( pop >= 3000, [Accessi per 1.000 ab.] )
```

</details>

## E. Confronto con il mese precedente (KPI della Direzionale)

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Accessi mese prec` | Accessi del mese precedente al mese di riferimento (ignora il filtro mese). | `#,0` | solo bozze |
| `Mese rif` | Numero dell'ultimo mese con dati nel periodo scelto: è il «mese di riferimento» dei confronti. | `0` | card KPI di Attese, Direzionale, Domanda, Flussi, Territorio |
| `Var % accessi` | Variazione % degli accessi: mese di riferimento rispetto al mese precedente. | `+0.0%;-0.0%;0.0%` | indiretta (via KPI card accessi, KPI sub accessi) |
| `Accessi mese` | Accessi del mese di riferimento (ignora il filtro mese). | `#,0` | indiretta (via KPI card accessi, KPI sub accessi) |
| `Mese rif breve` | Nome breve dell'ultimo mese con dati nel periodo scelto ('Mese rif'). | – | indiretta (via KPI card accessi, KPI card attesa mediana …) |
| `Mese prec breve` |  | – | indiretta (via KPI card accessi, KPI card attesa mediana …) |
| `Media mensile accessi` | Media mensile degli accessi su tutto il periodo dati (gen-giu 2022), indipendente dal mese scelto. | `#,0` | indiretta (via KPI sub accessi vs media) |
| `Valore € mese` |  | `#,0 €` | indiretta (via KPI card valore, KPI sub valore) |
| `Valore € mese prec` |  | `#,0 €` | indiretta (via KPI card valore, KPI sub valore) |
| `Var % valore` |  | `+0.0%;-0.0%;0.0%` | indiretta (via KPI card valore, KPI sub valore) |
| `Attesa mediana mese` |  | `#,0` | indiretta (via KPI card attesa mediana, KPI sub attesa mediana) |
| `Attesa mediana mese prec` |  | `#,0` | indiretta (via KPI card attesa mediana, KPI sub attesa mediana) |
| `Var % attesa mediana` |  | `+0.0%;-0.0%;0.0%` | indiretta (via Colore KPI attesa mediana, KPI card attesa mediana …) |
| `Permanenza P90 mese` |  | `#,0` | indiretta (via KPI card permanenza P90, KPI sub permanenza P90) |
| `Permanenza P90 mese prec` |  | `#,0` | indiretta (via KPI card permanenza P90, KPI sub permanenza P90) |
| `Var % permanenza P90` |  | `+0.0%;-0.0%;0.0%` | indiretta (via Colore KPI permanenza P90, KPI card permanenza P90 …) |
| `% codici bianchi mese` |  | `0.0%` | indiretta (via KPI card codici bianchi, KPI sub codici bianchi) |
| `% codici bianchi mese prec` |  | `0.0%` | indiretta (via KPI card codici bianchi, KPI sub codici bianchi) |
| `Var % codici bianchi` |  | `+0.0%;-0.0%;0.0%` | indiretta (via Colore KPI codici bianchi, KPI card codici bianchi …) |

<details><summary>Formule DAX · E. Confronto con il mese precedente (KPI della Direzionale)</summary>

**Accessi mese prec**

```dax
VAR m = [Mese rif] - 1
RETURN CALCULATE([Accessi], REMOVEFILTERS(Dim_Calendario_Accettazione),
                 Dim_Calendario_Accettazione[Mese_num] = m)
```

**Mese rif**

```dax
MAXX(VALUES(Fact_PS_2022[data_accettazione]),
                MONTH(Fact_PS_2022[data_accettazione]))
```

**Var % accessi**

```dax
DIVIDE([Accessi mese] - [Accessi mese prec], [Accessi mese prec])
```

**Accessi mese**

```dax
VAR m = [Mese rif]
RETURN CALCULATE([Accessi], REMOVEFILTERS(Dim_Calendario_Accettazione),
                 Dim_Calendario_Accettazione[Mese_num] = m)
```

**Mese rif breve**

```dax
VAR m = [Mese rif]
RETURN CALCULATE ( MAX ( Dim_Calendario_Accettazione[Mese_breve] ), REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Mese prec breve**

```dax
VAR m = [Mese rif] - 1
RETURN CALCULATE ( MAX ( Dim_Calendario_Accettazione[Mese_breve] ), REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Media mensile accessi**

```dax
CALCULATE (
    AVERAGEX ( VALUES ( Dim_Calendario_Accettazione[Mese_num] ), [Accessi] ),
    REMOVEFILTERS ( Dim_Calendario_Accettazione ),
    Dim_Calendario_Accettazione[In_periodo_dati] = TRUE ()
)
```

**Valore € mese**

```dax
VAR m = [Mese rif]
RETURN CALCULATE ( [Valore €], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Valore € mese prec**

```dax
VAR m = [Mese rif] - 1
RETURN CALCULATE ( [Valore €], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Var % valore**

```dax
DIVIDE ( [Valore € mese] - [Valore € mese prec], [Valore € mese prec] )
```

**Attesa mediana mese**

```dax
VAR m = [Mese rif]
RETURN CALCULATE ( [Attesa mediana (min)], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Attesa mediana mese prec**

```dax
VAR m = [Mese rif] - 1
RETURN CALCULATE ( [Attesa mediana (min)], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Var % attesa mediana**

```dax
DIVIDE ( [Attesa mediana mese] - [Attesa mediana mese prec], [Attesa mediana mese prec] )
```

**Permanenza P90 mese**

```dax
VAR m = [Mese rif]
RETURN CALCULATE ( [Permanenza P90 (min)], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Permanenza P90 mese prec**

```dax
VAR m = [Mese rif] - 1
RETURN CALCULATE ( [Permanenza P90 (min)], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Var % permanenza P90**

```dax
DIVIDE ( [Permanenza P90 mese] - [Permanenza P90 mese prec], [Permanenza P90 mese prec] )
```

**% codici bianchi mese**

```dax
VAR m = [Mese rif]
RETURN CALCULATE ( [% codici bianchi], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**% codici bianchi mese prec**

```dax
VAR m = [Mese rif] - 1
RETURN CALCULATE ( [% codici bianchi], REMOVEFILTERS ( Dim_Calendario_Accettazione ), Dim_Calendario_Accettazione[Mese_num] = m )
```

**Var % codici bianchi**

```dax
DIVIDE ( [% codici bianchi mese] - [% codici bianchi mese prec], [% codici bianchi mese prec] )
```

</details>

## F. Domanda potenziale CdC (imbuto unico)

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Accessi compatibili CdC` | IMBUTO UNICO del progetto (traccia SP2, 'Domanda compatibile'): accessi con Classificazione3_CdC = Potenzialmente compatibile, cioè tutti i criteri veri (diagnosi primaria, triage ingresso e uscita, esito, durata presa in carico-dimissione ≤ 2 h, diagnosi secondaria se presente). Totale 20.419. | `#,0` | Domanda potenziale · + 1 sottopagina · card KPI di Domanda |
| `FNL Step 1 - Triage Ingresso` | Imbuto, passo 1: accessi con triage in ingresso compatibile (verde o bianco). | `0` | indiretta (via FNL Valore) |
| `FNL Step 2 - + Diagnosi` | Imbuto, passo 2: … e diagnosi primaria compatibile. | `0` | indiretta (via FNL Valore) |
| `FNL Step 3 - + Esito` | Imbuto, passo 3: … ed esito compatibile. | `0` | indiretta (via FNL Valore) |
| `FNL Step 4 - + Durata` | Imbuto, passo 4: … e durata presa in carico → dimissione ≤ 2 ore. | `0` | indiretta (via FNL Valore) |
| `FNL Step 5 - + Triage Uscita` | Imbuto, passo 5: … e triage in uscita compatibile. | `0` | indiretta (via FNL Valore) |
| `FNL Step 6 - + Diagnosi Secondaria` | Imbuto, passo 6: … e diagnosi secondaria compatibile, se presente. | `0` | indiretta (via FNL Valore) |
| `FNL Step 7 - Episodio Compatibile CdC` | Imbuto, passo 7 (ultimo): accessi con Episodio_Compatibile_CdC = TRUE. Coincide con «Accessi compatibili CdC». | `0` | indiretta (via FNL Valore) |
| `FNL Step 0 - Accessi Totali` | Imbuto, passo 0: tutti gli accessi. | `0` | indiretta (via FNL Valore) |
| `% Accessi Compatibili CdC` | Accessi compatibili CdC ÷ tutti gli accessi. | `0.0%` | Domanda potenziale · + 2 sottopagine · card KPI di Direzionale |
| `Valore economico compatibili CdC` | Somma del valore delle prestazioni degli accessi compatibili CdC. | `#,0 €` | Domanda potenziale · card KPI di Domanda |
| `% valore economico  compatibili CdC` | Valore dei compatibili ÷ valore totale delle prestazioni. | – | Domanda potenziale · card KPI di Domanda |
| `Accessi non classificabili CdC` | Accessi con Classificazione3_CdC = Non classificabile: nessun criterio falso, ma almeno un dato mancante (diagnosi secondaria esclusa). Traccia SP2: casi dubbi da segnalare, non da contare come compatibili. | `#,0` | + 1 sottopagina |
| `Accessi non compatibili CdC` | Accessi con Classificazione3_CdC = Non compatibile: almeno un criterio dell'imbuto è falso. | `#,0` | + 1 sottopagina |
| `Quota CdC base dati` | Accessi potenzialmente compatibili che restano a ogni passo della tabella 'Quota CdC passi': chi decide da solo e arriva con mezzi propri, e chi arriva quando anche una CdC spoke è aperta (lun-sab 8-20, non festivi). Giustifica la quota base del 50%. | `#,0` | + 1 sottopagina |
| `FNL Valore` | Valore mostrato dal funnel «Da 75.664 accessi a 20.419 compatibili»: sceglie la misura FNL Step in base alla fase. | `0` | Domanda potenziale |

<details><summary>Formule DAX · F. Domanda potenziale CdC (imbuto unico)</summary>

**Accessi compatibili CdC**

```dax
CALCULATE ( COUNTROWS ( Fact_PS_2022 ), Fact_PS_2022[Classificazione3_CdC] = "Potenzialmente compatibile" )
```

**FNL Step 1 - Triage Ingresso**

```dax
CALCULATE (
    COUNTROWS ( Fact_PS_2022 ),
    Dim_Triage_Ingresso[Compatibile_CdC] = TRUE ()
)
```

**FNL Step 2 - + Diagnosi**

```dax
CALCULATE (
    [FNL Step 1 - Triage Ingresso],
    DIm_Diagnosi_Primaria[Compatibile_CdC] = TRUE ()
)
```

**FNL Step 3 - + Esito**

```dax
CALCULATE (
    [FNL Step 2 - + Diagnosi],
    Dim_Esito_Trattamento[Compatibile_CdC] = TRUE ()
)
```

**FNL Step 4 - + Durata**

```dax
CALCULATE (
    [FNL Step 3 - + Esito],
    Fact_PS_2022[Compatibile_CdC_Durata_Prestazione] = TRUE ()
)
```

**FNL Step 5 - + Triage Uscita**

```dax
CALCULATE (
    [FNL Step 4 - + Durata],
    Dim_Triage_Uscita[Compatibile_CdC] = TRUE ()
)
```

**FNL Step 6 - + Diagnosi Secondaria**

```dax
CALCULATE (
    [FNL Step 5 - + Triage Uscita],
    FILTER (
        Fact_PS_2022,
        ISBLANK ( Fact_PS_2022[FK_Codice_Diagnosi_Secondaria] )
            || RELATED ( DIm_Diagnosi_Secondaria[Compatibile_CdC] ) = TRUE ()
    )
)
```

**FNL Step 7 - Episodio Compatibile CdC**

```dax
CALCULATE (
    [FNL Step 6 - + Diagnosi Secondaria],
    Fact_PS_2022[Episodio_Compatibile_CdC] = TRUE ()
)
```

**FNL Step 0 - Accessi Totali**

```dax
COUNTROWS(Fact_PS_2022)
```

**% Accessi Compatibili CdC**

```dax
DIVIDE(
    [Accessi compatibili CdC],
    COUNTROWS(Fact_PS_2022),
    0
)
```

**Valore economico compatibili CdC**

```dax
CALCULATE (
    SUM ( Fact_PS_2022[Valore_economico_prestazioni_PS] ),
    Fact_PS_2022[Episodio_Compatibile_CdC] = TRUE ()
)
```

**% valore economico  compatibili CdC**

```dax
DIVIDE (
    [Valore economico compatibili CdC],
    SUM ( Fact_PS_2022[Valore_economico_prestazioni_PS] )
)
```

**Accessi non classificabili CdC**

```dax
CALCULATE ( COUNTROWS ( Fact_PS_2022 ), Fact_PS_2022[Classificazione3_CdC] = "Non classificabile" )
```

**Accessi non compatibili CdC**

```dax
CALCULATE ( COUNTROWS ( Fact_PS_2022 ), Fact_PS_2022[Classificazione3_CdC] = "Non compatibile" )
```

**Quota CdC base dati**

```dax
SWITCH (
    SELECTEDVALUE ( 'Quota CdC passi'[Ordine] ),
    1, [Accessi compatibili CdC],
    2, CALCULATE ( [Accessi compatibili CdC], Dim_Responsabile_Invio[Etichetta_breve] = "Decisione propria", Dim_Mod_Arrivo[Gruppo_arrivo] = "Autonomo" ),
    3, CALCULATE ( [Accessi compatibili CdC], Dim_Responsabile_Invio[Etichetta_breve] = "Decisione propria", Dim_Mod_Arrivo[Gruppo_arrivo] = "Autonomo",
            Fact_PS_2022[ora_intera_accettazione] >= 8, Fact_PS_2022[ora_intera_accettazione] < 20,
            Dim_Calendario_Accettazione[Giorno_sett_num] <= 6, Dim_Calendario_Accettazione[Festivo] = FALSE () )
)
```

**FNL Valore**

```dax
SWITCH(
    SELECTEDVALUE(FNL_Fasi[Fase]),
    "Accessi Totali", [FNL Step 0 - Accessi Totali],
    "- Triage Ingresso", [FNL Step 1 - Triage Ingresso],
    "- Diagnosi", [FNL Step 2 - + Diagnosi],
    "- Esito", [FNL Step 3 - + Esito],
    "- Durata", [FNL Step 4 - + Durata],
    "- Triage Uscita", [FNL Step 5 - + Triage Uscita],
    "- Diagnosi Secondaria", [FNL Step 6 - + Diagnosi Secondaria],
    "Episodio Compatibile CdC", [FNL Step 7 - Episodio Compatibile CdC]
)
```

</details>

## G. Scenari CdC e studio delle code (M/M/c)

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Giorni periodo` | Numero di giorni con dati nel contesto (181 sul periodo intero). | `0` | indiretta (via Lambda (pz/ora), Lambda dopo CdC (pz/ora)) |
| `Ore turno` | Durata del turno in ore: mattina 7, pomeriggio 7, notte 10. | `0` | indiretta (via Lambda (pz/ora), Lambda dopo CdC (pz/ora)) |
| `Lambda (pz/ora)` | Studio code: arrivi per ora = accessi ÷ (giorni × ore del turno). | `0.00` | indiretta (via Carico, Medici minimi) |
| `Medici` | Studio code: medici presenti nel turno (tabella del personale, dalla traccia). | `0` | indiretta (via Medici scenario) |
| `Medici scenario` | Studio code: medici del turno più i «Medici Aggiuntivi» scelti con il parametro. | `0` | indiretta (via Medici mancanti dopo CdC, Medici mancanti prima) |
| `Mu (pz/ora per medico)` | Studio code: pazienti visti in un'ora da un medico = 60 ÷ tempo di visita. | – | indiretta (via Carico, Medici minimi) |
| `Carico` | Studio code: carico offerto a = λ ÷ μ. | `0.00` | indiretta (via P attesa, Rho) |
| `Rho` | Studio code: utilizzo dei medici ρ = λ ÷ (medici × μ). Da 1 in su la coda non si stabilizza. | `0.00` | indiretta (via P attesa, Stato turno prima) |
| `P attesa` | Studio code: probabilità di attendere (formula di Erlang C, coda M/M/c). | `0.00` | indiretta (via Wq modello (min)) |
| `Wq modello (min)` | Studio code: attesa media in coda del modello M/M/c, in minuti. Vuota se ρ ≥ 1. | `#,0.0` | indiretta (via Stato turno prima) |
| `Medici minimi` | Studio code: medici minimi perché l'attesa del modello resti sotto la soglia scelta. | `0` | indiretta (via Medici liberati dalle CdC, Medici mancanti prima) |
| `Quota CdC compatibili` | Quota dei verdi compatibili (in orario CdC) che la CdC riesce davvero a prendere in carico. Viene dallo scenario scelto; senza scelta vale 50% (esempio della traccia). | `0%` | Domanda potenziale · card KPI di Domanda |
| `Quota CdC non classificabili` | Quota dei verdi non classificabili (in orario CdC) assorbita dalla CdC. Vale 0 tranne nello scenario Ampio. | `0%` | indiretta (via Accessi deviati alle CdC) |
| `Scenario CdC attivo` | Nome dello scenario scelto (per titoli e commenti). | – | indiretta (via Lettura scenario CdC) |
| `Accessi deviati alle CdC` | Domanda presa in carico (traccia SP2): quota dello scenario × accessi compatibili, più l'eventuale quota dei non classificabili (solo scenario 5). Tutte le ore: le CdC hub sono aperte h24 (DM 77). | `#,0` | + 2 sottopagine |
| `Accessi dopo CdC` | Accessi che restano al PS dopo la deviazione verso le CdC (accessi − accessi deviati). | `#,0` | indiretta (via Lambda dopo CdC (pz/ora)) |
| `Riduzione accessi PS %` | Accessi deviati ÷ accessi totali. Stima teorica a tutte le ore. | `0.0%` | + 1 sottopagina |
| `Lambda dopo CdC (pz/ora)` | Studio code: arrivi per ora dopo la deviazione. | `0.00` | indiretta (via Medici minimi dopo CdC, Rho dopo CdC) |
| `Rho dopo CdC` | Utilizzo dei medici dopo la deviazione (lambda' / (c x mu)). | `0.00` | indiretta (via Stato turno dopo CdC) |
| `Wq dopo CdC (min)` | Attesa media in coda (Erlang C, M/M/c) dopo la deviazione. Vuota se il sistema e' instabile (rho >= 1). | `#,0.0` | indiretta (via Stato turno dopo CdC) |
| `Stato turno prima` | Stato del turno oggi: Instabile (rho >= 1), Critico (attesa del modello sopra la soglia) oppure Ok. | – | indiretta (via Turni critici prima) |
| `Stato turno dopo CdC` | Stato del turno dopo la deviazione: Instabile, Critico oppure Ok. | – | indiretta (via Turni critici dopo CdC) |
| `Medici minimi dopo CdC` | Numero minimo di medici perche' l'attesa del modello resti sotto la soglia, dopo la deviazione verso le CdC. | `0` | indiretta (via Medici liberati dalle CdC, Medici mancanti dopo CdC) |
| `Medici liberati dalle CdC` | Medici in meno necessari nel turno grazie alla deviazione (medici minimi prima - dopo). | `0` | indiretta (via Ore-medico liberate a settimana) |
| `Medici mancanti prima` | Medici che mancano oggi per stare sotto la soglia (minimi - in organico, mai negativo). | `0` | indiretta (via Medici-turno mancanti prima) |
| `Medici mancanti dopo CdC` | Medici che mancano nel turno dopo la deviazione (mai negativo). | `0` | indiretta (via Medici-turno mancanti dopo CdC) |
| `Turni PS-turno (n)` | Numero di combinazioni PS x turno nel contesto (21 in totale). | `0` | indiretta (via Lettura scenario CdC) |
| `Turni critici prima` | Turni PS x turno instabili (rho>=1) o con attesa del modello sopra la soglia, oggi. | `0` | + 1 sottopagina |
| `Turni critici dopo CdC` | Numero di turni (su 21) instabili o con attesa del modello sopra la soglia, dopo la deviazione. | `0` | + 1 sottopagina |
| `Turni instabili prima` | Turni con ρ ≥ 1 oggi. | `0` | non usata |
| `Turni instabili dopo CdC` | Turni con ρ ≥ 1 dopo la deviazione. | `0` | non usata |
| `Medici-turno in organico` | Somma dei medici presenti nei turni (un medico in un turno = 1 medico-turno). Include i Medici Aggiuntivi dello scenario. | `0` | non usata |
| `Medici-turno minimi prima` | Medici-turno necessari oggi per stare sotto la soglia di attesa (modello Erlang C). | `0` | non usata |
| `Medici-turno minimi dopo CdC` | Medici-turno necessari dopo la deviazione verso le CdC. | `0` | non usata |
| `Medici-turno mancanti prima` | Dove i medici in organico sono meno dei minimi (somma dei soli deficit, i turni in surplus non compensano). | `0` | indiretta (via Lettura medici mancanti) |
| `Medici-turno mancanti dopo CdC` | Somma dei deficit di medici per turno, dopo la deviazione. | `0` | + 1 sottopagina |
| `Ore-medico liberate a settimana` | Ore-medico in meno a settimana grazie alla deviazione (medici liberati × ore del turno × 7). | `#,0` | non usata |
| `Medici Aggiuntivi Value` | Parametro what-if: medici in più per turno (0-3), scelto con lo slicer «Medici Aggiuntivi». | `0` | indiretta (via Medici scenario) |
| `Soglia Attesa Value` | Parametro what-if: soglia di attesa in minuti (5-60, default 15). | `0` | indiretta (via Lettura medici mancanti, Medici minimi dopo CdC) |
| `Tempo Visita Value` | Parametro what-if: tempo di visita in minuti (10-40, default 20). | `0` | indiretta (via Lettura medici mancanti, Mu (pz/ora per medico)) |

<details><summary>Formule DAX · G. Scenari CdC e studio delle code (M/M/c)</summary>

**Giorni periodo**

```dax
CALCULATE(COUNTROWS(Dim_Calendario_Accettazione),
    Dim_Calendario_Accettazione[In_periodo_dati] = TRUE())
```

**Ore turno**

```dax
VAR t = RIGHT(SELECTEDVALUE(Fact_PS_2022[FK_PS_Turno_Accettazione]), 1)
  RETURN SWITCH(t, "M", 7, "P", 7, "N", 10)
```

**Lambda (pz/ora)**

```dax
DIVIDE([Accessi], [Giorni periodo] * [Ore turno])
```

**Medici**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]),
    LOOKUPVALUE(Dim_Turni_Accettazione[Medici],
      Dim_Turni_Accettazione[PK_PS_Turno],
      Fact_PS_2022[FK_PS_Turno_Accettazione]))
```

**Medici scenario**

```dax
IF(HASONEVALUE(Fact_PS_2022[FK_PS_Turno_Accettazione]),
    [Medici] + [Medici Aggiuntivi Value])
```

**Mu (pz/ora per medico)**

```dax
60 / [Tempo Visita Value]
```

**Carico**

```dax
DIVIDE([Lambda (pz/ora)], [Mu (pz/ora per medico)])
```

**Rho**

```dax
DIVIDE([Carico], [Medici scenario])
```

**P attesa**

```dax
VAR c = [Medici scenario]  VAR a = [Carico]
  VAR p = POISSON.DIST(c, a, FALSE) * c / (c - a)
  RETURN IF(NOT ISBLANK([Rho]) && [Rho] < 1,
      DIVIDE(p, POISSON.DIST(c - 1, a, TRUE) + p))
```

**Wq modello (min)**

```dax
IF(NOT ISBLANK([Rho]) && [Rho] < 1,
    DIVIDE([P attesa],
      [Medici scenario] * [Mu (pz/ora per medico)] - [Lambda (pz/ora)]) * 60)
```

**Medici minimi**

```dax
VAR lam = [Lambda (pz/ora)]
VAR mu  = [Mu (pz/ora per medico)]
VAR a   = DIVIDE(lam, mu)
VAR ok  = FILTER(GENERATESERIES(1, 10, 1),
  VAR c = [Value]
  VAR p = POISSON.DIST(c, a, FALSE) * c / (c - a)
  RETURN c > a &&
    DIVIDE(DIVIDE(p, POISSON.DIST(c - 1, a, TRUE) + p), c * mu - lam) * 60
      <= [Soglia attesa Value])
RETURN MINX(ok, [Value])
```

**Quota CdC compatibili**

```dax
SELECTEDVALUE('Scenario CdC'[Quota compatibili], 0.5)
```

**Quota CdC non classificabili**

```dax
SELECTEDVALUE('Scenario CdC'[Quota non classificabili], 0)
```

**Scenario CdC attivo**

```dax
SELECTEDVALUE('Scenario CdC'[Scenario], "2 · Base (50% dei compatibili)")
```

**Accessi deviati alle CdC**

```dax
COALESCE ( [Quota CdC compatibili] * [Accessi compatibili CdC], 0 )
    + COALESCE ( [Quota CdC non classificabili] * [Accessi non classificabili CdC], 0 )
```

**Accessi dopo CdC**

```dax
[Accessi] - [Accessi deviati alle CdC]
```

**Riduzione accessi PS %**

```dax
DIVIDE([Accessi deviati alle CdC], [Accessi])
```

**Lambda dopo CdC (pz/ora)**

```dax
DIVIDE([Accessi dopo CdC], [Giorni periodo] * [Ore turno])
```

**Rho dopo CdC**

```dax
DIVIDE(DIVIDE([Lambda dopo CdC (pz/ora)], [Mu (pz/ora per medico)]), [Medici scenario])
```

**Wq dopo CdC (min)**

```dax
VAR c = [Medici scenario]
VAR lam = [Lambda dopo CdC (pz/ora)]
VAR mu = [Mu (pz/ora per medico)]
VAR a = DIVIDE(lam, mu)
VAR p = DIVIDE(POISSON.DIST(c, a, FALSE) * c, c - a)
RETURN
    IF(NOT ISBLANK(c) && NOT ISBLANK(lam) && a < c,
        DIVIDE(DIVIDE(p, POISSON.DIST(c - 1, a, TRUE) + p), c * mu - lam) * 60)
```

**Stato turno prima**

```dax
VAR rho = [Rho]
VAR w = [Wq modello (min)]
RETURN IF(ISBLANK(rho), BLANK(), IF(rho >= 1, "Instabile", IF(w > [Soglia Attesa Value], "Critico", "Ok")))
```

**Stato turno dopo CdC**

```dax
VAR rho = [Rho dopo CdC]
VAR w = [Wq dopo CdC (min)]
RETURN IF(ISBLANK(rho), BLANK(), IF(rho >= 1, "Instabile", IF(w > [Soglia Attesa Value], "Critico", "Ok")))
```

**Medici minimi dopo CdC**

```dax
VAR lam = [Lambda dopo CdC (pz/ora)]
VAR mu = [Mu (pz/ora per medico)]
VAR a = DIVIDE(lam, mu)
VAR soglia = [Soglia Attesa Value]
VAR ok =
    FILTER(GENERATESERIES(1, 10, 1),
        VAR c = [Value]
        VAR p = DIVIDE(POISSON.DIST(c, a, FALSE) * c, c - a)
        RETURN c > a && DIVIDE(DIVIDE(p, POISSON.DIST(c - 1, a, TRUE) + p), c * mu - lam) * 60 <= soglia)
RETURN IF(NOT ISBLANK(lam), MINX(ok, [Value]))
```

**Medici liberati dalle CdC**

```dax
IF(NOT ISBLANK([Medici minimi]) && NOT ISBLANK([Medici minimi dopo CdC]), [Medici minimi] - [Medici minimi dopo CdC])
```

**Medici mancanti prima**

```dax
IF(NOT ISBLANK([Medici minimi]), MAX(0, [Medici minimi] - [Medici scenario]))
```

**Medici mancanti dopo CdC**

```dax
IF(NOT ISBLANK([Medici minimi dopo CdC]), MAX(0, [Medici minimi dopo CdC] - [Medici scenario]))
```

**Turni PS-turno (n)**

```dax
COUNTROWS(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]))
```

**Turni critici prima**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), IF([Stato turno prima] IN {"Instabile", "Critico"}, 1, 0))
```

**Turni critici dopo CdC**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), IF([Stato turno dopo CdC] IN {"Instabile", "Critico"}, 1, 0))
```

**Turni instabili prima**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), IF([Stato turno prima] = "Instabile", 1, 0))
```

**Turni instabili dopo CdC**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), IF([Stato turno dopo CdC] = "Instabile", 1, 0))
```

**Medici-turno in organico**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), [Medici scenario])
```

**Medici-turno minimi prima**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), [Medici minimi])
```

**Medici-turno minimi dopo CdC**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), [Medici minimi dopo CdC])
```

**Medici-turno mancanti prima**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), [Medici mancanti prima])
```

**Medici-turno mancanti dopo CdC**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), [Medici mancanti dopo CdC])
```

**Ore-medico liberate a settimana**

```dax
SUMX(VALUES(Fact_PS_2022[FK_PS_Turno_Accettazione]), [Medici liberati dalle CdC] * [Ore turno]) * 7
```

**Medici Aggiuntivi Value**

```dax
SELECTEDVALUE('Medici Aggiuntivi'[Medici Aggiuntivi], 0)
```

**Soglia Attesa Value**

```dax
SELECTEDVALUE('Soglia Attesa'[Soglia Attesa], 15)
```

**Tempo Visita Value**

```dax
SELECTEDVALUE('Tempo Visita'[Tempo Visita], 20)
```

</details>

## H. Rete CdC (SP3)

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `SP3 N CdC` | Numero di CdC della rete. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0` | Confronto, Rete CdC · card KPI di Rete |
| `SP3 N hub` | CdC hub (bacino >= 40.000 ab., aperte h24 7/7). Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0` | Confronto, Rete CdC |
| `SP3 Gestita` | Visite all'anno gestite dalle CdC (presa in carico entro la capacità). Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `#,0` | Confronto, Rete CdC · card KPI di Rete |
| `SP3 Presa in carico` | Accessi compatibili all'anno in orario di apertura × quota presa in carico. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `#,0` | non usata |
| `SP3 Capacita` | Visite all'anno possibili: ore × medici × 3 visite/ora × 85%. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `#,0` | Confronto |
| `SP3 Riduzione accessi PS` | Visite gestite / accessi PS annui. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0.0%` | Confronto, Rete CdC · card KPI di Rete |
| `SP3 Km medi` | Distanza stradale stimata, media pesata per la domanda. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0.00` | Confronto, Rete CdC · card KPI di Rete |
| `SP3 Minuti medi` | Tempo medio di viaggio a 45 km/h. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0.0` | non usata |
| `SP3 Domanda entro 10 km` | Quota della domanda a meno di 10 km dalla sua CdC. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0.0%` | Confronto, Rete CdC · card KPI di Rete |
| `SP3 Km max` | Distanza del comune più lontano dalla sua CdC. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `0.0` | non usata |
| `SP3 Costo annuo` | Medici a ore + infermieri e amministrativi + sede. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `#,0 €` | Confronto, Rete CdC · card KPI di Rete |
| `SP3 Costo per visita` | Costo annuo / visite gestite. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `#,0 €` | Confronto, Rete CdC |
| `SP3 Valore PS non erogato` | Tariffa PS delle visite gestite: valorizzazione tariffaria, non risparmio certo. Calcolata dal notebook SP3 per la rete filtrata in SP3_Rete (se nessuna: Proposta), quota 50%. | `#,0 €` | Confronto |
| `SP3 Domanda compatibile rete` | Accessi compatibili (misura unica [Accessi compatibili CdC], gen-giu 2022) dei comuni assegnati alla rete o alla CdC filtrata, tramite la tabella SP3_Assegnazione. | `#,0` | indiretta (via SP3 Domanda annua) |
| `SP3 Domanda annua` | [SP3 Domanda compatibile rete] portata a un anno (× 365/181: i dati coprono 181 giorni). | `#,0` | Confronto |
| `SP3 Valore compatibili rete` | Valorizzazione tariffaria degli accessi compatibili dei comuni della rete (gen-giu 2022). | `#,0 €` | non usata |
| `SP3 Quota domanda` | Quota della domanda della rete per fascia di distanza o per CdC. | `0.0%` | + 1 sottopagina |
| `SP3 Comuni` | Numero di comuni del territorio. | `0` | non usata |

<details><summary>Formule DAX · H. Rete CdC (SP3)</summary>

**SP3 N CdC**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[N CdC] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 N hub**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[N hub] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Gestita**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Gestita] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Presa in carico**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Presa in carico] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Capacita**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Capacita] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Riduzione accessi PS**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Riduzione accessi PS] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Km medi**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Km medi] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Minuti medi**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Minuti medi] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Domanda entro 10 km**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Domanda entro 10 km] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Km max**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Km max] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Costo annuo**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Costo annuo] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Costo per visita**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Costo per visita] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Valore PS non erogato**

```dax
VAR r = SELECTEDVALUE ( SP3_Rete[Scenario], "Proposta" )
RETURN
    CALCULATE ( SUM ( SP3_Scenari[Valore PS non erogato] ), SP3_Scenari[Tipo] = "Base", SP3_Rete[Scenario] = r )
```

**SP3 Domanda compatibile rete**

```dax
CALCULATE ( [Accessi compatibili CdC], TREATAS ( VALUES ( SP3_Assegnazione[Codice_ISTAT] ), Dim_Comuni_Residenze[PK_Codice_Comune] ) )
```

**SP3 Domanda annua**

```dax
[SP3 Domanda compatibile rete] * 365 / 181
```

**SP3 Valore compatibili rete**

```dax
CALCULATE ( [Valore economico compatibili CdC], TREATAS ( VALUES ( SP3_Assegnazione[Codice_ISTAT] ), Dim_Comuni_Residenze[PK_Codice_Comune] ) )
```

**SP3 Quota domanda**

```dax
DIVIDE ( [SP3 Domanda annua], CALCULATE ( [SP3 Domanda annua], REMOVEFILTERS ( SP3_Assegnazione[Fascia km], SP3_Assegnazione[Fascia ordine], SP3_Assegnazione[CdC], SP3_Assegnazione[Comune] ) ) )
```

**SP3 Comuni**

```dax
DISTINCTCOUNT ( SP3_Assegnazione[Comune] )
```

</details>

## I. Confronto con la Direzione Generale (SP4)

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `SP4 Scostamento N CdC (Proposta - DG)` | Scostamento Proposta meno Direzione Generale (traccia SP4, punto D): numero di CdC. | `+0;-0;0` | Confronto · card KPI di Confronto |
| `SP4 Scostamento Gestita (Proposta - DG)` | Scostamento Proposta meno Direzione Generale (traccia SP4, punto D): visite gestite all'anno. | `+#,0;-#,0;0` | Confronto · card KPI di Confronto |
| `SP4 Scostamento Riduzione accessi PS (Proposta - DG)` | Scostamento Proposta meno Direzione Generale (traccia SP4, punto D): riduzione accessi PS. | `+0.0%;-0.0%;0.0%` | Confronto · card KPI di Confronto |
| `SP4 Scostamento Km medi (Proposta - DG)` | Scostamento Proposta meno Direzione Generale (traccia SP4, punto D): km medi. | `+0.00;-0.00;0.00` | Confronto · card KPI di Confronto |
| `SP4 Scostamento Domanda entro 10 km (Proposta - DG)` | Scostamento Proposta meno Direzione Generale (traccia SP4, punto D): quota di domanda entro 10 km. | `+0.0%;-0.0%;0.0%` | Confronto · card KPI di Confronto |
| `SP4 Scostamento Costo per visita (Proposta - DG)` | Scostamento Proposta meno Direzione Generale (traccia SP4, punto D): costo per visita gestita. | `+#,0 €;-#,0 €;0 €` | Confronto |
| `SP4 Scostamento Costo annuo (Proposta - DG)` | Scostamento Proposta meno Direzione Generale: costo annuo in milioni di euro. | `+0.00 M€;-0.00 M€;0 M€` | Confronto · card KPI di Confronto |

<details><summary>Formule DAX · I. Confronto con la Direzione Generale (SP4)</summary>

**SP4 Scostamento N CdC (Proposta - DG)**

```dax
CALCULATE ( [SP3 N CdC], SP3_Rete[Scenario] = "Proposta" )
    - CALCULATE ( [SP3 N CdC], SP3_Rete[Scenario] = "Direzione Generale" )
```

**SP4 Scostamento Gestita (Proposta - DG)**

```dax
CALCULATE ( [SP3 Gestita], SP3_Rete[Scenario] = "Proposta" )
    - CALCULATE ( [SP3 Gestita], SP3_Rete[Scenario] = "Direzione Generale" )
```

**SP4 Scostamento Riduzione accessi PS (Proposta - DG)**

```dax
CALCULATE ( [SP3 Riduzione accessi PS], SP3_Rete[Scenario] = "Proposta" )
    - CALCULATE ( [SP3 Riduzione accessi PS], SP3_Rete[Scenario] = "Direzione Generale" )
```

**SP4 Scostamento Km medi (Proposta - DG)**

```dax
CALCULATE ( [SP3 Km medi], SP3_Rete[Scenario] = "Proposta" )
    - CALCULATE ( [SP3 Km medi], SP3_Rete[Scenario] = "Direzione Generale" )
```

**SP4 Scostamento Domanda entro 10 km (Proposta - DG)**

```dax
CALCULATE ( [SP3 Domanda entro 10 km], SP3_Rete[Scenario] = "Proposta" )
    - CALCULATE ( [SP3 Domanda entro 10 km], SP3_Rete[Scenario] = "Direzione Generale" )
```

**SP4 Scostamento Costo per visita (Proposta - DG)**

```dax
CALCULATE ( [SP3 Costo per visita], SP3_Rete[Scenario] = "Proposta" )
    - CALCULATE ( [SP3 Costo per visita], SP3_Rete[Scenario] = "Direzione Generale" )
```

**SP4 Scostamento Costo annuo (Proposta - DG)**

```dax
DIVIDE (
    CALCULATE ( [SP3 Costo annuo], SP3_Rete[Scenario] = "Proposta" )
        - CALCULATE ( [SP3 Costo annuo], SP3_Rete[Scenario] = "Direzione Generale" ),
    1e6
)
```

</details>

## L. Controlli per la pagina Leggimi

| Misura | Cosa misura | Formato | Dove si vede |
|---|---|---|---|
| `Controllo accessi totali` | Numeri di controllo (ignorano tutti i filtri) per la pagina Leggimi. | `#,0` | indiretta (via Controllo accessi totali testo) |
| `Controllo pazienti distinti` |  | `#,0` | indiretta (via Controllo pazienti distinti testo) |
| `Controllo valore totale €` |  | `#,0.00 €` | indiretta (via Controllo valore totale testo) |
| `Controllo accessi senza dimissione` |  | `#,0` | indiretta (via Controllo accessi senza dimissione testo) |
| `Controllo codici bianchi` |  | `#,0` | indiretta (via Controllo codici bianchi testo) |
| `Controllo accessi totali testo` | Come «Controllo accessi totali», scritto con il formato italiano (punto per le migliaia), per la pagina Leggimi. | – | Leggimi |
| `Controllo pazienti distinti testo` | Come «Controllo pazienti distinti», in formato italiano. | – | Leggimi |
| `Controllo valore totale testo` | Come «Controllo valore totale €», in formato italiano con i centesimi. | – | Leggimi |
| `Controllo accessi senza dimissione testo` | Come «Controllo accessi senza dimissione», in formato italiano. | – | Leggimi |
| `Controllo codici bianchi testo` | Come «Controllo codici bianchi», in formato italiano. | – | Leggimi |

<details><summary>Formule DAX · L. Controlli per la pagina Leggimi</summary>

**Controllo accessi totali**

```dax
CALCULATE ( [Accessi], REMOVEFILTERS () )
```

**Controllo pazienti distinti**

```dax
CALCULATE ( [Pazienti], REMOVEFILTERS () )
```

**Controllo valore totale €**

```dax
CALCULATE ( [Valore €], REMOVEFILTERS () )
```

**Controllo accessi senza dimissione**

```dax
CALCULATE ( [Accessi senza dimissione], REMOVEFILTERS () )
```

**Controllo codici bianchi**

```dax
CALCULATE ( [Accessi codice bianco], REMOVEFILTERS () )
```

**Controllo accessi totali testo**

```dax
FORMAT ( [Controllo accessi totali], "#,0", "it-IT" )
```

**Controllo pazienti distinti testo**

```dax
FORMAT ( [Controllo pazienti distinti], "#,0", "it-IT" )
```

**Controllo valore totale testo**

```dax
FORMAT ( [Controllo valore totale €], "#,0.00", "it-IT" ) & " €"
```

**Controllo accessi senza dimissione testo**

```dax
FORMAT ( [Controllo accessi senza dimissione], "#,0", "it-IT" )
```

**Controllo codici bianchi testo**

```dax
FORMAT ( [Controllo codici bianchi], "#,0", "it-IT" )
```

</details>

## M. Misure di presentazione (non calcolano numeri di business)

Servono solo a disegnare il report: card KPI in SVG (numero, freccia di variazione, linea mensile), colori condizionali, testi dei sottotitoli e tooltip della mappa. Ogni card KPI usa una misura di calcolo (colonna «Misura sorgente» nella descrizione dentro il modello): il numero mostrato è sempre quello della misura di calcolo.

| Cartella nel modello | N. misure | Esempi |
|---|---:|---|
| (senza cartella) | 8 | Lettura accessi, Lettura scenario CdC, Lettura medici mancanti … |
| 7 KPI Direzionale | 13 | KPI sub accessi, KPI sub accessi vs media, Lettura valore … |
| SP4 Confronto | 1 | SP4 Lettura confronto |
| Grafica KPI\Direzionale | 18 | KPI Direzionale accessi valore, KPI Direzionale accessi linea, KPI Direzionale accessi freccia … |
| Grafica KPI\Attese | 12 | KPI Attese attesa90 valore, KPI Attese attesa90 linea, KPI Attese attesa90 freccia … |
| Grafica KPI\Territorio | 12 | KPI Territorio comuni valore, KPI Territorio comuni linea, KPI Territorio comuni freccia … |
| Grafica KPI\Domanda | 10 | KPI Domanda val_cdc valore, KPI Domanda val_cdc linea, KPI Domanda val_cdc freccia … |
| Grafica KPI\Rete CdC | 6 | KPI Rete CdC n_cdc valore, KPI Rete CdC gestita valore, KPI Rete CdC riduzione valore … |
| Grafica KPI\Confronto | 12 | KPI Confronto n_cdc valore, KPI Confronto n_cdc freccia, KPI Confronto km valore … |
| Grafica KPI | 5 | KPI stile colore, KPI stile su, KPI stile giu … |
| Grafica KPI\Flussi | 18 | KPI Flussi acc_giorno valore, KPI Flussi acc_giorno linea, KPI Flussi acc_giorno freccia … |
| 9 Grafica | 1 | Colore race comune |
| 9 Grafica\Tooltip mappa | 6 | Tooltip comune sottotitolo, Tooltip confronto tasso, Tooltip compatibili CdC … |
| 9 Grafica\Evidenze | 4 | Colore evidenza mese, Colore evidenza giorno, Colore comune sede PS … |
| 9 Grafica\GitHub | 10 | GitHub indirizzo base, GitHub link fonti, GitHub link anomalie … |

<details><summary>Elenco completo delle misure di presentazione</summary>

**(senza cartella)**

- `Lettura accessi`
- `Lettura scenario CdC`
- `Lettura medici mancanti`
- `KPI card attesa mediana`
- `KPI card accessi`
- `KPI card codici bianchi`
- `KPI card permanenza P90`
- `KPI card valore`

**7 KPI Direzionale**

- `KPI sub accessi`
- `KPI sub accessi vs media`
- `Lettura valore`
- `KPI sub valore`
- `Lettura attesa mediana`
- `KPI sub attesa mediana`
- `Lettura permanenza P90`
- `KPI sub permanenza P90`
- `Lettura codici bianchi`
- `KPI sub codici bianchi`
- `Colore KPI attesa mediana`
- `Colore KPI permanenza P90`
- `Colore KPI codici bianchi`

**SP4 Confronto**

- `SP4 Lettura confronto`

**Grafica KPI\Direzionale**

- `KPI Direzionale accessi valore`
- `KPI Direzionale accessi linea`
- `KPI Direzionale accessi freccia`
- `KPI Direzionale bianchi valore`
- `KPI Direzionale bianchi linea`
- `KPI Direzionale bianchi freccia`
- `KPI Direzionale attesa valore`
- `KPI Direzionale attesa linea`
- `KPI Direzionale attesa freccia`
- `KPI Direzionale perm90 valore`
- `KPI Direzionale perm90 linea`
- `KPI Direzionale perm90 freccia`
- `KPI Direzionale valore valore`
- `KPI Direzionale valore linea`
- `KPI Direzionale valore freccia`
- `KPI Direzionale pacc_cdc valore`
- `KPI Direzionale pacc_cdc linea`
- `KPI Direzionale pacc_cdc freccia`

**Grafica KPI\Attese**

- `KPI Attese attesa90 valore`
- `KPI Attese attesa90 linea`
- `KPI Attese attesa90 freccia`
- `KPI Attese perm valore`
- `KPI Attese perm linea`
- `KPI Attese perm freccia`
- `KPI Attese attesa_vb valore`
- `KPI Attese attesa_vb linea`
- `KPI Attese attesa_vb freccia`
- `KPI Attese perm_vb valore`
- `KPI Attese perm_vb linea`
- `KPI Attese perm_vb freccia`

**Grafica KPI\Territorio**

- `KPI Territorio comuni valore`
- `KPI Territorio comuni linea`
- `KPI Territorio comuni freccia`
- `KPI Territorio top10 valore`
- `KPI Territorio top10 linea`
- `KPI Territorio top10 freccia`
- `KPI Territorio per1000 valore`
- `KPI Territorio per1000 linea`
- `KPI Territorio per1000 freccia`
- `KPI Territorio fuori valore`
- `KPI Territorio fuori linea`
- `KPI Territorio fuori freccia`

**Grafica KPI\Domanda**

- `KPI Domanda val_cdc valore`
- `KPI Domanda val_cdc linea`
- `KPI Domanda val_cdc freccia`
- `KPI Domanda pval_cdc valore`
- `KPI Domanda pval_cdc linea`
- `KPI Domanda pval_cdc freccia`
- `KPI Domanda acc_cdc valore`
- `KPI Domanda acc_cdc linea`
- `KPI Domanda acc_cdc freccia`
- `KPI Domanda quota valore`

**Grafica KPI\Rete CdC**

- `KPI Rete CdC n_cdc valore`
- `KPI Rete CdC gestita valore`
- `KPI Rete CdC riduzione valore`
- `KPI Rete CdC km valore`
- `KPI Rete CdC entro10 valore`
- `KPI Rete CdC costo valore`

**Grafica KPI\Confronto**

- `KPI Confronto n_cdc valore`
- `KPI Confronto n_cdc freccia`
- `KPI Confronto km valore`
- `KPI Confronto km freccia`
- `KPI Confronto entro10 valore`
- `KPI Confronto entro10 freccia`
- `KPI Confronto gestita valore`
- `KPI Confronto gestita freccia`
- `KPI Confronto riduzione valore`
- `KPI Confronto riduzione freccia`
- `KPI Confronto costo valore`
- `KPI Confronto costo freccia`

**Grafica KPI**

- `KPI stile colore`
- `KPI stile su`
- `KPI stile giu`
- `KPI stile glow`
- `KPI stile alone`

**Grafica KPI\Flussi**

- `KPI Flussi acc_giorno valore`
- `KPI Flussi acc_giorno linea`
- `KPI Flussi acc_giorno freccia`
- `KPI Flussi acc_paz valore`
- `KPI Flussi acc_paz linea`
- `KPI Flussi acc_paz freccia`
- `KPI Flussi autonomi valore`
- `KPI Flussi autonomi linea`
- `KPI Flussi autonomi freccia`
- `KPI Flussi prest_acc valore`
- `KPI Flussi prest_acc linea`
- `KPI Flussi prest_acc freccia`
- `KPI Flussi val_medio valore`
- `KPI Flussi val_medio linea`
- `KPI Flussi val_medio freccia`
- `KPI Flussi ticket valore`
- `KPI Flussi ticket linea`
- `KPI Flussi ticket freccia`

**9 Grafica**

- `Colore race comune`

**9 Grafica\Tooltip mappa**

- `Tooltip comune sottotitolo`
- `Tooltip confronto tasso`
- `Tooltip compatibili CdC`
- `Tooltip comune titolo`
- `Tooltip valore`
- `Tooltip barre mesi`

**9 Grafica\Evidenze**

- `Colore evidenza mese`
- `Colore evidenza giorno`
- `Colore comune sede PS`
- `Colore diagnosi top 2`

**9 Grafica\GitHub**

- `GitHub indirizzo base`
- `GitHub link fonti`
- `GitHub link anomalie`
- `GitHub link metodo`
- `GitHub link KPI`
- `GitHub link misure`
- `GitHub link controlli`
- `GitHub link imbuto`
- `GitHub link code`
- `GitHub link rete`

</details>

## Misure non usate

Misure di calcolo che, leggendo i file del report e del modello, non compaiono in nessun visual e non sono richiamate da altre misure. Sono rimaste da prove precedenti. Prima di cancellarle apri il report e controlla con «Visualizza dipendenze» di Power BI.

- `Paziente top`
- `Max accessi per paziente`
- `% V+B`
- `Valore € V+B`
- `Fascia di picco`
- `Durata mediana (min)`
- `Pazienti in coda (media)`
- `Pazienti presenti (P90)`
- `Tempo medio permanenza (min)`
- `Presenti (media)`
- `Accessi (media per ora)`
- `Personale (media)`
- `Turni instabili prima`
- `Turni instabili dopo CdC`
- `Medici-turno in organico`
- `Medici-turno minimi prima`
- `Medici-turno minimi dopo CdC`
- `Ore-medico liberate a settimana`
- `SP3 Presa in carico`
- `SP3 Minuti medi`
- `SP3 Km max`
- `SP3 Valore compatibili rete`
- `SP3 Comuni`


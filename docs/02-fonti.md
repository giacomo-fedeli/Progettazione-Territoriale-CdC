# 02 – Fonti

Questo documento dice **da dove arriva ogni dato, ogni regola e ogni parametro** del progetto.
Le fonti sono in quattro gruppi: (1) dati forniti, (2) tabelle preparate dal team, (3) dati territoriali, (4) fonti normative, scientifiche e istituzionali.
Alla fine c'è la tabella di ogni parametro dell'SP3 con la sua fonte, oppure con la scritta **IPOTESI**.

> **Regola:** ogni numero del report si deve poter ritrovare così: *file → tabella del modello → colonna → misura*.
> La tabella al punto 2 è la prima parte di questo percorso. La seconda parte è nel [catalogo delle misure](04b-catalogo-misure.md).

---

## 1. Dati e materiali forniti dai docenti

| Materiale | Contenuto | Dove sta nel repository | Usato per |
|---|---|---|---|
| `01_DB_Excel_PS_2022.xlsx` | Flusso dei Pronto Soccorso: 75.664 accessi, 25 colonne, foglio `PS_2022`. Dal 01/01/2022 al 30/06/2022, 7 PS dell'ASST dei Sette Laghi, 58.320 pazienti | `dati/sorgenti/` | Tabella dei fatti |
| `03_Codifiche_Diagnosi_e_Problema_principale.xlsx` | Codebook ICD-9-CM: foglio `Diagnosi` (16.228 codici) e foglio `Problema principale` | `dati/sorgenti/` | Dimensioni diagnosi e problema principale |
| `codifiche flusso.pdf` | Data dictionary del flusso (campi e codici) | non caricato (materiale del corso) | Decodifiche: triage, arrivo, esito, regime, ticket, reparti, cittadinanza |
| Tabella del personale per turno | Medici / infermieri / OSS presenti per PS e turno M/P/N (nel testo della traccia, p. 3). In Excel: 21 righe = 7 PS × 3 turni | `dati/dimensioni/dim_turni.xlsx` (versione base). Il modello usa `Personale_PS_Turno.xlsx`, che aggiunge `Totale_Personale` e gli orari dei turni | Tabelle `Dim_Turni_*` e studio delle code |
| `case della comunità e domanda potenziale.pdf` | Funzioni delle CdC e criteri di esclusione degli accessi | non caricato | Criteri della domanda potenziale ([06](06-domanda-potenziale-cdc.md)) |
| `sottoprova 4_configurazione CdC direzione.pdf` | 10 comuni (con indirizzo) scelti dalla Direzione Generale | non caricato | Rete DG ([07](07-rete-cdc-e-confronto.md)) |
| `04_Queuing_Model_1/2/3.pdf` e dispensa sulla teoria delle code | Teoria delle code per i Pronto Soccorso | non caricati | Studio delle code (facoltativo) |
| Traccia `ITS_DATA_ANALYST_E2 - PW4.pdf` | Richieste di ogni sottoprova | non caricata | Tutto |

> I PDF e i materiali dei docenti non si caricano su GitHub (diritti): si citano in [`../riferimenti/bibliografia.md`](../riferimenti/bibliografia.md).

---

## 2. Dal file al modello: tabella per tabella

Il modello Power BI (`PW4 15`) ha:
- **27 tabelle caricate da Excel**: la fact e 26 dimensioni;
- **6 tabelle SP3/SP4**: 5 caricate da Excel (output del notebook) e 1 creata in Power Query;
- **9 tabelle calcolate in DAX**;
- la tabella `_Misure` (solo misure) e un parametro Power Query (`Cartella_SP3`).

Sotto, per ogni tabella: file di origine, foglio, trasformazioni in Power Query.

### 2.1 Tabella dei fatti

| Tabella del modello | File | Foglio | Trasformazioni principali |
|---|---|---|---|
| `Fact_PS_2022` | `fatti_ridotta.xlsx` | `Sheet1` | Preparata dal team dal DB originale. In Power Query: tipi dei campi, ordinamento per `data_ora_accettazione`, indice `PK_ID_Episodio` (1…75.664), colonne data-ora (`data_ora_prcar` = data + ora), durate, ora intera, chiavi dei turni, colonna `Compatibile_CdC_Durata_Prestazione`. Dettaglio in [05](05-modello-dati.md) |

*Come nasce `fatti_ridotta.xlsx`:* è il DB originale senza le colonne `sesso` e `anno_nascita` (spostate in `pazienti.xlsx`), con in più le colonne `Ticket_pagato`, `data_ora_accettazione`, `data_ora_dimissione` e `durata_pronto_soccorso`. Il numero di righe è uguale (75.664). Il file `Fact_Finale_PowerBI.xlsx` è un'esportazione della fact finale dal modello (40 colonne, comprese le colonne di compatibilità CdC): serve al notebook SP3.

### 2.2 Dimensioni caricate da Excel

| Tabella del modello | File di origine | Foglio | Righe | Note |
|---|---|---|---:|---|
| `DIm_Pazienti` | `pazienti.xlsx` | `Sheet1` | 58.320 | Un paziente = una riga; sesso = ultimo registrato; `sesso_descrizione` creata in Power Query (1 = Maschio, 2 = Femmina) |
| `Dim_Pronto_Soccorso` | `dim_struttura_ricovero.xlsx` | `dim_struttura_ricovero` | 7 | Denominazione, comune, coordinate; colonne `… corretta` in DAX |
| `Dim_Comuni_Residenze` | `code_to_residenza_geo_pop.xlsx` | `Sheet1` | 1.379 | Codice ISTAT a 6 cifre come **testo**; popolazione ISTAT 2022; tenuti solo i codici presenti nella fact (join interno) |
| `Dim_Paesi_Cittadinanze` | `codici_cittadinanza_paesi.xlsx` | `codici_cittadinanza_paesi` | 129 | Codici ANPR |
| `DIm_Diagnosi_Primaria`, `DIm_Diagnosi_Secondaria` | `03_Codifiche_Diagnosi_e_Problema_principale (1).xlsx` | `Diagnosi` | 16.228 | Stessa tabella caricata due volte (primaria e secondaria). La colonna `Compatibile_CdC` è il primo criterio della classificazione CdC |
| `Dim_Calendario_Accettazione`, `…_Prcar`, `…_Dimissione` | `Dim_Calendario_Fasce_v3 1.xlsx` | `cal corr` | 212 | Tre copie dello stesso calendario (una per ogni data della fact). `In_periodo_dati` = TRUE per i 181 giorni con dati |
| `DIm_Fasce_Orarie_Accetazionee`, `…_Prcar`, `…_Dimissione` | `lookup_codifiche_PS_2022_v2 (1).xlsx` | `fasce_orarie` | 24 | Ora 0–23 con turno M/P/N (7–14, 14–21, 21–7) |
| `Dim_Fasce_Eta` | idem | `fasce_eta` | 111 | Una riga per età 0–110 |
| `Dim_Mod_Arrivo` | idem | `mod_arr` | 8 | Con `Gruppo_arrivo` (Autonomo / Mezzo di soccorso / Non rilevato) |
| `Dim_Problema_Principale` | idem | `problemaprincipale` | 31 | |
| `Dim_Regime_Erogazione` | idem | `reg_erog` | 4 | |
| `Dim_Reparti` | idem | `Codice reparto modificato` | 72 | |
| `Dim_Responsabile_Invio` | idem | `resp_inv` | 9 | |
| `Dim_Ticket` | idem | `tck` | 2 | 0 = nessun ticket; 2500 = ticket da 25 € |
| `Dim_Triage_Ingresso`, `Dim_Triage_Uscita` | idem | `triage` | 6 | Foglio caricato due volte: triage in ingresso e in uscita. Con colonna `Compatibile_CdC` |
| `Dim_Esito_Trattamento` | idem | `esito_tratt` | 10 | Con `Gruppo_esito` e `Compatibile_CdC` |
| `Dim_Turni_Accettazione`, `…_Prcar`, `…_Dimissione` | `Personale_PS_Turno.xlsx` | `Personale_PS_Turno` | 21 | 7 PS × 3 turni; medici, infermieri, OSS presenti |

### 2.3 Tabelle dell'SP3/SP4 (dal notebook)

Il parametro Power Query `Cartella_SP3` punta alla cartella `SP3_rete_CdC/output/`. Il file `SP3_rete_CdC_PowerBI.xlsx` è prodotto dal notebook (vedi [07](07-rete-cdc-e-confronto.md)).

| Tabella | Foglio di `SP3_rete_CdC_PowerBI.xlsx` | Righe | Contenuto |
|---|---|---:|---|
| `SP3_Assegnazione` | `Assegnazione_CdC` | 230 | Per ogni codice ISTAT e rete: CdC, km, minuti, fascia di distanza, coordinate |
| `SP3_CdC` | `Dim_CdC` | 16 | Una riga per sede e rete: tipo, orario, domanda, personale, capacità, costo |
| `SP3_Scenari` | `Scenari` | 13 | Indicatori per rete × quota (30/50/70%) + sensibilità |
| `SP3_Frontiera` | `Frontiera` | 6 | Rete migliore per numero di CdC (da 5 a 10) |
| `SP3_Parametri` | `Parametri` | 26 | Tutte le ipotesi del notebook |
| `SP3_Rete` | (creata in Power Query) | 2 | Proposta (SP3) e Direzione Generale (SP4): filtra le altre |

### 2.4 Tabelle calcolate nel modello (DAX)

| Tabella | Cosa è |
|---|---|
| `FNL_Fasi` | Le 8 fasi del funnel «da 75.664 a 20.419» |
| `Scenario CdC` | 6 scenari di quota presa in carico (0/30/50/70/100% e «70% + 30% dei non classificabili») |
| `Quota CdC passi` | I 3 passi che giustificano la quota base del 50% |
| `Medici Aggiuntivi`, `Soglia Attesa`, `Tempo Visita` | Parametri «what-if» dello studio delle code (valori 0–3, 5–60, 10–40) |
| `Ore_presenza` | Griglia giorno × ora (4.344 righe = 181 giorni × 24) |
| `Tab_Presenti_Ora` | Pazienti presenti per giorno della settimana e ora (168 righe) |
| `Tab_Presenti_Ora_Istituto` | Stesso calcolo per PS (1.176 righe), con pazienti in coda e personale |

---

## 3. Dati territoriali

| Fonte | Cosa | Usata per |
|---|---|---|
| ISTAT – popolazione residente per comune al 01/01/2022 (file POSAS 2022) | Abitanti di ogni comune | `Popolazione_2022` → accessi ogni 1.000 abitanti; peso dei comuni nel territorio SP3 |
| ISTAT – elenco dei comuni (codici a 6 cifre) | Codice del comune di residenza | Collegamento fact → comuni. Nel DB il campo `residenza` contiene il **codice ISTAT del comune**, non il CAP come scrive il PDF |
| ISTAT – confini dei comuni al 01/01/2026 (generalizzati) | Poligoni dei comuni | Centro (centroide) di ogni comune e mappe dei bacini. Scaricati da [istat.it](https://www.istat.it/classificazione/confini-delle-unita-amministrative-a-fini-statistici/) |
| `dim_struttura_ricovero.xlsx` | Indirizzo e coordinate dei 7 PS | Punti dei PS sulle mappe |

---

## 4. Fonti normative, scientifiche e istituzionali

### 4.1 Per i criteri della domanda potenziale (SP2) e per la rete (SP3)

| Fonte | Cosa ci abbiamo preso |
|---|---|
| **DM 23 maggio 2022 n. 77**, Allegato 1 – [Gazzetta Ufficiale](https://www.gazzettaufficiale.it/eli/id/2022/06/22/22G00085/sg) | Modello hub e spoke: hub ogni 40–50 mila abitanti, aperte h24 7 giorni su 7; spoke aperte h12 6 giorni su 7 |
| **AGENAS** – Linee di indirizzo per l'attuazione del modello organizzativo delle CdC Hub (2024) | Funzioni e servizi delle CdC (citate dal documento del corso) |
| **AGENAS** – Randazzo, *Rete ospedaliera dell'emergenza e Pronto Soccorso* (2025), slide 18–19 | Indicatore di accessi potenzialmente evitabili (citato dal documento del corso) |
| Documento del corso «Case della Comunità e domanda potenziale» (par. 3) | Servizi assunti per le CdC e **criteri di esclusione**: trauma e ustione; coma, shock, sindrome neurologica acuta; dolore toracico, dispnea acuta; complicanze di gravidanza, parto, puerperio; emergenze psichiatriche, intossicazioni; procedure di emergenza, rianimazione, chirurgia urgente |
| Codici di triage | Nel PDF dei codici è definito solo il codice N (nero). I colori R, G, V, B seguono lo standard di triage e sono stati aggiunti nel file di decodifica (colonna `Fonte` = «Standard triage (non nel PDF)») |

### 4.2 Per i costi (SP3)

| Fonte | Valore usato |
|---|---|
| Intesa Stato-Regioni del 26/06/2026 sull'**ACN** della medicina generale (ore in CdC) – [QuotidianoSanità](https://www.quotidianosanita.it/uncategorized/accordo-su-medici-di-famiglia-nelle-case-della-comunita-lintesa-pubblicata-in-gu/) | **38,72 €/ora** per i medici |
| **RGS – Conto annuale 2024** (retribuzione media del comparto) – [QuotidianoSanità](https://www.quotidianosanita.it/studi-e-analisi/personale-ssn-dopo-anni-di-calo-la-sanita-torna-ad-assumere-nel-2024-i-dipendenti-sono-saliti-a-714-mila-in-aumento-di-60-mila-rispetto-al-2015/) | **33.809 €** lordi medi per infermieri e amministrativi |

### 4.3 Per il metodo di localizzazione (SP3)

- Hakimi, S. L. (1964). *Optimum locations of switching centers and the absolute centers and medians of a graph*. Operations Research, 12(3).
- ReVelle, C. S., & Swain, R. W. (1970). *Central facilities location*. Geographical Analysis, 2(1).
- Solver **HiGHS** (tramite `scipy.optimize.milp`): programmazione lineare intera esatta.

### 4.4 Per lo studio delle code (facoltativo, SP1)

1. Vass, H., & Szabo, Z. K. (2015). *Application of queuing model to patient flow in emergency department. Case study*. Procedia Economics and Finance, 32, 479–487.
2. Bittencourt, O., Verter, V., & Yalovsky, M. (2018). *Hospital capacity management based on the queueing theory*. International Journal of Productivity and Performance Management, 67(2), 224–238.
3. Wang, C. H., Tian, R., Hu, K., Chen, Y. T., & Ku, T. H. (2025). *A Markov decision optimization of medical service resources for two-class patient queues in emergency departments via particle swarm optimization algorithm*. Scientific Reports, 15(1), 2942.
4. Lezioni 1–3 sulla teoria delle code (materiale del corso).

### 4.5 Letteratura usata per controllare la quota del 50% e la quota «non urgenti»

Questi riferimenti sono usati **solo come controllo esterno** nella presentazione, non per calcolare i numeri del report.

| Fonte | Uso | Stato |
|---|---|---|
| Uscher-Pines L. et al. (2013). *Emergency department visits for nonurgent conditions: systematic literature review*. American Journal of Managed Care – [link](https://www.ajmc.com/journals/issue/2013/2013-1-vol19-n1/emergency-department-visits-for-nonurgent-conditions-systematic-literature-review?p=1) | Gli accessi non urgenti sono in media il 37%: il nostro 27% è prudente | Link annotato nella bozza della presentazione; non riaperto in questa sessione |
| Regione Emilia-Romagna – report sui CAU, 2024 | I Centri di assistenza urgenza hanno ridotto i codici verdi del 10%: giustifica lo scenario prudente al 30% | Come sopra |
| Studio ASSR sulle Case della Salute (2009–2019), riportato da [Dire (2022)](https://www.dire.it/09-06-2022/746146-il-nuovo-ruolo-del-medico-di-famiglia-il-congresso-simg-emilia-romagna/) | −16% di accessi dove ci sono le Case della Salute | **Da verificare sul dossier originale prima di citarlo**: abbiamo solo l'articolo di giornale |

---

## 5. Parametri dell'SP3: fonte o ipotesi

Tutti i parametri sono nella tabella `SP3_Parametri` del modello e nella cella 1 del notebook `SP3_rete_CdC.ipynb`.

| Parametro | Valore | Fonte | Tipo |
|---|---|---|---|
| Numero massimo di CdC | 10 | Traccia SP3 | Dato |
| Quote di presa in carico | 30%, 50%, 70% | Traccia SP2/SP4 (esempi) | Dato |
| Quota base | 50% | Giustificata dai dati: vedi [06](06-domanda-potenziale-cdc.md) | **IPOTESI** |
| Annualizzazione | × 365/181 = 2,0166 | I dati coprono 181 giorni | Calcolo |
| Hub: bacino minimo | 40.000 abitanti | DM 77/2022 | Fonte |
| Orario hub / spoke | h24 7/7 · 8–20 6/7 | DM 77/2022 | Fonte |
| Territorio: soglia | ≥ 50 accessi ogni 1.000 ab. (semestre) | Scelta del gruppo | **IPOTESI** |
| Sede solo in comuni con almeno | 5.000 abitanti | Scelta del gruppo | **IPOTESI** |
| Sede obbligata | Varese | Scelta del gruppo | **IPOTESI** |
| Distanza massima comune → CdC | 15 km | Scelta del gruppo | **IPOTESI** |
| Standard di accessibilità | 90% della domanda entro 10 km | Scelta del gruppo | **IPOTESI** |
| Distanza stradale | linea d'aria × 1,3 | Scelta del gruppo | **IPOTESI** |
| Velocità media | 45 km/h | Scelta del gruppo | **IPOTESI** |
| Visite per ora e per medico | 3 (20 minuti a visita) | Scelta del gruppo | **IPOTESI** |
| Utilizzo programmato | 85% | Scelta del gruppo | **IPOTESI** |
| Costo orario medico | 38,72 € | ACN 2026 | Fonte |
| Costo annuo comparto | 33.809 € × 1,33 = 44.965,97 € | RGS 2024; oneri 33% | Fonte + **IPOTESI** (oneri) |
| Ore annue di un tempo pieno (FTE) | 1.500 | Scelta del gruppo | **IPOTESI** |
| Amministrativi | 2 per hub, 1 per spoke | Scelta del gruppo | **IPOTESI** |
| Costo della sede | 100.000 € hub, 50.000 € spoke | **Nessuna fonte** (utenze, pulizie, manutenzione) | **IPOTESI** |
| Personale in ogni ora di apertura | 1 medico e 1 infermiere, più medici se l'ora di punta lo richiede | Scelta del gruppo | **IPOTESI** |

> Il costo della sede e gli oneri sono le ipotesi più deboli: non hanno una fonte. Sono dichiarate anche nella pagina Leggimi e nei limiti ([10](10-limiti-e-riproducibilita.md)).

**Torna all'[indice](README.md).**

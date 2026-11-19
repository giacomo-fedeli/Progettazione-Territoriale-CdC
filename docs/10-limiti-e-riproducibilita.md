# 10 – Limiti, riproducibilità e cose ancora da fare

Questo documento dice **cosa il lavoro non può dire**, **cosa serve per rifarlo da zero** e **cosa resta da controllare**.
La traccia chiede metodologie «documentate e replicabili»: qui diciamo con onestà fin dove lo sono.

---

## 1. Limiti del lavoro

### Dati
- **Solo sei mesi** (gennaio–giugno 2022) e **solo chi è andato in PS**: manca la domanda latente (chi non ci è andato).
- **Nessuna informazione clinica oltre ai codici**: diagnosi ICD-9, triage, esito. Non sappiamo se il paziente aveva un medico di famiglia, se era cronico stabile, se avrebbe accettato la CdC.
- **Anomalie:** 1.526 accessi senza dimissione, 153 senza triage, 1.747 arrivi «non rilevato», 22 residenze non utilizzabili, 2.483 accessi con diagnosi assente o senza capitolo ([03](03-anomalie-e-decisioni.md)).
- **Ticket e regime** non coerenti in 185 accessi: non corretti.
- **Personale PS Del Ponte:** la traccia dà una sola riga di personale per «030003 / 03090102» (ostetrico-ginecologico e pediatrico). Il file a 21 righe assegna a entrambi gli stessi numeri (2 medici, 6 infermieri, 3 OSS al mattino…). Se l'organico è in realtà condiviso, medici e infermieri dei due PS sono **sovrastimati**.

### Classificazione della domanda (SP2)
- Il risultato è una **stima teorica**, non una previsione di quanti pazienti andrebbero in CdC.
- Le regole sulle **diagnosi** (prefisso più lungo, permissive) e la **soglia di 2 ore** sono scelte del gruppo; non sono state validate da un clinico.
- Il **triage** è usato come indicatore di gravità: è un'approssimazione.
- Un codice vuoto non è mai considerato «soddisfatto»: sono 1.245 accessi non classificabili, quasi tutti per diagnosi o durata mancanti.

### Rete CdC (SP3) e confronto (SP4)
- **Distanze stimate** (linea d'aria × 1,3), non tempi di percorrenza reali; laghi e valli allungano i percorsi.
- **Il numero 6 dipende dalla soglia del 90%** entro 10 km (con il 95% sarebbero 8).
- **Costo della sede** (100.000 € hub, 50.000 € spoke) e **oneri del 33%** sono ipotesi **senza fonte**.
- **Un medico per sede** in tutte le sedi: la capacità è molto più alta della domanda (saturazione 5–20%). Il modello non include cronicità, prevenzione, specialistica.
- **Hub scelta per abitanti**, non per domanda: Sesto Calende è hub ma con saturazione 6,5% e 549 € a visita.
- **Rete DG** valutata con le **nostre** regole (bacino = CdC più vicina): la Direzione potrebbe assegnare i comuni in altro modo.
- **Valore PS non erogato** è una tariffa, **non un risparmio**. Le CdC costano più di quanto valgono le prestazioni PS evitate (3,86 M€ contro 1,14 M€): il loro valore sta nell'appropriatezza e nel tempo dei pazienti, non nel risparmio.
- **Stime teoriche, non effetti causali**: la traccia lo richiede.

### Modello e report
- **Filtri bidirezionali** su 9 relazioni: da tenere sotto controllo se si aggiungono visual.
- **Data/ora automatica** di Power BI attiva (13 relazioni automatiche e le tabelle `LocalDateTable_…`): si può disattivare e usare solo i calendari del modello.
- **Tre copie** del calendario, delle fasce orarie e dei turni: scelta voluta, ma raddoppia il numero di tabelle.
- **23 misure non usate** (vedi [catalogo](04b-catalogo-misure.md#misure-non-usate)).

---

## 2. Riproducibilità: cosa serve per rifare tutto

### 2.1 Il problema dei percorsi
Il file `PW4 15` legge quasi tutte le tabelle da **percorsi assoluti del PC di Shah** (per esempio `C:\Users\ShahUzairHussain\Downloads\lookup_codifiche_PS_2022_v2 (1).xlsx`). Funziona solo su quel PC. Solo le tabelle `SP3_*` usano un parametro (`Cartella_SP3`).

| Tabella / gruppo | File letto | Dove si trova nel repository (o sul PC del gruppo) |
|---|---|---|
| `Fact_PS_2022` | `fatti_ridotta.xlsx` | Non in `dati/`. Copia sul PC di Giacomo: `coda/fatti_ridotta (1).xlsx`. Sorgente: `dati/sorgenti/01_DB_Excel_PS_2022.xlsx` |
| `DIm_Pazienti` | `pazienti.xlsx` | Non presente su questo PC (file di Shah). Si rigenera dal DB: un paziente = una riga con ultimo sesso, anno di nascita, età |
| `Dim_Calendario_*` | `Dim_Calendario_Fasce_v3 1.xlsx` foglio `cal corr` | In `dati/dimensioni/` c'è `Dim_Calendario_Fasce_v3.xlsx` (versione di base); il foglio `cal corr` è nella copia di Shah |
| `DIm_Fasce_*`, `Dim_Mod_Arrivo`, `Dim_Triage_*`, `Dim_Esito_*`, `Dim_Ticket`, `Dim_Reparti`, … | `lookup_codifiche_PS_2022_v2 (1).xlsx` | In `dati/dimensioni/` c'è `lookup_codifiche_PS_2022_v2.xlsx` (versione di base). La copia «(1)» di Shah aggiunge le colonne `Compatibile_CdC` a triage ed esito e il foglio `Codice reparto modificato` |
| `DIm_Diagnosi_*` | `03_Codifiche_Diagnosi_e_Problema_principale (1).xlsx` | Su questo PC: `20 - LABORATORIO DI AI BASE/03_Codifiche_Diagnosi_e_Problema_principale_CdC.xlsx` (con `Compatibile_CdC` e foglio `Regole_CdC`). Stessi conteggi: 8.518 TRUE e 7.710 FALSE |
| `Dim_Comuni_Residenze` | `code_to_residenza_geo_pop.xlsx` | `dati/dimensioni/` ✓ |
| `Dim_Paesi_Cittadinanze` | `codici_cittadinanza_paesi.xlsx` | `dati/dimensioni/` ✓ |
| `Dim_Pronto_Soccorso` | `dim_struttura_ricovero (1).xlsx` | `dati/dimensioni/dim_struttura_ricovero.xlsx` ✓ |
| `Dim_Turni_*` | `Personale_PS_Turno.xlsx` | Non presente su questo PC. Base: `dati/dimensioni/dim_turni.xlsx` (stesse 21 righe, senza orari dei turni) |
| `SP3_*` | `SP3_rete_CdC_PowerBI.xlsx` | `SP3_rete_CdC/output/`, tramite il parametro `Cartella_SP3` ✓ |

**Cosa fare per renderlo replicabile:**
1. Mettere in `dati/elaborati/` i file preparati dal team: `fatti_ridotta.xlsx`, `pazienti.xlsx`, la versione «team» del lookup, la versione «team» del calendario (foglio `cal corr`), `Personale_PS_Turno.xlsx` e il codebook diagnosi con `Compatibile_CdC`.
2. In Power BI, *Trasforma dati → Gestisci parametri*: creare il parametro `PercorsoDati` (cartella `dati\`) e far leggere a tutte le query `PercorsoDati & "elaborati\…"` (come descritto in [`../dati/elaborati/README.md`](../dati/elaborati/README.md)).
3. Documentare **come** sono nati i file «elaborati» (quali colonne tolte e aggiunte). In questa sessione abbiamo ricostruito la struttura di `fatti_ridotta.xlsx` e di `pazienti.xlsx` dalle query, ma **non esiste uno script** che li rigeneri dal DB originale.

### 2.2 Dal DB originale al modello (passi)
1. DB originale (`01_DB_Excel_PS_2022.xlsx`, 75.664 righe) → togliere `sesso` e `anno_nascita` (vanno in `pazienti.xlsx`), aggiungere data-ora complete, durata e `Ticket_pagato` → `fatti_ridotta.xlsx`.
2. Decodifiche e calendario → file Excel `lookup…` e `Dim_Calendario…`.
3. Colonne `Compatibile_CdC` nelle tabelle triage, esito e diagnosi (regole in [06](06-domanda-potenziale-cdc.md)).
4. Power Query carica le tabelle e crea le colonne derivate ([05](05-modello-dati.md)).
5. Le colonne calcolate in DAX (`Classificazione3_CdC` ecc.) e le misure sono nel modello (file TMDL).
6. Controllare i **numeri di controllo** ([04, sezione 4](04-kpi-e-misure.md)).

### 2.3 SP3 e SP4
Vedi [07, sezione 9](07-rete-cdc-e-confronto.md): installare i pacchetti, eseguire `SP3_rete_CdC.ipynb` con *Run All*, aggiornare Power BI. Se cambia la fact, rilanciare prima `prepara_dati.py`.

### 2.4 Catalogo delle misure
Si rigenera con:

```powershell
python docs/strumenti/genera_catalogo_misure.py powerbi/PW4.SemanticModel/definition powerbi/PW4.Report/definition docs/04b-catalogo-misure.md
```

### 2.5 Strumenti per modificare il report da file
Nella cartella `SP3_rete_CdC/strumenti_powerbi/` ci sono gli script (Python) con cui sono state fatte le modifiche ai file del report (filtri anomalie, KPI, tooltip, mappa, grafici). Si usano **solo con Power BI Desktop chiuso** e dopo aver fatto una copia di sicurezza. Non fanno parte del metodo di analisi.

---

## 3. Stato del repository prima della pubblicazione

Il repository `PW4-CaseDellaComunita-G5/` ha oggi **un solo commit** («Struttura iniziale del repo PW4») e nessun remote. Questa documentazione è in `docs/`. Per pubblicare un repository completo vanno portati dentro (o aggiornati) questi elementi:

| Cosa | Dove si trova oggi | Dove va nel repository | Nota |
|---|---|---|---|
| Report e modello **di riferimento** `PW4 15` | `pbi_base2/PW4 15.pbip`, `PW4 15.Report/`, `PW4 15.SemanticModel/` | `powerbi/` (sostituire `PW4.pbip` e le due cartelle) | Il `powerbi/` del repository è la copia del 10/11/2026, **superata**. Rinominare in `PW4.pbip` e aggiornare i percorsi |
| Notebook SP3, dati, output, guida | `SP3_rete_CdC/` | `analisi/localizzazione/` | Escludere `archivio/`, `data/confini_istat_2026/` se pesa (si riscarica da ISTAT) e `~$…` |
| Script di modifica del report | `SP3_rete_CdC/strumenti_powerbi/` | `analisi/strumenti_powerbi/` (facoltativo) | |
| Piano SP0 aggiornato (17/11) | `SP0/` | `S0_Pianificazione/` | Sostituisce i file `…_tmp0.xml` del 13/11: la cartella `S0_Pianificazione` del repository è superata |
| Dati elaborati | PC di Shah e `coda/fatti_ridotta (1).xlsx` | `dati/elaborati/` | Vedi punto 2.1 |
| Storia della dashboard (bozza per l'esposizione) | `Storia_dashboard_PW4.md` | `presentazione/` | È una bozza di discorso, non documentazione |

**Da non pubblicare:** i PDF della traccia e dei docenti (diritti), i materiali del corso, le cartelle `_backup_prima_…`, i file `.pbix`, i file `.zip`, le cartelle `.pbi/` locali (già nel `.gitignore`), i file personali.
**Dimensioni:** `01_DB_Excel_PS_2022.xlsx` (12 MB) e `Fact_Finale_PowerBI.xlsx` (18 MB) sono sotto il limite di GitHub (100 MB per file). `*.xlsx` è già marcato come binario in `.gitattributes`.

**Documentazione precedente da non confondere.** Nel progetto ci sono vecchi documenti: `PW4_Guida_ai_grafici.md` (guida ai grafici della bozza di inizio novembre), `PoweBI_Base/SCARTI.md` e `COSA_HO_FATTO.md` (riordino del 12/11), `DOCUMENTAZIONE_STUDIO_CODE_CDC.md` (13/11). Riferiscono nomi di pagine e misure di versioni precedenti (per esempio la classificazione dei verdi C/X/U e le regole «Stretta» e «Larga», oggi eliminate). **I documenti in questa cartella `docs/` prevalgono.**

---

## 4. Controlli ancora da fare

| # | Cosa | Perché |
|---|---|---|
| 1 | **Fatto il 19/11:** Leggimi compilato con sintesi e pulsanti GitHub; indirizzo impostato su `https://github.com/giacomo-fedeli/Progettazione-Territoriale-CdC` (misura `GitHub indirizzo base`, cartella `9 Grafica\GitHub`). **Resta:** provare ogni pulsante (la cartella `docs/` è già su GitHub, ramo `main`; il repository è privato, quindi i pulsanti si aprono solo per chi ha accesso) | I pulsanti aprono il documento nell'anteprima di GitHub. Dettaglio in [08, sezione 9](08-dashboard-pagine.md) |
| 2 | Correggere il titolo del treemap della Direzionale: «9 accessi su 10» | Il valore esatto è 87,6%; meglio «quasi 9 su 10» o «88%» |
| 3 | **Vedere a schermo** le funzioni scritte nei file ma non verificate: pulsante «Mese per mese» (segnalibri), filtro on/off CdC, titoli e linee della revisione «il grafico parla da solo» | Le modifiche del 18/11 sono state validate sui file e con le misure, non guardando il report. Il tooltip della mappa è già stato provato e funziona |
| 4 | Rendere replicabili i percorsi (parametro `PercorsoDati`) e salvare in `dati/elaborati/` i file di Shah | Vedi 2.1 |
| 5 | Aprire i 3 file XML della SP0 in ProjectLibre; scrivere il PDF della SP0 | Verifica visiva di Gantt e istogramma |
| 6 | Verificare le fonti della letteratura (Uscher-Pines, Emilia-Romagna, ASSR) sui documenti originali | Oggi abbiamo solo link e un articolo di giornale per ASSR |
| 7 | Decidere se togliere le 31 misure non usate (elenco in [04b](04b-catalogo-misure.md)) | Pulizia: nessun numero cambia |
| 8 | Esportare il `.pbix` finale e allegarlo alla Release su GitHub; creare i tag (`S1`, `S2`, `S3`, `S4`, `finale`) | Come da regole del team nel README del repository |
| 9 | Segnalare ai docenti: il documento DG dice «9 CdC» ma elenca 10 comuni; ticket e regime non coerenti in 185 accessi | Sono dubbi sui dati forniti |
| 10 | Presentazione finale (15 minuti + 10 di discussione) | Non ancora fatta; la bozza del discorso è in `Storia_dashboard_PW4.md` |

---

## 5. Come è cambiato il lavoro (cronologia delle scelte)

Utile per capire perché alcune cose non ci sono più.

| Data | Cosa |
|---|---|
| 10/11 | Esistono due modelli: una bozza ricca del gruppo (5 pagine) e il **nuovo modello del team** (fact + dimensioni preparate da Shah). Il team sceglie il nuovo come **modello unico**. Si crea lo scheletro del repository |
| 11/11 | Grafica e navigazione (palette ASST, menu, pagine, filtri). Mappa Azure su Territorio |
| 12/11 | Riordino: pagine SP1 complete, scarti spostati in pagine TEST. Prima classificazione dei verdi (C/X/U) e scenari CdC |
| 13/11 | KPI della Direzionale rifatti come card SVG; colonna `Compatibile_CdC` sui codici ICD-9 |
| 16/11 | Regola CdC «Stretta/Larga» (due diagnosi) come imbuto; **notebook SP3** (p-median); poi versione breve e un solo metodo; filtro sulle diagnosi secondarie (20.538 → 20.419) |
| 17/11 | **Imbuto unico** `Classificazione3_CdC`; eliminate le regole dei verdi e le misure collegate; SP3 e SP4 in Power BI (tabelle `SP3_*`, misure, pagine «Rete CdC» e «Confronto»); pagine 16:9 con sottopagine; piano SP0 rifatto senza picchi |
| 18/11 | Rifinitura (piramide, Sankey, funnel quota 50%, nota decisionale); codici anomali nascosti nei grafici; regola «max 6 KPI per pagina, nessun KPI ripetuto»; classifica animata (poi spostata dietro un pulsante); tooltip della mappa; filtro on/off CdC; titoli dei grafici che «parlano da soli» |

**Cose provate e scartate** (con il motivo):
- *Mappa a comuni colorati* su Territorio: giudicata non adatta, si è tornati alle bolle.
- *Play Axis* sulla Direzionale e su Territorio: filtrava tutta la pagina o andava a scatti; tolto.
- *Classifica animata come vista principale*: il movimento distrae dai KPI e la differenza dal 5° al 10° comune è rumore (61 accessi); ora è dietro un pulsante.
- *Grafici a torta*: con più di 3 fette l'occhio non confronta gli angoli; si usano barre, Sankey e piramide.
- *Più regole di classificazione in parallelo* (verdi C/X/U, Stretta, Larga): sostituite dall'imbuto unico («un dato, una fonte, un metodo»).

**Torna all'[indice](README.md).**

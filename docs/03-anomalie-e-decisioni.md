# 03 – Anomalie trovate nei dati e decisioni

Questo documento elenca **tutto ciò che non torna** nei dati e **cosa abbiamo deciso**, con il motivo.
La traccia (pagina «Leggimi») chiede proprio questo: anomalie trovate, righe escluse o corrette, e perché.

**Come sono stati verificati i numeri.** Ogni conteggio è stato ricalcolato in due modi indipendenti:
1. direttamente dal file Excel originale `01_DB_Excel_PS_2022.xlsx` (75.664 righe) con Python/pandas;
2. con misure DAX sul modello Power BI (`PW4 15`).
I due risultati coincidono per tutte le righe di questa pagina. Dove non c'è un confronto lo diciamo.

> **Regola generale del team.** I file in `dati/sorgenti/` non si modificano mai. Ogni pulizia si fa in Power Query o in DAX e si documenta qui.
> Un accesso con un dato strano **resta nei totali** (ogni KPI torna a 75.664). Lo togliamo solo dove sarebbe una categoria senza senso (per esempio una barra «(Vuoto)»).

---

## 1. Tabella riassuntiva

| # | Anomalia | Accessi | Decisione in una riga |
|---|---|---:|---|
| 1 | Senza data/ora di dimissione | 1.526 | Fuori dai tempi di permanenza, dentro i volumi |
| 2 | Triage in ingresso e in uscita assente | 153 | Nei totali; nascosto nei grafici per triage |
| 3 | Modalità di arrivo «Non rilevato» | 1.747 | Nei totali; fuori dalla quota «arrivi autonomi» e dai grafici per arrivo |
| 4 | Residenza vuota | 9 | Nei totali; nascosti nei grafici per comune e sulla mappa |
| 5 | Residenza con codice presente ma comune «Non trovato» | 13 | Come sopra |
| 6 | Diagnosi principale assente o non nel codebook | 1.604 | Nei totali; nascosti nei grafici per diagnosi; «non classificabile» per la domanda CdC |
| 7 | Diagnosi presente ma senza capitolo ICD-9 (codici COVID) | 879 | Nei totali; nascosti nel grafico per categoria |
| 8 | Stesso paziente con due sessi diversi | 10 (3 pazienti) | Si tiene l'ultimo sesso registrato |
| 9 | Ticket registrato ≠ regime di erogazione | 185 | Nessuna correzione; la stima del ticket è separata dal registrato |
| 10 | Ticket stimato ≠ ticket registrato sui codici bianchi | 3.230 bianchi senza ticket | Si mostrano entrambi e la differenza (80.750 €) |
| 11 | Permanenze molto lunghe (oltre 24 ore) | 4.845 | Tenute; per i tempi si usano mediana e 90° percentile, mai la media |
| 12 | Coordinate di alcuni PS senza virgola decimale | – | Colonne «corretta» con regola esplicita |
| 13 | Comuni fusi con più codici ISTAT | – | Popolazione contata una volta per comune |
| 14 | Documento DG: «9 CdC» ma 10 comuni elencati | – | Valutate tutte e 10 |

I punti 1–8 sono anche scritti nella pagina **Leggimi** del report (box «Anomalie e decisioni»).

---

## 2. Dettaglio

### 1. Accessi senza data/ora di dimissione – 1.526 (2,0%)
- **Come si vede:** `data_dim` e `ora_dim` vuote nel file originale; nella fact `data_ora_dimissione` è vuota.
- **Chi sono:** 1.521 hanno esito 7 «il paziente abbandona il PS in corso di accertamenti e/o prima della chiusura della cartella»; 3 hanno esito 1 (dimissione a domicilio); 2 hanno esito 2 (ricovero).
- **Decisione:** restano nei volumi (accessi, valore, diagnosi, triage…). Sono esclusi da:
  - permanenza (mediana e 90° percentile);
  - pazienti presenti per ora (non hanno un'ora di fine);
  - durata presa in carico → dimissione, quindi nella classificazione CdC il criterio «durata ≤ 2 ore» risulta **vuoto**.
- **Perché:** lo chiede la traccia («si escludono dai tempi di permanenza ma restano nei volumi; indicatene il numero nella pagina Leggimi»).
- **Dove si vede:** misura `Accessi senza dimissione`; numero di controllo nel Leggimi.

### 2. Triage in ingresso e in uscita assente – 153
- **Come si vede:** `triage_ingresso` e `triage_uscita` vuoti **sulle stesse 153 righe**.
- **Decisione:** nei totali sì. Nei grafici per triage il vuoto è nascosto con un filtro per visual (`ds_f_anom_colore`). Nella classificazione CdC il criterio è **vuoto** → l'accesso è «non classificabile» se nessun altro criterio è falso.
- **Perché:** non è un colore di triage, quindi non si può leggere né confrontare. Il codice «ND» c'è nel lookup ma non è mai usato nei dati: nel modello il vuoto resta vuoto.

### 3. Modalità di arrivo «Non rilevato» – 1.747
- **Come si vede:** `mod_arr = 9`.
- **Decisione:** nei totali sì. Esclusi dal denominatore di `% arrivi autonomi` e nascosti nei grafici per arrivo.
- **Perché:** è un codice di dato mancante, non un modo di arrivare. Contarlo come «non autonomo» gonfierebbe i casi gravi.

### 4–5. Residenza non utilizzabile – 9 + 13 = 22
- **9 vuoti:** `residenza` vuota nel file originale.
- **13 «Non trovato»:** il codice c'è (9 codici distinti, per esempio `012532`, `012519`, `99X224`) ma nel file dei comuni risulta con provincia «Non trovato».
- **Decisione:** nei totali sì. Nei grafici per comune e sulla mappa filtriamo `Provincia` diversa da vuoto e da «Non trovato» (filtro `ds_f_anom_provincia`). Filtriamo sulla provincia, non sul comune, per non toccare le classifiche TopN.
- **Perché:** non si possono mettere su una mappa né assegnare a una CdC.
- **Nota:** 812 accessi hanno residenza estera (provincia «Estero»). Sono validi: restano ovunque. Non entrano nel territorio del progetto SP3 (vedi [07](07-rete-cdc-e-confronto.md)).

### 6. Diagnosi principale assente o non decodificabile – 1.604
- **Composizione:** 1.541 con `diagn_pr` vuoto + 63 con codice `04331`/`04332`, che non sono nel codebook ICD-9 fornito (sono codici regionali COVID-19).
- **Decisione:** nei totali sì. Nei grafici per diagnosi il vuoto è nascosto. Nella classifica «prime 7 categorie» il vuoto è escluso **prima** di scegliere le 7 (con alcuni PS, per esempio Cittiglio e il Pediatrico, il vuoto entrava tra le prime 7).
- **Classificazione CdC:** diagnosi vuota → criterio vuoto → «non classificabile». Dei 1.245 accessi non classificabili, 1.192 hanno la diagnosi primaria senza regola.

### 7. Diagnosi presente ma senza capitolo ICD-9 – 879
- **Cosa sono:** 16 codici del codebook senza categoria. Sono tutti codici COVID-19 (per esempio `04321`, `04311`, `48041`, `V1204`).
- **Decisione:** nei totali sì; nascosti nel grafico per categoria di diagnosi (`ds_f_anom_*`).
- **Effetto:** nei grafici per categoria la somma delle barre può essere più bassa del totale. Il massimo è il **3,3%** (2.483 accessi su 75.664 tra i punti 6 e 7).

### 8. Stesso paziente con sesso diverso – 3 pazienti, 10 accessi
- **Come si vede:** nel file originale `sesso` cambia tra un accesso e l'altro per lo stesso `id_pz`. L'anno di nascita è sempre coerente.
- **Decisione:** si tiene **l'ultimo sesso registrato** (quello dell'accesso più recente). Nel modello il sesso sta nella tabella `DIm_Pazienti`, non nella fact, quindi un paziente ha un solo sesso.
- **Verificato:** SIMP0002659 → Maschio; SIMP0043711 → Femmina; SIMP0045625 → Maschio.
- **Perché:** un paziente deve avere un solo sesso e l'ultimo dato è il più aggiornato.

### 9. Ticket registrato non coerente con il regime di erogazione – 185
- **Come si vede:** `reg_erog` (regime) e `tck` (ticket) non coincidono: 138 accessi con regime «SSN + ticket» ma ticket 0; 15 con ticket da 25 € e regime SSN; 32 con ticket da 25 € e regime «Ministero Interni».
- **Decisione:** nessuna correzione. Usiamo `tck` come «ticket registrato». Segnalato come «da verificare» con chi ha fornito i dati.
- **Perché:** non abbiamo una regola per sapere quale dei due campi sia giusto.

### 10. Ticket stimato e ticket registrato sui codici bianchi
- **Stima (traccia):** codici bianchi in **uscita** (5.304) × 25 € = **132.600 €**.
- **Registrato:** 2.074 accessi con ticket da 25 € = **51.850 €**. Sono tutti codici bianchi in uscita: nessun altro codice ha ticket.
- **Differenza:** 80.750 €. Per 3.230 bianchi (il 61%) non c'è un ticket registrato.
- **Decisione:** mostriamo le due cifre separate (misure `Ticket stimato €`, `Ticket registrato €`, `Scostamento ticket €`). Ipotesi: i 3.230 possono essere esenti o non pagati; non abbiamo i dati per dirlo.
- **Perché:** la traccia dice che la stima è una **compartecipazione alla spesa**, non il costo del servizio, e va distinta dal registrato.

### 11. Permanenze molto lunghe – 4.845 oltre 24 ore
- **Come si vede:** 4.845 accessi superano le 24 ore; 1.507 superano le 48 ore; il massimo è 10.263 minuti (7,1 giorni).
- **Decisione:** tenuti. Non sono errori evidenti (l'ordine temporale è sempre rispettato: nessuna durata negativa).
- **Effetto sui KPI:** la media sarebbe fuorviante. Il 90° percentile di permanenza vale 1.049 minuti (circa 17,5 ore) mentre la mediana è 178 minuti. Per questo il report usa **mediana e 90° percentile**, come chiede la traccia.

### 12. Coordinate dei PS
- **Come si vede:** nel file `dim_struttura_ricovero` alcune coordinate hanno perso la virgola (es. `45815453853118` al posto di `45,815453853118`).
- **Decisione:** due colonne calcolate nel modello, `Latitudine corretta` e `Longitudine corretta`. Regola: latitudine > 90 → si riportano 2 cifre intere (45–46 per Varese); longitudine > 180 → 1 cifra intera (8–9 per Varese).
- **Perché:** servono per mettere i 7 PS sulla mappa.

### 13. Comuni fusi
- **Cosa succede:** nel file dei comuni un comune nato da fusione può avere più codici ISTAT con la stessa popolazione ripetuta.
- **Decisione:** la misura `Accessi per 1.000 ab.` conta la popolazione **una sola volta per comune**.
- **Nel notebook SP3:** i codici dello stesso comune sono sommati (la tabella `SP3_Assegnazione` ha una riga per codice ISTAT, 230 righe in tutto).

### 14. Documento della Direzione Generale
- Il testo dice «9 Case della Comunità», ma la tabella elenca **10 comuni** (Angera, Arcisate, Azzate, Cuasso al Monte, Gavirate, Laveno-Mombello, Luino, Sesto Calende, Tradate, Varese).
- **Decisione:** valutate tutte e 10. Da segnalare ai docenti.

---

## 3. Cose controllate che **non** sono anomalie

| Controllo | Esito |
|---|---|
| Righe duplicate (tutte le colonne uguali) | 0 |
| Date fuori dal periodo | Nessuna: dal 01/01/2022 al 30/06/2022 (181 giorni) |
| Durate negative (presa in carico prima dell'arrivo, dimissione prima della presa in carico) | 0 |
| Valore delle prestazioni ≤ 0 o numero di prestazioni ≤ 0 | 0 (valore minimo 1,70 €) |
| Reparto vuoto in 65.369 accessi | Atteso: il reparto è valorizzato **solo** quando l'esito è ricovero (10.295 accessi), e sempre |
| Diagnosi secondaria vuota in 69.972 accessi (92,5%) | Atteso: la secondaria è facoltativa. Per la classificazione CdC la secondaria vuota non conta |
| Attesa di 0 minuti (arrivo = presa in carico) | 533 accessi: plausibile, tenuti |
| Problema principale vuoto | 72 accessi: non è usato nei KPI |
| Triage «nero» (N) | 17 in ingresso, 238 in uscita; 15 «giunto cadavere» tutti con triage N. Non è un'anomalia: **non** è nascosto |
| Età 0 anni / 100 anni o più | 496 / 51 accessi: plausibili, tenuti |
| Esiti previsti dal PDF ma assenti nei dati | «Ricovero in OBI» (0) e «Abbandono pre-visita» (6): nessun accesso |
| Codice «responsabile invio» 0 non previsto dal PDF | 1 accesso: non decodificabile, tenuto |
| Cittadinanza | Tutti i codici sono decodificati dal file `codici_cittadinanza_paesi.xlsx` (ANPR) |

---

## 4. Dove sono applicate le decisioni

| Decisione | Strumento nel progetto |
|---|---|
| Esclusione dai tempi | Misure DAX: `MEDIAN` e `PERCENTILE.INC` ignorano i vuoti; `Accessi senza dimissione` li conta |
| Nascondere i vuoti nei grafici | Filtri a livello di singolo visual con prefisso `ds_f_anom_` (script `SP3_rete_CdC/strumenti_powerbi/nascondi_anomalie.py`) |
| Ultimo sesso del paziente | Tabella `pazienti.xlsx` → `DIm_Pazienti` |
| Coordinate PS | Colonne calcolate in `Dim_Pronto_Soccorso` |
| Dati mancanti nella classificazione CdC | Colonna `Classificazione3_CdC` (vedi [06](06-domanda-potenziale-cdc.md)) |

Il filtro si vede nel riquadro *Filtri* di ogni grafico e si toglie con un clic. I grafici nelle pagine **Bozza** e **Tooltip** non hanno questi filtri.

**Torna all'[indice](README.md).**

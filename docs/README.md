# Documentazione del progetto PW4 – Case della Comunità

**ITS Data Analyst – Project Work 4: Laboratorio di AI base** (case study LIUC)
**Gruppo 5:** Fedeli Giacomo · Murariu Vlad Teodor · Shah Uzair Hussain

Questa cartella contiene la documentazione di **tutto il lavoro fatto**: metodo, fonti, anomalie, definizione dei KPI e delle misure, modello dati, e i documenti di ogni sottoprova.
È scritta in Markdown, quindi si legge direttamente su GitHub.

*Stato: 18/11/2026. Report di riferimento: `PW4 15.pbip`. Dati: accessi ai 7 Pronto Soccorso dell'ASST dei Sette Laghi, gennaio–giugno 2022.*

---

## Da dove cominciare

| Se vuoi… | Leggi |
|---|---|
| Capire il progetto in 5 minuti | Questa pagina, poi [01 – Metodo](01-metodo.md) |
| Sapere se i dati sono affidabili | [03 – Anomalie e decisioni](03-anomalie-e-decisioni.md) |
| Sapere da dove arriva ogni numero | [02 – Fonti](02-fonti.md) |
| Capire cosa significa ogni KPI | [04 – KPI e misure](04-kpi-e-misure.md) |
| Vedere la formula DAX di una misura | [04b – Catalogo delle misure](04b-catalogo-misure.md) |
| Capire il modello dati | [05 – Modello dati](05-modello-dati.md) |
| Capire come si decide cosa va in CdC | [06 – Domanda potenziale](06-domanda-potenziale-cdc.md) |
| Capire dove aprire le CdC e il confronto con la Direzione | [07 – Rete CdC e confronto](07-rete-cdc-e-confronto.md) |
| Sapere cosa mostra ogni pagina della dashboard | [08 – Dashboard](08-dashboard-pagine.md) |
| Vedere il piano di progetto e i costi | [09 – Pianificazione (SP0)](09-pianificazione-sp0.md) |
| Sapere cosa non funziona o cosa manca | [10 – Limiti e riproducibilità](10-limiti-e-riproducibilita.md) |
| Cercare una sigla | [11 – Glossario](11-glossario.md) |

---

## I documenti

| # | Documento | Contenuto |
|---|---|---|
| 01 | [Metodo](01-metodo.md) | Dal problema alla raccomandazione, passo per passo, con i principi di lavoro e i controlli |
| 02 | [Fonti](02-fonti.md) | File → tabella del modello; fonti normative, scientifiche e istituzionali; parametri con fonte o **IPOTESI** |
| 03 | [Anomalie e decisioni](03-anomalie-e-decisioni.md) | 14 anomalie con numeri verificati, decisione e motivo; controlli che non sono anomalie |
| 04 | [KPI e misure](04-kpi-e-misure.md) | Tabella «Dalla domanda al KPI», KPI di ogni pagina, studio delle code, numeri di controllo |
| 04b | [Catalogo delle misure](04b-catalogo-misure.md) | Tutte le 299 misure del modello con formula DAX (**generato** dallo script) |
| 05 | [Modello dati](05-modello-dati.md) | Schema a stella, relazioni, data dictionary della fact e delle dimensioni |
| 06 | [Domanda potenziale](06-domanda-potenziale-cdc.md) | SP2: criteri, regole, imbuto, tre classi, quota presa in carico |
| 07 | [Rete CdC e confronto](07-rete-cdc-e-confronto.md) | SP3 e SP4: p-median, capacità, costi, matrice, sensibilità, nota decisionale |
| 08 | [Dashboard](08-dashboard-pagine.md) | Le pagine, i grafici e i messaggi |
| 09 | [Pianificazione (SP0)](09-pianificazione-sp0.md) | WBS, reticolo, budget, EVM |
| 10 | [Limiti e riproducibilità](10-limiti-e-riproducibilita.md) | Limiti, come rifare tutto, controlli in sospeso, cronologia delle scelte |
| 11 | [Glossario](11-glossario.md) | Sigle e termini |

---

## I numeri chiave

Tutti ricalcolati dal file originale e dal modello (vedi [04, sezione 5](04-kpi-e-misure.md)).

| | |
|---|---|
| Accessi ai 7 PS (01/01–30/06/2022) | **75.664** (418 al giorno) |
| Pazienti distinti | 58.320 |
| Valore delle prestazioni (tariffa, non costo) | 9.840.639,33 € |
| Attesa mediana · 90° percentile | 37 · 203 minuti |
| Permanenza mediana · 90° percentile | 178 · 1.049 minuti |
| Codici bianchi in uscita | 5.304 (7,0%) |
| Accessi senza dimissione | 1.526 |
| **Potenzialmente compatibili con una CdC** | **20.419 (27,0%)** |
| Non classificabili · non compatibili | 1.245 · 54.000 |
| Presa in carico con quota 50% (teorica) | 10.210 accessi (−13,5% sugli accessi PS) |
| **Rete proposta** | **6 CdC** (4 hub h24 e 2 spoke), 4,97 km medi, 93,2% della domanda entro 10 km |
| Visite gestite all'anno · costo annuo | 15.310 · 3,86 M€ (252 € a visita) |
| Rete della Direzione Generale | 10 CdC, 3,97 km, 99,3% entro 10 km, 13.967 visite, 5,27 M€ (378 € a visita) |

**Raccomandazione (bozza del gruppo):** la rete proposta di 6 CdC, a condizione di accettare circa 1 km in più di distanza media e di garantire i trasporti per i comuni oltre 10 km (7% della domanda). Testo completo e tre evidenze in [07](07-rete-cdc-e-confronto.md).

---

## Corrispondenza con la traccia

| La traccia chiede | Dove |
|---|---|
| Documentazione dei dati e delle variabili (SP1) | [05](05-modello-dati.md), [02](02-fonti.md) |
| Anomalie trovate, righe escluse o corrette, e perché (Leggimi) | [03](03-anomalie-e-decisioni.md) |
| Definizione di ogni KPI e numeri di controllo (Leggimi) | [04](04-kpi-e-misure.md) |
| Tabella «Dalla domanda al KPI» (4–6 KPI della Direzionale) | [04, sezione 2](04-kpi-e-misure.md) |
| Metodologie documentate e replicabili | [01](01-metodo.md), [10](10-limiti-e-riproducibilita.md) |
| Fonti normative, scientifiche e istituzionali (SP2, SP3) | [02, sezione 4](02-fonti.md) |
| Criteri di inclusione ed esclusione, regole sulle variabili, ipotesi, casi dubbi (SP2) | [06](06-domanda-potenziale-cdc.md) |
| Metodo di localizzazione, obiettivo, vincoli, distanze, domanda esterna, capacità, costi (SP3) | [07, sezioni 1–5](07-rete-cdc-e-confronto.md) |
| Confronto strutturato, matrice multidimensionale, sensibilità, nota decisionale (SP4) | [07, sezioni 6–7](07-rete-cdc-e-confronto.md) |
| Pianificazione, WBS, reticolo, budget, CV/CPI/SV/SPI/EAC (SP0) | [09](09-pianificazione-sp0.md) |
| Presentazione finale con problema, metodo, risultati, raccomandazione, ipotesi e limiti | La bozza del discorso è `Storia_dashboard_PW4.md`; limiti in [10](10-limiti-e-riproducibilita.md) |

---

## Convenzioni

- **Numeri** in formato italiano: punto per le migliaia, virgola per i decimali (20.419; 3,86 M€).
- **«CdC»** = Casa della Comunità. **«PS»** = Pronto Soccorso. **«DG»** = Direzione Generale.
- **IPOTESI** in grassetto = scelta del gruppo senza fonte esterna.
- **Stime teoriche, non effetti causali**: nessun risultato su CdC dimostra un effetto reale (la traccia lo richiede).
- I file di dati, i PDF dei docenti e il report `.pbip` non sono in questa cartella: vedi [10, sezione 3](10-limiti-e-riproducibilita.md) per cosa va aggiunto al repository.

## Come è stata verificata questa documentazione

- Totali e anomalie: ricalcolati con **Python/pandas** dal file `01_DB_Excel_PS_2022.xlsx` e con **misure DAX** sul modello aperto (`PW4 15`), il 18/11/2026. I due risultati coincidono.
- Definizioni dei KPI, formule e relazioni: lette dai **file TMDL e PBIR** del progetto; il [catalogo delle misure](04b-catalogo-misure.md) è generato da script.
- Dati dell'SP3 e dell'SP4: letti dalle tabelle del modello e dal notebook.
- **Non verificato:** il comportamento a schermo di alcune funzioni aggiunte il 18/11 e l'apertura dei file SP0 in ProjectLibre (elenco in [10, sezione 4](10-limiti-e-riproducibilita.md)).

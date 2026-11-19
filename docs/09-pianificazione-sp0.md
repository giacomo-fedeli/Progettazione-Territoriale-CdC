# 09 – Pianificazione del progetto (SP0)

La sottoprova 0 chiede di pianificare il progetto: obiettivo, date, team, attività, WBS fino al 4° livello, reticolo, costi e budget, e gli indicatori di performance (EVM) al **5° giorno** e all'**ultimo giorno**.
La traccia chiede un documento PDF con il lavoro fatto in ProjectLibre (o altri strumenti). Qui c'è la sintesi del metodo e dei numeri; le tabelle complete, la legenda e i file di progetto sono nella cartella `SP0/`.

> **Fonte unica.** Tutti i file della SP0 nascono da due script, `SP0/genera_sp0.py` e `SP0/sp0_tabelle.py`. Il dato di partenza è la tabella delle attività dentro lo script: per cambiare un numero si cambia lì e si rilancia `python genera_sp0.py`.
> La versione precedente è in `SP0/vecchi/` (con picchi di carico del 300%, superata).

---

## 1. Dati di base

| Voce | Valore |
|---|---|
| Committente | Direzione Strategica – azienda sanitaria della provincia di Varese |
| Obiettivo | Dall'analisi degli accessi in PS alla proposta di rete delle Case della Comunità e al confronto con la Direzione Generale |
| Inizio | lunedì 09/11/2026, ore 08:00 |
| Fine | **venerdì 20/11/2026, ore 17:00** (uguale nei tre file) |
| Calendario | lun–ven, 08:00–12:00 e 13:00–17:00 = 8 ore al giorno (un solo calendario) |
| Durata totale (dal reticolo) | **80 ore lavorative = 10 giorni** |
| Team | Shah Uzair Hussain (SU, project manager), Fedeli Giacomo (GF, BI developer), Murariu Vlad Teodor (MV, analista territoriale) |
| Attività | 52 attività (livello 4) e 9 milestone |
| Ore pianificate | 228 ore-persona: 76 a testa su 80 disponibili (4 ore di riserva ciascuno) |

## 2. WBS

La WBS ha **4 livelli**, con criterio **ibrido** (fasi + deliverable):
1. progetto;
2. fase (le sottoprove della traccia, **in ordine di tempo**): 1.1 SP0 avvio · 1.2 SP1 · 1.3 SP0 controllo al giorno 5 · 1.4 SP2 · 1.5 SP3 · 1.6 SP4 · 1.7 chiusura;
3. deliverable (per esempio 1.2.2 «Dashboard SP1»);
4. attività (per esempio 1.2.2.3 «Pagina Flussi»): lavoro di **una sola persona**, con ore e costo.

La SP0 compare tre volte (1.1, 1.3, 1.7) per un motivo pratico: ProjectLibre ignora i legami «all'indietro» nella WBS, quindi la WBS segue l'ordine del tempo e tutte le frecce vanno in avanti.

## 3. Reticolo e cammino critico

- Legami solo **fine-inizio**. Nessun vincolo di data: le date nascono dai legami.
- Ogni persona fa una cosa alla volta (legame di risorsa, indicato con (R) nelle tabelle).
- Il cammino critico passa per le attività di modello, criteri, rete e confronto: dalla raccolta dati (1.1.1.3), al modello dati (1.2.1.x), ai criteri CdC (1.4.1.x), al modello di localizzazione (1.5.2.1), all'inserimento della configurazione DG (1.6.1.x), fino alla consegna finale.
- **Milestone**: M1 piano approvato · M2 modello validato · M3 consegna SP1 · M4 controllo del giorno 5 · M5 consegna SP2 · M7 proposta di rete congelata (SP3) · M8 arriva la configurazione DG (evento esterno) · M9 confronto completato (SP4) · M10 consegna finale.

## 4. Risorse, costi e budget

| Persona | Costo orario | Ore pianificate | Costo pianificato | Ore effettive | Costo effettivo |
|---|---:|---:|---:|---:|---:|
| Shah Uzair Hussain | 27 €/h | 76 | 2.052 € | 80 | 2.160 € |
| Fedeli Giacomo | 25 €/h | 76 | 1.900 € | 80 | 2.000 € |
| Murariu Vlad Teodor | 25 €/h | 76 | 1.900 € | 80 | 2.000 € |
| Costi fissi | | | 82 € | | 82 € |

**Costi fissi** (per attività): licenze Power BI Pro 3 × 14 € = 42 € (kick-off e ambiente di lavoro); servizio di calcolo distanze 15 € (metodo di localizzazione); stampa e materiali 25 € (presentazione).
**Le tariffe orarie sono ipotesi del gruppo** (profili junior), non dati ufficiali.

| Fase | Ore | Budget |
|---|---:|---:|
| 1.1 SP0 – Avvio e pianificazione | 24 | 674 € |
| 1.2 SP1 – Analisi dei flussi e dei bisogni | 76 | 1.940 € |
| 1.3 SP0 – Controllo al giorno 5 | 4 | 108 € |
| 1.4 SP2 – Domanda potenziale per le CdC | 28 | 708 € |
| 1.5 SP3 – Progettazione della rete CdC | 48 | 1.247 € |
| 1.6 SP4 – Confronto Proposta contro Direzione Generale | 30 | 770 € |
| 1.7 Chiusura – presentazione, controllo finale, consegna | 18 | 487 € |
| **Totale (BAC)** | **228** | **5.934 €** |

I **costi di istituzione delle CdC** non rientrano nel progetto (indicazione della traccia). Il budget qui è quello del **progetto di analisi** (ore del team), non quello della rete di CdC.

## 5. Indicatori di performance (EVM)

Formule: **PV** valore pianificato · **EV** = Σ (% di completamento × budget) · **AC** costi effettivi · **CV = EV − AC** · **CPI = EV ÷ AC** · **SV = EV − PV** · **SPI = EV ÷ PV** · **EAC = AC + (BAC − EV)**, cioè i costi che restano saranno quelli previsti (ipotesi della traccia).

| Indicatore | Giorno 5 (ven 13/11, ore 17:00) | Ultimo giorno (ven 20/11, ore 17:00) |
|---|---:|---:|
| BAC | 5.934 € | 5.934 € |
| PV | 3.022 € | 5.934 € |
| EV | 2.893 € | 5.934 € |
| AC | 3.122 € | 6.242 € |
| **CV** | **−229 €** | **−308 €** |
| **CPI** | **0,927** | **0,951** |
| **SV** | **−129 €** | **0 €** |
| **SPI** | **0,957** | **1,000** |
| **EAC** | **6.163 €** (VAC −229 €); se l'efficienza restasse quella di oggi: BAC ÷ CPI = 6.404 € | 6.242 € (a consuntivo) |
| % completamento | 48,8% (pianificata 50,9%) | 100% |

**Commento.**
- **Giorno 5.** Per ogni euro speso abbiamo prodotto 93 centesimi di lavoro (CPI 0,93) e abbiamo fatto il 96% del lavoro previsto a questa data (SPI 0,96). Tutti hanno lavorato 8 ore al giorno, ma alcune attività hanno richiesto più ore del previsto (Pagina Attese e code, Pagina Direzionale, Studio delle code, Controllo della dashboard SP1). Tre attività sono ancora aperte e la consegna SP1 slitta da venerdì 12:00 a lunedì 16/11 alle 10:00. Azione: usare le 4 ore di riserva di ciascuno nella seconda settimana.
- **Ultimo giorno.** Il progetto è in tempo (SPI 1,00), venerdì 20/11 alle 17:00, senza straordinari. È costato il **5,2% in più** del budget (CPI 0,95): sono le 12 ore di riserva usate (4 a testa). Lezione: senza riserva il ritardo del giorno 5 avrebbe spostato la fine del progetto.

> **Cosa sono questi dati di avanzamento.** I due stati sono **stime del gruppo** (la traccia chiede di «stimare costi sostenuti e % di completamento»). Sono scritte nella tabella delle attività dello script `SP0/genera_sp0.py` e coincidono in tutti i file (XML, Excel, testo). Le ore reali delle attività che si sono scostate dal piano sono nella tabella 9 della legenda (`SP0/PW4_G5_SP0_legenda.md`).

## 6. I file della SP0

| File | Cosa contiene |
|---|---|
| `PW4_G5_SP0_1_baseline.xml` | Il piano approvato (baseline): WBS, Gantt, reticolo, risorse, costi. Si apre in ProjectLibre |
| `PW4_G5_SP0_2_giorno5.xml` | Lo stesso piano con l'avanzamento al giorno 5 |
| `PW4_G5_SP0_3_ultimo_giorno.xml` | Lo stesso piano a progetto concluso |
| `PW4_G5_SP0_tabelle.xlsx` | Tabelle per il report, **con formule** (WBS, reticolo, risorse, budget, EVM, milestone) |
| `PW4_G5_SP0_numeri.md` | Le stesse tabelle in testo |
| `PW4_G5_SP0_legenda.md` | Ogni termine, sigla e attività; dizionario WBS; glossario di project management |
| `genera_sp0.py`, `sp0_tabelle.py` | Rigenerano tutto |

### Regole per ProjectLibre scoperte aprendo i file (versione 1.9.8)

1. **Nessun vincolo di data.** Risalvando da ProjectLibre i vincoli «non prima di» si perdono e le attività tornano al 9/11. Le date devono nascere solo dai legami.
2. **Legami solo «in avanti»** nell'ordine della WBS.
3. **Avanzamento e baseline** vanno scritti nei dati «a fasi di tempo» delle assegnazioni (tipo 2 = ore effettive, 1 = ore rimanenti, 4 = baseline).
4. **Importi in euro**, non in centesimi (ProjectLibre non li divide per 100).
5. **Un solo calendario** (8–12, 13–17), nessun calendario personale.
6. **Una persona per attività** e nessuna unità sopra il 100%: evita i picchi di carico del 300%.

### Controlli fatti dallo script e da una verifica indipendente degli XML

- Ogni persona ha al massimo 8 ore al giorno in tutti e 3 i file (istogramma mai sopra il 100%).
- Fine progetto venerdì 20/11/2026 alle 17:00 in tutti e 3 i file.
- Un solo calendario, nessun vincolo di data, nessun legame all'indietro, nessuna assegnazione sulle attività di riepilogo.
- Le formule dell'Excel danno gli stessi numeri dello script (ricalcolo via COM su una copia).
- **Non ancora fatto:** aprire i 3 file in ProjectLibre e guardare Gantt e istogramma a schermo; scrivere il PDF finale.

**Torna all'[indice](README.md).**

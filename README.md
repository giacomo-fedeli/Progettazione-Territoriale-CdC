# PW4 – Dall'analisi dei bisogni alla rete delle Case della Comunità

**ITS Data Analyst – Project Work 4: Laboratorio di AI base** (case study LIUC)
**Gruppo 5:** Fedeli Giacomo · Murariu Vlad Teodor · Shah Uzair Hussain

## La domanda della Direzione Strategica

1. Come sono distribuiti sul territorio i bisogni oggi intercettati dai servizi ospedalieri?
2. Quale quota potrebbe essere gestita dalle Case della Comunità (CdC)?
3. Come dovrebbe essere configurata una rete territoriale per rispondere a tale domanda
   e come si confronta con la configurazione assunta dalla Direzione Generale?

## Documentazione

Metodo, fonti, anomalie e decisioni, definizione dei KPI e delle misure, modello dati e documenti di ogni sottoprova sono in **[docs/](docs/README.md)** (si leggono direttamente su GitHub).

## Dove trovare le consegne

| Sottoprova | Cosa chiede la traccia | Deliverable | Stato |
|---|---|---|---|
| **S0** Pianificazione | WBS al 4° livello, reticolo, budget, CV/CPI/SV/SPI/EAC al giorno 5 e all'ultimo giorno | [S0_Pianificazione/](S0_Pianificazione/) | ⬜ da fare |
| **S1** Flussi e bisogni | Dashboard navigabile, documentazione dati, sintesi + tabella «Domanda → KPI» | [powerbi/](powerbi/) · [dati/README.md](dati/README.md) · [S1_Flussi_e_bisogni/](S1_Flussi_e_bisogni/) | ⬜ da fare |
| **S2** Domanda potenziale | Criteri nel modello, misure «compatibile» e «presa in carico», pagina «Domanda potenziale» | [powerbi/](powerbi/) · [dati/criteri/](dati/criteri/) · [S2_Domanda_potenziale/](S2_Domanda_potenziale/) | ⬜ da fare |
| **S3** Rete CdC | Max 10 CdC, bacini, mappa, capacità, costi annui di funzionamento | [S3_Rete_CdC/](S3_Rete_CdC/) · [dati/scenari/](dati/scenari/) · [analisi/localizzazione/](analisi/localizzazione/) | ⬜ da fare |
| **S4** Confronto con la DG | Matrice multidimensionale, sensibilità (30/50/70%), nota decisionale, pagina «Confronto» | [powerbi/](powerbi/) · [S4_Confronto_DG/](S4_Confronto_DG/) | ⬜ da fare |
| **Finale** | Presentazione 15 min + 10 min di discussione | [presentazione/](presentazione/) | ⬜ da fare |

## Struttura del repository

```
powerbi/          UNICO modello Power BI (PBIP) che cresce da S1 a S4
dati/             sorgenti fornite, dimensioni, criteri S2, scenari S3/S4
analisi/          script replicabili (localizzazione), se usati
S0_ … S4_         documenti PDF consegnati per ogni sottoprova
presentazione/    slide finali
riferimenti/      bibliografia (fonti citate, non i PDF)
```

## Come aprire il report

1. Clonare il repository.
2. Aprire `powerbi/PW4.pbip` con Power BI Desktop.
3. In *Trasforma dati → Gestisci parametri*, impostare **`PercorsoDati`** sulla cartella
   `dati\` del proprio clone (con la barra finale), ad esempio `C:\…\PW4-CaseDellaComunita-G5\dati\`.
4. Verificare che in `dati/elaborati/` ci siano i 4 file preparati dal team (vedi [dati/elaborati/README.md](dati/elaborati/README.md)).
5. *Aggiorna*. I numeri di controllo sono nella pagina **Leggimi** e in [dati/README.md](dati/README.md).

## Versioni consegnate

A ogni consegna si crea un tag Git (`S1`, `S2`, `S3`, `S4`, `finale`) e una *Release* su GitHub
con allegato il file `.pbix` esportato. Così resta la versione della pagina «Leggimi» di ogni sottoprova.

## Regole del team

- Il modello è uno solo: niente copie `PW4_v2.pbip`, `PW4_finale.pbip`. Le versioni le tiene Git.
- I file in `dati/sorgenti/` non si modificano mai: le pulizie si fanno in Power Query e si documentano.
- Ogni numero citato nei PDF deve essere ritrovabile nella dashboard.

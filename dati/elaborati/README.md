# dati/elaborati/ – file preparati dal team (fuori da Power BI)

Il modello in `../../powerbi/` legge questi 4 file. **Vanno aggiunti qui** da chi li ha preparati:

| File atteso qui | Usato da | Nome originale sul PC di chi l'ha creato |
|---|---|---|
| `fatti_ridotta.xlsx` (foglio `Sheet1`) | `Fact_PS_2022` | `fatti_ridotta.xlsx` |
| `pazienti.xlsx` (foglio `Sheet1`) | `DIm_Pazienti` | `pazienti.xlsx` |
| `lookup_codifiche_PS_2022_team.xlsx` | 10 dimensioni di decodifica (triage, esito, arrivo, …) | `lookup_codifiche_PS_2022_v2 (1).xlsx` |
| `Dim_Calendario_Fasce_team.xlsx` (foglio `cal corr`) | `Dim_Calendario` | `Dim_Calendario_Fasce_v3 1.xlsx` |

Gli ultimi due sono versioni **modificate** dei file in `../dimensioni/`. Contengono fogli che negli originali non ci sono: `cal corr`, `problemaprincipale`, `Codice reparto modificato`.

## Da documentare (replicabilità)

La traccia chiede metodologie «documentate e replicabili». Per ogni file indicare:
- da quale file sorgente nasce (es. `../sorgenti/01_DB_Excel_PS_2022.xlsx`);
- quali righe o colonne sono state tolte, corrette o aggiunte, e perché;
- con quale strumento (script Python in `../../analisi/preparazione/`, Excel a mano, …).

Le stesse decisioni vanno riportate nella pagina «Leggimi» e in `../README.md` (Anomalie e decisioni).

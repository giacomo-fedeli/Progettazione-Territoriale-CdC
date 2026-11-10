# dati/ – sorgenti e tabelle del modello

| Cartella | Contenuto | Chi la modifica |
|---|---|---|
| `sorgenti/` | File forniti dal docente (DB PS_2022, codifiche). **Non modificare mai.** | nessuno |
| `dimensioni/` | Calendario e fasce, lookup codifiche, comuni ISTAT/popolazione, strutture, cittadinanze | il team |
| `elaborati/` | File preparati dal team fuori da Power BI (`fatti_ridotta`, `pazienti`, lookup e calendario modificati). Vedi [elaborati/README.md](elaborati/README.md) | il team |
| `criteri/` | `criteri_CdC.xlsx` – regole S2 (es. codice diagnosi → compatibile / non compatibile / non classificabile) | il team (S2) |
| `scenari/` | `assegnazione_comune_CdC.xlsx` (Comune, CdC, **Scenario**), `cdc_proposta.xlsx`, `cdc_DG.xlsx`, `parametri_capacita_costi.xlsx` | il team (S3/S4) |

Il parametro Power Query `PercorsoDati` punta a questa cartella.

## Data dictionary (S1)

| Campo | Significato | Tipo / note |
|---|---|---|
| codice_istituto | Struttura che registra l'accesso | testo, conservare gli zeri iniziali |
| id_pz | Paziente (può ricorrere in più episodi) | testo |
| … | … | … |

> Completare con tutti i campi usati (vedi `codifiche flusso.pdf`).

## Anomalie e decisioni

| # | Anomalia trovata | Righe coinvolte | Decisione | Perché |
|---|---|---|---|---|
| 1 | Accessi senza data/ora di dimissione | … | Esclusi dai tempi di permanenza, restano nei volumi | Richiesto dalla traccia |
| 2 | … | … | … | … |

## Numeri di controllo

| Controllo | Valore | Dove si verifica |
|---|---|---|
| Totale accessi | … | pagina Leggimi |
| Pazienti distinti | … | pagina Leggimi |
| Totale valore prestazioni (€) | … | pagina Leggimi |
| Accessi senza dimissione | … | pagina Leggimi |

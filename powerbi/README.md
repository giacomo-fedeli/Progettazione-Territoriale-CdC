# powerbi/ – il modello unico

Qui va **un solo** progetto Power BI in formato PBIP (`PW4.pbip`, `PW4.Report/`, `PW4.SemanticModel/`).
Cresce dalla sottoprova 1 alla 4; la pagina «Leggimi» si aggiorna a ogni sottoprova.

**Stato al 10/11/2026:** è il nuovo modello del team (prima `PoweBI_Base/PW4 2 (1).pbip`), rinominato in `PW4`.
Ha 17 tabelle (`Fact_PS_2022` + 16 dimensioni), 26 relazioni, **nessuna misura** e nessuna tabella `_Misure`.
I percorsi dei file passano tutti dal parametro `PercorsoDati` → cartella `dati\` del repo.
Le tabelle `LocalDateTable_*` e `DateTableTemplate_*` sono create in automatico da Power BI:
conviene disattivare *Opzioni → Caricamento dati → Data/ora automatica* e usare solo `Dim_Calendario`.

Per salvare in PBIP: *File → Salva con nome → Progetto Power BI (.pbip)*.

## Pagine richieste

| Pagina | Sottoprova | Contenuto (destinatario da scrivere nel sottotitolo) |
|---|---|---|
| Direzionale | S1 | Direzione Strategica – 4–6 KPI con confronto e lettura, andamento, vista territorio, solo filtro periodo |
| Flussi | S1 | Livello tattico – periodo, giorno, fascia oraria, anagrafica, triage, diagnosi, arrivo, esiti, prestazioni, codici bianchi + ticket €25 (triage in uscita) |
| Attese e code | S1 | Livello tattico – mediana e 90° percentile (min) per triage in ingresso e fascia; matrice giorno × ora dei pazienti presenti |
| Territorio | S1 | Livello tattico – accessi e valore per comune (ISTAT 6 cifre), mappa |
| Domanda potenziale | S2 | Domanda compatibile vs presa in carico, per mese e comune, con criteri e quota ipotizzata |
| Confronto | S4 | Proposta vs Direzione Generale sugli stessi KPI, scostamento, sensibilità 30/50/70% |
| Leggimi | tutte | Fonti, anomalie, decisioni, definizione dei KPI, numeri di controllo |

## Modello

- Star schema: fatto = accessi; dimensioni Calendario, Fasce orarie (7–14, 14–21, 21–7), Comuni, decodifiche (triage, arrivo, diagnosi, esito).
- Tabella dei criteri S2 e tabella di assegnazione comune → CdC con colonna «Scenario» (S4), lette da `../dati/`.
- Misure in una tabella dedicata (`_Misure`) con nomi comprensibili. Valore economico = `SUM`.

## Regole grafiche

Titolo su ogni visual, numeri formattati con unità, colore solo per evidenziare, niente 3D,
assi in ordine logico, lettura della pagina in ordine logico.

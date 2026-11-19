# 11 – Glossario

Sigle e termini usati nel progetto, in ordine alfabetico.

| Termine | Significato |
|---|---|
| **90° percentile (P90)** | Valore sotto il quale cade il 90% dei casi. «Attesa P90 = 203 minuti» significa che il 10% dei pazienti aspetta più di 203 minuti. Si usa insieme alla mediana |
| **Accesso** | Una visita al Pronto Soccorso: una riga della tabella dei fatti. Un paziente può avere più accessi |
| **Accessi deviati alle CdC** | Nel modello è la «domanda presa in carico»: quota dello scenario × accessi compatibili |
| **ACN** | Accordo collettivo nazionale dei medici di medicina generale. Fonte dei 38,72 €/ora |
| **AGENAS** | Agenzia nazionale per i servizi sanitari regionali |
| **ASST** | Azienda socio-sanitaria territoriale. Qui: ASST dei Sette Laghi (provincia di Varese) |
| **Attesa** | Tempo tra l'arrivo (accettazione) e la presa in carico, in minuti |
| **BAC** | *Budget at completion*: il budget totale del progetto (5.934 €) |
| **Bacino** | L'insieme dei comuni assegnati a una CdC |
| **Capacità** | Visite che una CdC può erogare in un anno: ore × medici × 3 visite/ora × 85% |
| **CdC** | Casa della Comunità: struttura territoriale con servizi sanitari e sociosanitari (DM 77/2022) |
| **Codice bianco / verde / giallo / rosso / nero** | Codici di triage, dalla minore alla maggiore gravità (bianco, verde, giallo, rosso); il nero indica il decesso. «Codici bianchi» si legge sul triage in **uscita** |
| **Compatibile / non compatibile / non classificabile** | Le tre classi della domanda potenziale ([06](06-domanda-potenziale-cdc.md)) |
| **CPI** | *Cost performance index* = EV ÷ AC. Sotto 1: si spende più di quanto si produce |
| **CV** | *Cost variance* = EV − AC |
| **DAX** | Linguaggio delle formule di Power BI |
| **Direzione Generale (DG)** | Chi ha definito la configurazione delle 10 CdC con cui confrontiamo la nostra rete (SP4) |
| **Direzione Strategica** | Destinatario del lavoro |
| **DM 77/2022** | Decreto ministeriale che definisce modelli e standard dell'assistenza territoriale: hub e spoke, orari, standard |
| **Domanda compatibile** | Accessi che *in teoria* una CdC potrebbe gestire (20.419) |
| **Domanda presa in carico** | La parte della domanda compatibile che le CdC riescono davvero ad assorbire: quota (ipotesi) × domanda compatibile |
| **EAC** | *Estimate at completion* = AC + (BAC − EV): costo finale previsto se il lavoro che resta costa quanto previsto |
| **Episodio** | Sinonimo di accesso nel flusso |
| **Erlang C** | Formula della probabilità di attendere in una coda M/M/c |
| **Esito** | Come finisce l'accesso: dimissione a domicilio, ricovero, trasferimento, abbandono… |
| **EV** | *Earned value* = Σ (% di completamento × budget) |
| **FTE** | *Full time equivalent*: un lavoratore a tempo pieno. Qui 1.500 ore all'anno |
| **Fact / tabella dei fatti** | La tabella centrale del modello: un accesso per riga |
| **Funnel / imbuto** | Sequenza di criteri che restringe gli accessi da 75.664 a 20.419 |
| **Hub** | CdC con bacino di almeno 40.000 abitanti, aperta h24 7 giorni su 7 (DM 77) |
| **HiGHS** | Solutore di programmazione lineare intera usato dal notebook SP3 |
| **ICD-9-CM** | Classificazione internazionale delle diagnosi usata nel flusso |
| **ISTAT (codice a 6 cifre)** | Codice del comune; collega gli accessi ai comuni e alla popolazione |
| **KPI** | *Key performance indicator*: numero che risponde a una domanda della Direzione |
| **λ, μ, ρ, Wq** | Arrivi per ora, pazienti visti per ora da un medico, utilizzo dei medici, attesa media in coda ([04](04-kpi-e-misure.md), sezione 4) |
| **M/M/c** | Coda con arrivi casuali, tempi di visita casuali e `c` serventi (qui i medici) |
| **Mediana** | Il valore centrale: metà dei casi sta sotto, metà sopra |
| **Misura** | Formula DAX che calcola un numero al volo, secondo i filtri della pagina |
| **PBIP** | Formato di progetto Power BI fatto di file di testo, adatto a Git |
| **p-median** | Modello di localizzazione: sceglie `k` sedi che minimizzano la somma domanda × distanza |
| **Permanenza** | Tempo tra l'arrivo e la dimissione, in minuti |
| **Presa in carico (prcar)** | Il momento in cui il paziente è visto da un professionista |
| **Power Query** | Strumento di Power BI per caricare e trasformare i dati |
| **Proposta** | La rete di 6 CdC ideata dal gruppo (SP3) |
| **PS** | Pronto Soccorso |
| **PV** | *Planned value*: valore pianificato alla data di stato |
| **Quota presa in carico** | Ipotesi (30, 50, 70%) sulla parte dei compatibili che le CdC assorbirebbero |
| **Scenario** | Nel modello SP3: «Proposta» o «Direzione Generale». Nella domanda potenziale: una quota di presa in carico |
| **Spoke** | CdC più piccola, aperta 8–20, 6 giorni su 7 (DM 77: h12 6/7) |
| **SP0 … SP4** | Sottoprove: pianificazione, flussi e bisogni, domanda potenziale, rete CdC, confronto |
| **SPI** | *Schedule performance index* = EV ÷ PV. Sotto 1: si è in ritardo |
| **SV** | *Schedule variance* = EV − PV |
| **Star schema (stella)** | Modello con una tabella dei fatti al centro e tabelle di dimensione intorno |
| **Territorio (del progetto)** | I 107 comuni con almeno 50 accessi ogni 1.000 abitanti ai nostri PS |
| **Ticket** | Compartecipazione alla spesa: 25 € per i codici bianchi in uscita. La stima è distinta dal registrato |
| **Triage** | Valutazione della gravità all'arrivo (ingresso) e a fine percorso (uscita) |
| **Turno (M, P, N)** | Mattina 7–14, pomeriggio 14–21, notte 21–7 |
| **WBS** | *Work breakdown structure*: scomposizione del progetto in fasi, deliverable e attività |

**Torna all'[indice](README.md).**

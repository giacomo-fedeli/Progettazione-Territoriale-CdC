# 04 – Definizione dei KPI e delle misure

Questo documento spiega **ogni KPI della dashboard in parole semplici**: cosa risponde, come si calcola, in che unità, come si legge.
La formula DAX esatta di ogni misura è nel [catalogo delle misure](04b-catalogo-misure.md) (generato dal modello).

I numeri sono quelli del report `PW4 15` sul periodo intero (01/01–30/06/2022) e senza filtri, verificati il 18/11/2026.

---

## 1. Regole che valgono per tutti i KPI

| Regola | Significato |
|---|---|
| **Periodo** | Il solo filtro della Direzionale è il periodo (mesi). I dati coprono 181 giorni, dal 01/01/2022 al 30/06/2022 |
| **Un accesso = una riga** | `Accessi` = `COUNTROWS(Fact_PS_2022)`. Un paziente può avere più accessi |
| **Tempi in minuti** | Le durate sono frazioni di giorno nel modello; le misure moltiplicano per 1.440 e arrotondano |
| **Mediana e 90° percentile, mai la media** | La traccia non accetta la media da sola. Il 90° percentile (`PERCENTILE.INC`, 0,9) dice quanto aspetta il 10% che aspetta di più |
| **Mese di riferimento** | È l'ultimo mese con dati nel periodo scelto (giugno se il periodo è intero). Il confronto è con il mese prima (maggio) |
| **Banda di stabilità ±2%** | Variazione relativa tra −2% e +2%: «● stabile». Oltre: «▲ in aumento» o «▼ in calo». Per attese, permanenza e codici bianchi l'aumento è rosso e il calo è verde; per accessi e valore il colore è neutro |
| **Codici bianchi** | Si leggono sul **triage in uscita** (traccia), non su quello in ingresso |
| **Valore = tariffa** | `Valore €` è la valorizzazione tariffaria delle prestazioni: **non** è un costo né un ricavo |
| **Un KPI per pagina, massimo 6** | Un KPI non si ripete in due pagine. Se un tema torna, torna con un'altra misura dello stesso studio (per giorno, per paziente, per 1.000 abitanti, solo bianchi e verdi) |
| **Anomalie** | I codici vuoti o anomali restano nei KPI; sono nascosti solo nei grafici per categoria ([03](03-anomalie-e-decisioni.md)) |

---

## 2. Dalla domanda al KPI (pagina Direzionale)

La traccia chiede una riga per ciascuno dei 4–6 KPI della pagina Direzionale: parte della domanda, formula, unità, lettura e azione.

Le tre domande della Direzione Strategica:
- **D1** – Come sono distribuiti sul territorio i bisogni oggi intercettati dai servizi ospedalieri?
- **D2** – Quale quota potrebbe essere gestita dalle Case della Comunità?
- **D3** – Come dovrebbe essere configurata una rete territoriale e come si confronta con quella della Direzione Generale?

Nella pagina Direzionale ogni KPI mostra: il valore del periodo, la variazione dell'ultimo mese rispetto al precedente e l'andamento mensile.

| KPI | Parte della domanda | Formula | Unità | Valore (gen–giu) | Lettura | Azione proposta |
|---|---|---|---|---:|---|---|
| **Accessi al PS** | D1 – quanto è grande la domanda | Numero di accessi (righe della fact) | accessi | **75.664** (418 al giorno) | Giugno 13.889 contro maggio 14.242: −2,5% (▼). Media mensile 12.611 | Se sale oltre +2% per due mesi: controllare i turni dei PS più carichi (il Circolo di Varese ha il 31% degli accessi) |
| **Codici bianchi in uscita** | D1 e D2 – quanta domanda è non urgente | Accessi con triage in **uscita** bianco ÷ tutti gli accessi | % | **7,0%** (5.304) | Giugno 7,07% contro maggio 7,36%: −3,9% (▼, verde) | Se sale: rafforzare l'orientamento verso servizi alternativi. È il KPI più vicino al target delle CdC |
| **Attesa mediana** | D1 – quanto aspetta il paziente | **Mediana** di (data-ora presa in carico − data-ora arrivo) | minuti | **37** | Giugno 37 contro maggio 37: stabile (●). Il 90° percentile è 203 minuti | Se sale oltre +2%: aprire «Attese e code» per vedere quale PS e quale fascia oraria |
| **Permanenza 90° percentile** | D1 – la coda lunga | **90° percentile** di (data-ora dimissione − data-ora arrivo); gli accessi senza dimissione sono esclusi | minuti | **1.049** (17 h 29 min) | Giugno 996 contro maggio 1.005: −0,9% (●). La mediana è 178 minuti | Se sale: guardare le permanenze oltre 24 ore (4.845 accessi) e i ricoveri |
| **Valore prestazioni** | D1 – peso economico della domanda | Somma di `Valore_economico_prestazioni_PS` | milioni di € | **9,84 M€** | Giugno 1,79 M€ contro maggio 1,83 M€: −2,1% (▼) | È una tariffa, non un costo. Se cresce più degli accessi: più prestazioni per accesso (vedi Flussi) |
| **% accessi compatibili CdC** | D2 – quota gestibile dalle CdC | Accessi «potenzialmente compatibili» ÷ tutti gli accessi | % | **27,0%** (20.419) | Giugno 27,2% contro maggio 27,6%: −1,3% (●) | Se sale: il bacino delle CdC cresce, passare a «Domanda potenziale». Con il filtro «Solo compatibili» acceso vale 100% per costruzione |

> **Nota.** La colonna «Lettura» riporta le regole **già nel report** (banda ±2% e confronto con il mese precedente). La colonna «Azione proposta» è una proposta di lettura per la Direzione: le soglie vere del report sono solo quelle della colonna «Lettura».
> Il confronto con la media dell'anno (media mensile 12.611 accessi) è nel sottotitolo del KPI «Accessi».

Come si verifica ogni valore: `Accessi` (misura), `% codici bianchi`, `Attesa mediana (min)`, `Permanenza P90 (min)`, `Valore €`, `% Accessi Compatibili CdC` nel [catalogo](04b-catalogo-misure.md). Le variazioni vengono dalle misure della cartella *4 Confronti* (`Var % accessi`, `Var % valore`, …).

---

## 3. Gli altri KPI, pagina per pagina

### Flussi (livello tattico)

| KPI | Formula | Unità | Valore | Come si legge |
|---|---|---|---:|---|
| Accessi al giorno | Accessi ÷ giorni con dati | accessi/giorno | 418,0 | Sale da 345 (inizio semestre) a 463 (media mobile a 7 giorni) |
| Accessi per paziente | Accessi ÷ pazienti distinti | accessi/paziente | 1,30 | Il 79% dei pazienti (46.056) viene una sola volta; il 21% (12.264) torna e produce il 39% degli accessi; massimo 39 accessi per un paziente |
| Arrivi con mezzi propri | Accessi con arrivo «Autonomo» ÷ accessi con arrivo **noto** | % | 80,6% | Esclusi gli arrivi «Non rilevato». Chi arriva da solo può scegliere una CdC |
| Prestazioni per accesso | Prestazioni ÷ accessi | prestazioni | 11,4 | 860.628 prestazioni in totale |
| Valore medio per accesso | Valore € ÷ accessi | € | 130,1 | Tariffa media, non costo |
| Ticket stimato − registrato | Bianchi in uscita × 25 € − ticket registrato nel flusso | € | 80.750 € | Stima 132.600 € contro registrato 51.850 € ([03](03-anomalie-e-decisioni.md), punto 10). Compartecipazione, non costo del servizio |

### Attese e code (livello tattico)

| KPI | Formula | Unità | Valore |
|---|---|---|---:|
| Attesa 90° percentile | 90° percentile di (presa in carico − arrivo) | minuti | 203 |
| Attesa mediana bianchi e verdi | Mediana dell'attesa dei soli accessi con triage in **ingresso** V o B | minuti | 47 (contro 37 di tutti i codici) |
| Permanenza mediana | Mediana di (dimissione − arrivo) | minuti | 178 |
| Permanenza mediana bianchi e verdi | Come sopra, solo V e B in ingresso | minuti | 152 |

**Altre misure della pagina.**
- `% attesa oltre 1 ora` = accessi con attesa > 60 minuti ÷ accessi con il dato → **36,6%**.
- `% permanenza oltre 6 ore` = accessi con permanenza > 360 minuti ÷ accessi con dimissione → **25,6%**.
- Le soglie di 1 e 6 ore sono scelte dal gruppo per leggibilità, **non** sono norma.
- Matrice **pazienti presenti**: media dei pazienti presenti per giorno della settimana × ora; regola nel [05](05-modello-dati.md).

### Territorio (livello tattico)

| KPI | Formula | Unità | Valore |
|---|---|---|---:|
| Comuni con accessi | Comuni di residenza distinti con almeno un accesso | comuni | 1.379 |
| Accessi ogni 1.000 ab. (prov. Varese) | Accessi dei residenti in provincia di Varese ÷ abitanti della provincia × 1.000 (ISTAT 2022) | accessi/1.000 ab. | 73,7 |
| Quota primi 10 comuni | Accessi dei 10 comuni con più accessi ÷ accessi totali | % | 33,5% |
| Accessi da fuori provincia | Accessi di residenti fuori dalla provincia di Varese (estero compreso) ÷ accessi con residenza nota | % | 14,4% |

La popolazione di un comune è contata **una volta sola** anche se il comune ha più codici ISTAT (comuni fusi).

### Domanda potenziale (SP2)

| KPI | Formula | Unità | Valore |
|---|---|---|---:|
| Accessi compatibili CdC | Accessi con `Classificazione3_CdC` = «Potenzialmente compatibile» | accessi | 20.419 |
| Valore compatibili CdC | Somma del valore delle prestazioni dei compatibili | € | 1.521.047 € |
| % valore compatibile | Valore dei compatibili ÷ valore totale | % | 15,5% |
| Quota presa in carico (ipotesi) | Quota dello scenario scelto | % | 50% (scenario base) |
| **Domanda presa in carico** | Quota × accessi compatibili (+ 30% dei non classificabili solo nello scenario 5) | accessi | 10.209,5 (scenario base) |

Sottopagina «Classi e distribuzione»: non classificabili **1.245**; non compatibili **54.000**; presa in carico dello scenario scelto.

### Rete CdC (SP3) – quota base 50%

| KPI | Formula | Unità | Valore (Proposta) |
|---|---|---|---:|
| CdC proposte | Numero di sedi della rete | CdC | 6 (di cui 4 hub) |
| Visite gestite all'anno | Per ogni CdC: minimo tra presa in carico e capacità; somma | visite/anno | 15.310 |
| Accessi PS in meno | Visite gestite ÷ accessi PS annui (152.564) | % | 10,0% |
| Km medi alla CdC | Media dei km stradali stimati, pesata per la domanda | km | 4,97 |
| Domanda entro 10 km | Quota di domanda a meno di 10 km dalla sua CdC | % | 93,2% |
| Costo annuo | Medici a ore + infermieri e amministrativi a FTE + sede | M€/anno | 3,86 |

Misure di appoggio: `SP3 Presa in carico` (accessi compatibili annui in orario × quota), `SP3 Capacita` (ore × medici × 3 visite/ora × 85%), `SP3 Costo per visita` (252 €), `SP3 Valore PS non erogato` (tariffa delle visite gestite: 1,14 M€, **non** è un risparmio).

### Confronto (SP4): scostamento Proposta − Direzione Generale

| KPI | Proposta | Direzione Generale | Scostamento (Proposta − DG) |
|---|---:|---:|---:|
| CdC | 6 | 10 | −4 |
| Km medi | 4,97 | 3,97 | +1,00 |
| Domanda entro 10 km | 93,2% | 99,3% | −6,1 punti |
| Visite gestite all'anno | 15.310 | 13.967 | +1.343 |
| Accessi PS in meno | 10,0% | 9,2% | +0,9 punti |
| Costo annuo | 3,86 M€ | 5,27 M€ | −1,41 M€ |
| Costo per visita | 252 € | 378 € | −125 € |

Lo scostamento è **Proposta − Direzione Generale**, come chiede la traccia (punto D). Misure: cartella *SP4 Confronto*.

---

## 4. Studio delle code (facoltativo, SP1)

Modello **M/M/c** (formula di Erlang C): arrivi di Poisson, tempi di visita esponenziali, `c` medici in parallelo. Si applica a ogni turno di ogni PS (21 casi).

| Simbolo | Misura | Definizione |
|---|---|---|
| λ | `Lambda (pz/ora)` | Accessi ÷ (giorni × ore del turno); turni: M 7 h, P 7 h, N 10 h |
| μ | `Mu (pz/ora per medico)` | 60 ÷ tempo di visita (default 20 minuti → 3 pazienti/ora) |
| c | `Medici scenario` | Medici del turno (tabella del personale) + medici aggiuntivi (parametro 0–3) |
| ρ | `Rho` | λ ÷ (c × μ): utilizzo dei medici. Con ρ ≥ 1 la coda non si stabilizza («Instabile») |
| Wq | `Wq modello (min)` | Attesa media in coda del modello. Vuota se ρ ≥ 1 |
| Medici minimi | `Medici minimi` | Il più piccolo c con Wq ≤ soglia (parametro 5–60 minuti, default 15) |
| Turno critico | `Turni critici prima` / `dopo CdC` | ρ ≥ 1 oppure Wq sopra la soglia |

**Risultato** (tempo di visita 20 minuti, soglia 15 minuti, medici aggiuntivi 0): turni critici **8 su 21** oggi. Dopo la deviazione verso le CdC restano 8 con quota 30% e 50%; scendono a 6 con 70% e a 5 con 100%.

**Limiti:** il modello **non è calibrato** sulle attese osservate; usa solo sei mesi di dati; sono stime teoriche, non effetti causali. L'organico dei due PS Del Ponte (ostetrico-ginecologico e pediatrico) è indicato dalla traccia come una sola riga: il file lo assegna a entrambi (vedi [10](10-limiti-e-riproducibilita.md)).

---

## 5. Numeri di controllo (pagina Leggimi)

Misure della cartella *8 Controlli (Leggimi)*: ignorano tutti i filtri, quindi sono sempre uguali.

| Controllo | Misura | Valore | Come si verifica indipendentemente |
|---|---|---:|---|
| Accessi totali | `Controllo accessi totali` | **75.664** | Righe del foglio `PS_2022` di `01_DB_Excel_PS_2022.xlsx` |
| Pazienti distinti | `Controllo pazienti distinti` | **58.320** | Valori distinti di `id_pz` |
| Valore totale | `Controllo valore totale €` | **9.840.639,33 €** | Somma di `Valore_economico_prestazioni_PS` |
| Accessi senza dimissione | `Controllo accessi senza dimissione` | **1.526** | Righe con `data_dim` vuota |
| Codici bianchi in uscita | `Controllo codici bianchi` | **5.304** | Righe con `triage_uscita = "B"` |

I cinque valori sono stati ricalcolati con Python dal file originale e coincidono con il modello.

---

## 6. Come sono costruite le card KPI

Ogni card KPI è un'immagine SVG disegnata da una misura DAX (numero grande, freccia di variazione, linea mensile). Sono le **136 misure di presentazione** del modello: non calcolano numeri di business, mostrano il valore di una misura di calcolo.
Esempio: `KPI Direzionale accessi valore` mostra il valore di `Accessi`; `KPI Direzionale accessi freccia` il segno di `Var % accessi`.

Ogni pagina ha sei card al massimo (Attese e code ne ha quattro, Territorio quattro, Domanda quattro). La linea mensile ignora il filtro del periodo e rispetta gli altri filtri.

**Torna all'[indice](README.md).**

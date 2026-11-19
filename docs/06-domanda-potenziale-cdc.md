# 06 – Domanda potenziale per le Case della Comunità (SP2)

Questo documento spiega **come abbiamo deciso quali accessi al PS potrebbero essere gestiti da una Casa della Comunità (CdC)**, con quali criteri, con quali numeri e con quali limiti.

**Metodo in una riga:** *un dato, una fonte, un metodo.*
- **Dato:** gli accessi ai 7 PS (75.664).
- **Fonte:** la colonna calcolata `Fact_PS_2022[Classificazione3_CdC]`.
- **Metodo:** un solo imbuto di criteri, che divide gli accessi in tre classi.

**Risultato:** 20.419 accessi potenzialmente compatibili (**27,0%**), 1.245 non classificabili (1,6%), 54.000 non compatibili (71,4%).

---

## 1. Cosa chiede la traccia

- Definire i **criteri** di inclusione ed esclusione, con fonti normative, scientifiche o istituzionali.
- Tradurli in **regole** sulle variabili del database, replicabili.
- Distinguere tre classi: **potenzialmente compatibile**, **non compatibile**, **non classificabile**.
- Non considerare «automaticamente soddisfatte» le condizioni per cui mancano informazioni.
- Fare la classificazione **dentro il modello Power BI**, in una tabella collegata o in una colonna calcolata, non a mano.
- Due misure distinte: **domanda compatibile** e **domanda presa in carico** (la parte che le CdC riescono davvero ad assorbire, con una quota dichiarata come ipotesi).
- Una pagina «Domanda potenziale» con le due misure per mese e per comune.

---

## 2. Servizi assunti per le CdC e criteri di esclusione

Dal documento del corso *Case della Comunità e domanda potenziale* (par. 3), la rete territoriale offre:
- valutazioni di medicina generale per bisogni **non urgenti e a bassa complessità**;
- assistenza infermieristica ambulatoriale (medicazioni semplici non traumatiche, controlli);
- controlli e monitoraggio di condizioni croniche stabili;
- prestazioni di base programmate (prelievi, ECG) in percorsi non urgenti.

Sono **esclusi** gli accessi per: trauma o ustione; coma, shock o sindrome neurologica acuta; dolore toracico, dispnea acuta o altri quadri urgenti; complicanze di gravidanza, parto e puerperio; emergenze psichiatriche o intossicazioni acute; procedure di emergenza, rianimazione, chirurgia urgente o diagnostica avanzata.

Riferimenti del documento: DM 77/2022, linee di indirizzo AGENAS 2024, indicatore AGENAS di accessi potenzialmente evitabili (2025). Vedi [02 – Fonti](02-fonti.md).

---

## 3. Dai criteri alle regole

Ogni criterio diventa una colonna booleana `Compatibile_CdC` in una tabella di decodifica (o una colonna della fact). La colonna vale TRUE, FALSE oppure **vuota** (= informazione mancante).

| # | Criterio | Perché | Variabile del DB | Regola | Dove sta nel modello |
|---|---|---|---|---|---|
| 1 | **Diagnosi principale** compatibile | Esclude trauma, ustione, quadri neurologici acuti, dolore toracico, gravidanza e parto, psichiatria, intossicazioni (documento par. 3) | `diagn_pr` (ICD-9-CM, 16.228 codici) | Ogni codice prende la regola del **prefisso più lungo** che combacia. Logica permissiva: TRUE di default, FALSE solo per i casi esclusi. **8.518 TRUE, 7.710 FALSE** | `DIm_Diagnosi_Primaria[Compatibile_CdC]` |
| 2 | **Triage in ingresso** verde o bianco | Bassa priorità all'arrivo: bisogni non urgenti | `triage_ingresso` | V, B = TRUE; R, G, N, ND = FALSE | `Dim_Triage_Ingresso[Compatibile_CdC]` |
| 3 | **Triage in uscita** verde o bianco | Bassa gravità a fine percorso (conferma la bassa complessità) | `triage_uscita` | V, B = TRUE; R, G, N, ND = FALSE | `Dim_Triage_Uscita[Compatibile_CdC]` |
| 4 | **Esito** compatibile | Il paziente non ha avuto bisogno di ricovero, osservazione o trasferimento | `esito_tratt` | TRUE: 1 dimissione a domicilio, 6 abbandono pre-visita, 7 abbandono in accertamenti, 8 dimissione ambulatoriale. FALSE: 0 ricovero OBI, 2 ricovero, 3 trasferimento, 4 deceduto in PS, 5 rifiuta ricovero, 9 giunto cadavere | `Dim_Esito_Trattamento[Compatibile_CdC]` |
| 5 | **Durata** presa in carico → dimissione **≤ 2 ore** | Una visita breve è un indizio di bassa complessità: serve a escludere i percorsi con molti accertamenti | `ora_prcar`, `ora_dim` | TRUE se ≤ 2 ore; vuoto se manca la dimissione | `Fact_PS_2022[Compatibile_CdC_Durata_Prestazione]` |
| 6 | **Diagnosi secondaria** compatibile, se presente | La secondaria può rivelare un quadro più complesso | `diagn_sec` | Conta solo se presente. Una secondaria vuota **non** rende l'accesso non classificabile | `DIm_Diagnosi_Secondaria[Compatibile_CdC]` |

> **Ipotesi dichiarate.** Il criterio 5 (soglia di 2 ore) è una **scelta del gruppo**, non una norma. I criteri 2 e 3 usano il triage come indicatore di gravità: è un'approssimazione.

### Criteri che **non** si possono verificare con i dati

La traccia vuole che siano esplicitati. Il database **non** contiene:
- stabilità clinica e cronicità (per esempio «condizione cronica stabile»);
- se il paziente ha un medico di famiglia o un percorso di cura già attivo;
- l'esistenza e l'orario di una CdC vicina al momento dell'accesso (nel 2022 le CdC non c'erano);
- se la prestazione fosse davvero erogabile in una CdC (per esempio ECG o prelievi): lo stimiamo solo con la diagnosi.

Questi criteri **non sono dati per soddisfatti**: l'imbuto usa solo informazioni presenti. Per questo la domanda compatibile è «**potenziale**» e va letta come una **stima teorica**.

---

## 4. La regola di classificazione

Per ogni accesso, in ordine:

1. Se **almeno un criterio è FALSE** → **Non compatibile**.
2. Altrimenti, se **almeno un criterio è vuoto** → **Non classificabile**.
3. Altrimenti (tutti TRUE, oppure secondaria assente) → **Potenzialmente compatibile**.

Una condizione **falsa vince** su una condizione mancante: se so già che il triage è giallo, non importa che la diagnosi manchi.

Codice (colonna calcolata `Fact_PS_2022[Classificazione3_CdC]`):

```dax
VAR dgP = RELATED ( DIm_Diagnosi_Primaria[Compatibile_CdC] )
VAR trU = RELATED ( Dim_Triage_Uscita[Compatibile_CdC] )
VAR trI = RELATED ( Dim_Triage_Ingresso[Compatibile_CdC] )
VAR es  = RELATED ( Dim_Esito_Trattamento[Compatibile_CdC] )
VAR du  = Fact_PS_2022[Compatibile_CdC_Durata_Prestazione]
VAR secPresente = NOT ISBLANK ( Fact_PS_2022[FK_Codice_Diagnosi_Secondaria] )
VAR dgS = RELATED ( DIm_Diagnosi_Secondaria[Compatibile_CdC] )
VAR haFalse =
    ( NOT ISBLANK ( dgP ) && dgP = FALSE () )
    || ( NOT ISBLANK ( trU ) && trU = FALSE () )
    || ( NOT ISBLANK ( trI ) && trI = FALSE () )
    || ( NOT ISBLANK ( es ) && es = FALSE () )
    || ( NOT ISBLANK ( du ) && du = FALSE () )
    || ( secPresente && NOT ISBLANK ( dgS ) && dgS = FALSE () )
VAR haVuoto =
    ISBLANK ( dgP ) || ISBLANK ( trU ) || ISBLANK ( trI ) || ISBLANK ( es ) || ISBLANK ( du )
    || ( secPresente && ISBLANK ( dgS ) )
RETURN
    SWITCH (
        TRUE (),
        haFalse, "Non compatibile",
        haVuoto, "Non classificabile",
        "Potenzialmente compatibile"
    )
```

Le viste derivate: `Episodio_Compatibile_CdC` (TRUE/FALSE) e `Filtro CdC` (testo per il pulsante on/off) usano la stessa colonna: non sono metodi diversi.

---

## 5. Risultati

### 5.1 L'imbuto passo per passo

Ogni passo aggiunge un criterio (misure `FNL Step 0…7`; il funnel nella pagina «Domanda potenziale»).

| Passo | Criterio aggiunto | Accessi che restano | Esclusi dal passo |
|---|---|---:|---:|
| 0 | Tutti gli accessi | 75.664 | – |
| 1 | Triage in ingresso verde o bianco | 59.460 | 16.204 |
| 2 | + diagnosi primaria compatibile | 34.086 | 25.374 |
| 3 | + esito compatibile | 31.568 | 2.518 |
| 4 | + durata presa in carico → dimissione ≤ 2 ore | 20.540 | 11.028 |
| 5 | + triage in uscita verde o bianco | 20.538 | 2 |
| 6 | + diagnosi secondaria compatibile (se presente) | **20.419** | 119 |
| 7 | Episodio compatibile (= passo 6) | **20.419** | 0 |

Lettura: **la diagnosi è il filtro più selettivo** (esclude 25.374 accessi). Il risultato finale non dipende dall'ordine dei passi: ogni criterio è un «E». L'ordine serve solo a mostrare dove si perde la domanda.

Nota di continuità: fino al 16/11 esistevano due regole (una «larga» e una «stretta») e una classificazione dei verdi in tre classi. La regola «larga» corrispondeva al passo 5 (20.538); con la diagnosi secondaria è diventata 20.419. Il 17/11 il gruppo ha scelto **un solo metodo** e ha eliminato gli altri.

### 5.2 Le tre classi

| Classe | Accessi | % sul totale | Valore prestazioni |
|---|---:|---:|---:|
| Potenzialmente compatibile | **20.419** | 27,0% | 1.521.047 € (15,5%) |
| Non classificabile | **1.245** | 1,6% | 103.435 € |
| Non compatibile | **54.000** | 71,4% | 8.216.158 € |
| **Totale** | 75.664 | 100% | 9.840.639 € |

**Perché 1.245 non classificabili.** Il dato che manca (le cifre si sovrappongono):
- diagnosi principale assente o non nel codebook: **1.192**;
- durata presa in carico → dimissione non calcolabile (manca la dimissione): **1.152**;
- triage in ingresso e in uscita vuoti: **39**;
- diagnosi secondaria presente ma non nel codebook: **14**.

Gli accessi non classificabili **non** sono contati come compatibili. Solo lo **scenario 5** ne prende il 30%, come ipotesi esplicita.

### 5.3 Chi sono gli accessi compatibili

Tutti i valori sono ricalcolati con misure del modello.

| Caratteristica | Compatibili | Non compatibili | Commento |
|---|---|---|---|
| Attesa mediana (arrivo → presa in carico) | **44 min** | 34 min | I compatibili aspettano **di più**: il triage dà la precedenza ai casi gravi |
| Permanenza mediana | 101 min | 233 min | Sono casi più brevi |
| Arrivo con mezzi propri | 91,6% | 76,5% | Nei compatibili quasi tutti arrivano da soli |

**Per età** (quota di accessi compatibili): 0–14 anni **37,3%** · 15–44 **27,4%** · 45–64 **28,2%** · 65–74 **24,4%** · 75–84 **19,3%** · 85+ **13,1%**. I bambini sono il gruppo più «compatibile»; gli anziani il meno.

**Per tipo di giorno:** feriale 26,8% · sabato 27,4% · domenica/festivo 27,5%. La quota è **la stessa in tutti i giorni**: non è solo un problema del weekend con il medico di famiglia chiuso.

**Per turno di arrivo:** mattina (7–14) 27,9% · pomeriggio (14–21) 26,2% · notte (21–7) 26,6%.

**Per mese:** gennaio 26,3% → giugno 27,2% (maggio 27,6%).

**Per Pronto Soccorso:**

| PS | Accessi | % compatibili | Attesa mediana |
|---|---:|---:|---:|
| Varese – Circolo | 23.705 | 19,4% | 62 min |
| Tradate – Galmarini | 16.398 | 31,0% | 34 min |
| Cittiglio – Luvini | 10.851 | 36,0% | 29 min |
| Varese – Pediatrico Del Ponte | 8.009 | 33,8% | 31 min |
| Luino – Onfalonieri | 6.346 | 21,2% | 37 min |
| Varese – Ostetrico-ginecologico Del Ponte | 5.221 | 26,4% | 19 min |
| Angera – Ondoli | 5.134 | 27,4% | 26 min |

Il **Circolo di Varese** ha la quota di compatibili più bassa (riceve i casi più gravi) ma l'attesa mediana più alta: il problema non è «quanti sono», è **dove vanno**.

**Per comune di residenza** (compatibili in valore assoluto): Varese 2.574 · Tradate 757 · Luino 615 · Malnate 586 · Besozzo 397 · Gavirate 390 · Laveno-Mombello 352 · Sesto Calende 329. (Pagina «Domanda potenziale» e sottopagina «Classi e distribuzione»: tabella e mappa dei comuni.)

---

## 6. Domanda compatibile e domanda presa in carico

La traccia vuole le due cose **distinte**:

| Misura | Cosa è | Valore |
|---|---|---:|
| **Domanda compatibile** = `Accessi compatibili CdC` | Quelli che *in teoria* una CdC potrebbe gestire | 20.419 |
| **Domanda presa in carico** = `Accessi deviati alle CdC` | La parte che le CdC *riescono davvero* ad assorbire = quota dello scenario × accessi compatibili | 10.209,5 con quota 50% |

La quota è un'**ipotesi dichiarata** e si sceglie con lo slicer «Scenario CdC». La tabella `Scenario CdC` ha sei scenari. I risultati sono **stime teoriche, non effetti causali** (la traccia lo richiede).

| Scenario | Quota | Accessi deviati | Riduzione accessi PS |
|---|---:|---:|---:|
| 0 · Oggi | 0% | 0 | 0,0% |
| 1 · Prudente | 30% | 6.126 | 8,1% |
| 2 · **Base** | **50%** | **10.210** | **13,5%** |
| 3 · Ottimistico | 70% | 14.293 | 18,9% |
| 4 · Massimo teorico | 100% | 20.419 | 27,0% |
| 5 · Ampio | 70% dei compatibili + 30% dei non classificabili | 14.667 | 19,4% |

La riduzione del 13,5% qui è **teorica**: conta tutti i compatibili, a tutte le ore. La rete di 6 CdC dell'SP3 ne gestisce meno (10,0%) perché considera solo il territorio, gli orari delle spoke e la capacità: vedi [07](07-rete-cdc-e-confronto.md).

### Perché la quota base è il 50%

È un'ipotesi della traccia, ma la **verifichiamo sui dati**. Sui 20.419 compatibili (funnel «Perché la quota base è il 50%», misura `Quota CdC base dati`):

| Passo | Accessi | Quota |
|---|---:|---:|
| Potenzialmente compatibili | 20.419 | 100% |
| … che **decidono da soli** (responsabile dell'invio = «Decisione propria») **e arrivano con mezzi propri** | 16.545 | **81,0%** |
| … e arrivano **dal lunedì al sabato, 8–20, non festivi** (quando è aperta anche una CdC spoke) | 10.182 | **49,9%** |

Quindi la quota base del 50% **non è un numero a caso**: è circa la parte dei compatibili che sceglie da sola e arriva negli orari di una CdC spoke.
- **30% (prudente):** nella realtà i servizi territoriali tolgono meno del teorico (vedi letteratura in [02](02-fonti.md), punto 4.5).
- **70% (ottimistico):** vicino al tetto dell'81% di chi si muove da solo.

---

## 7. Dove si trova tutto nel modello

| Cosa | Dove |
|---|---|
| Criteri (colonne `Compatibile_CdC`) | `DIm_Diagnosi_Primaria`, `DIm_Diagnosi_Secondaria`, `Dim_Triage_Ingresso`, `Dim_Triage_Uscita`, `Dim_Esito_Trattamento`, `Fact_PS_2022[Compatibile_CdC_Durata_Prestazione]` |
| Classificazione | `Fact_PS_2022[Classificazione3_CdC]` |
| Misure | `Accessi compatibili CdC`, `Accessi non classificabili CdC`, `Accessi non compatibili CdC`, `Accessi deviati alle CdC`, `Quota CdC compatibili`, funnel `FNL Step 0…7` ([catalogo](04b-catalogo-misure.md), sezioni F e G) |
| Pagine | «Domanda potenziale» e sottopagina «Classi e distribuzione» |
| Controllo | La somma delle tre classi fa 75.664 |

## 8. Limiti

- **Teorico, non causale.** Una diagnosi compatibile non dice che il paziente *sarebbe andato* in CdC.
- **Solo il primo semestre 2022**, quando le CdC non esistevano: non c'è domanda latente (chi non è andato in PS).
- **La soglia di 2 ore** e **l'uso del triage come indicatore** sono scelte del gruppo.
- **Le regole sulla diagnosi** (prefisso più lungo, permissive) sono un'interpretazione clinica semplice: non sono state validate da un clinico.
- **Un codice diagnosi non presente nel codebook** (63 accessi COVID `04331`/`04332`) lascia il criterio vuoto: l'accesso diventa «non classificabile» se nessun altro criterio è falso.
- **Dipendenza dai file del compagno:** le colonne `Compatibile_CdC` delle tabelle triage, esito e diagnosi arrivano da file preparati da Shah (non tutti sono nel repository, vedi [10](10-limiti-e-riproducibilita.md)).

**Torna all'[indice](README.md).**

# 08 – La dashboard: pagine, grafici e come si naviga

La traccia chiede **quattro pagine più il «Leggimi»**: Direzionale (livello strategico) e Flussi, Attese e code, Territorio (livello tattico). Il gruppo ha aggiunto le pagine delle sottoprove 2, 3 e 4. Il sottotitolo di ogni pagina indica il destinatario.

Report di riferimento: **`PW4 15.pbip`**, 1920×1080 (16:9). Le pagine sono 26: 9 nel menu, 8 sottopagine nascoste, 7 bozze nascoste, 2 tooltip.

---

## 1. Mappa delle pagine

| Pagina (menu) | Livello / destinatario | Sottoprova | Sottopagine (nascoste, si aprono con i pulsanti →) |
|---|---|---|---|
| **Home** | Copertina | – | – |
| **Direzionale** | Strategico – Direzione Strategica | SP1 | – |
| **Flussi** | Tattico – chi organizza i servizi del PS | SP1 | Confronto tra PS · Approfondimento episodi |
| **Attese e code** | Tattico – chi organizza risorse del PS | SP1 | Personale e coda |
| **Territorio** | Tattico – chi organizza i servizi sul territorio | SP1 | – |
| **Domanda potenziale** | Direzione Strategica | SP2 | Classi e distribuzione |
| **Rete CdC** | Direzione Strategica | SP3 | – |
| **Confronto** | Direzione Strategica | SP4 | Scenari e dettaglio · Impatto sul Pronto Soccorso |
| **Leggimi** | Tutti | metodo | Imbuto CdC e code · Rete CdC (SP3 e SP4) |

**Pagine tooltip:** «Tooltip · comune» (400×300, per la mappa di Territorio) e «Tooltip · paziente» (600×450).
**Pagine bozza** (nascoste, in fondo): test grafici (1/2 e 2/2), test KPI (1/2 e 2/2), classificazione CdC, tabella comuni compatibili, materiale da riordinare. Contengono visual messi da parte, non cancellati.

**Navigazione.** Menu laterale verde a sinistra (logo in alto, «Gruppo 5» e loghi ITS e LIUC in fondo). Nelle sottopagine ci sono i pulsanti «← Torna a…».
**Filtri.** Periodo (mesi) su Direzionale, Flussi, Attese e code, Territorio e Domanda potenziale, sincronizzato (la Direzionale ha solo questo filtro, come chiede la traccia). Pronto Soccorso su Flussi, Attese e code, Territorio, Domanda potenziale. Pulsante on/off **«Solo accessi compatibili CdC»** su Direzionale, Flussi, Attese e code, Territorio (sincronizzato; non su Domanda potenziale perché ragiona già sui soli compatibili, né su Rete CdC e Confronto che usano le tabelle dello scenario).

**Regole grafiche** (traccia): titolo su ogni visual; numeri formattati con unità; colore solo per evidenziare; niente 3D; assi in ordine logico; lettura in ordine logico.
**Regola dei titoli:** ogni grafico «parla da solo». Il titolo è l'insight, con un numero **verificato sul modello**; il sottotitolo dà unità e come leggere.

---

## 2. Direzionale (SP1 – livello strategico)

**Domanda a cui risponde:** *quanto è grande la domanda e che peso ha?* Sei KPI con confronto e andamento, un solo filtro (periodo).

| Elemento | Cosa mostra | Messaggio |
|---|---|---|
| 6 card KPI | Accessi · Codici bianchi in uscita · Attesa mediana · Permanenza 90° percentile · Valore prestazioni · % accessi compatibili CdC | Vedi [04](04-kpi-e-misure.md), sezione 2 |
| Colonne «Accessi in crescita: +33% da gennaio a maggio» | Accessi per mese; mese più alto in verde scuro; linea della media | Da 10.707 a gennaio a 14.242 a maggio |
| Treemap «9 accessi su 10 escono con codice verde o bianco» | Triage in **uscita** | Verde 80,6%, bianco 7,0%: **87,6%** in totale |
| Barre «Primi 10 comuni: in testa le sedi di PS» | Accessi per comune di residenza | In verde scuro i comuni sede di PS (Malnate confina con Varese). Un pulsante «▶ Mese per mese» apre, sopra il grafico, una classifica animata mese per mese (bar chart race, segnalibri; funzione aggiunta il 18/11, non verificata a schermo) |

> *Nota di precisione:* il titolo del treemap dice «9 accessi su 10»; il valore esatto è 87,6% (60.967 verdi + 5.304 bianchi su 75.664). Meglio «quasi 9 su 10» o «88%».

## 3. Flussi (SP1 – tattico)

**Domanda:** *chi entra, quando e come arriva, e come esce?* Volumi per periodo, giorno e ora; anagrafica; triage; diagnosi; modalità di arrivo; esiti; prestazioni; codici bianchi e ticket.

| Grafico | Messaggio (numeri sul periodo intero) |
|---|---|
| Linea (media mobile 7 giorni) «Accessi al giorno in crescita per tutto il semestre: da 345 a 463 (+34%)» | Tolto l'effetto del giorno della settimana |
| Colonne per giorno «Il lunedì è il giorno più carico: 458 accessi, +10% sulla media» | Accessi medi per giorno della settimana |
| Linea per ora «Arrivi concentrati tra le 9 e le 12» | Picco alle 10 (33 accessi al giorno), minimo alle 4 (4) |
| Piramide età–sesso | Più donne tra 15 e 44 anni (c'è il PS ostetrico-ginecologico) e dopo i 75 |
| Barre «Traumi e sintomi non definiti: quasi metà degli accessi (45%)» | Prime 7 categorie ICD-9-CM della diagnosi principale |
| Colonne «Arrivi con mezzi propri, per codice in ingresso (%)» | I meno gravi arrivano da soli: sono quelli che una CdC può intercettare |
| Colonne «Ricovero o trasferimento, per fascia d'età (%)» | Dopo i 75 anni quasi 1 accesso su 3 finisce in ricovero: casi da PS |
| Sankey «Triage: dal colore in ingresso al colore in uscita» | Quasi 1 giallo su 2 (49%) esce verde o bianco |
| 6 card KPI | Accessi al giorno · Accessi per paziente · Arrivi con mezzi propri · Prestazioni per accesso · Valore medio per accesso · Ticket stimato − registrato |

Sottopagine: **Confronto tra PS** (età, triage e sesso per PS in barre al 100%; dispersione animata mese per mese: volume contro attesa mediana) e **Approfondimento episodi** (valore contro numero di prestazioni, correlazione 0,69).

## 4. Attese e code (SP1 – tattico)

**Domanda:** *quanto si aspetta e quanto si resta, e quando il PS è più carico?* Attesa (arrivo → presa in carico) e permanenza (arrivo → dimissione) in **mediana e 90° percentile**, per triage in ingresso e fascia oraria.

| Grafico | Messaggio |
|---|---|
| Matrice giorno × ora «Pazienti presenti in PS: il massimo è il lunedì tra le 11 e le 16 (circa 174)» | Media dei pazienti presenti nello stesso momento; minimo la domenica all'alba (84) |
| Colonne «Chi è meno grave aspetta di più: 66 minuti i bianchi, 6 i rossi» | Mediana e 90° percentile per triage in ingresso |
| Colonne «I gialli restano più a lungo: oltre 6 ore di mediana» | Permanenza per triage in ingresso; esclusi gli accessi senza dimissione |
| Combinato «I picchi di arrivi non allungano i tempi» | Colonne: arrivi per ora; linee: quota che aspetta oltre 1 ora (36,6%) e che resta oltre 6 ore (25,6%) |
| 4 card KPI | Attesa 90° percentile · Attesa mediana bianchi e verdi · Permanenza mediana · Permanenza mediana bianchi e verdi |

Sottopagine: **Personale e coda** (pazienti in coda e personale presente per ora; «la coda supera i 60 pazienti tra le 10 e le 12») e, dentro **Confronto**, **Impatto sul Pronto Soccorso** (scenari CdC e turni critici).
Il numero di accessi senza dimissione (**1.526**) è indicato nel Leggimi, come chiede la traccia.

## 5. Territorio (SP1 – tattico)

**Domanda:** *da dove arrivano i pazienti?* Accessi e valore per comune, con mappa; collegamento dal **codice ISTAT a 6 cifre**.

| Elemento | Messaggio |
|---|---|
| Mappa a bolle «Da dove arrivano i pazienti» | Bolla = accessi per comune; punti rossi = i 7 PS; tooltip: accessi ogni 1.000 residenti, valore, accessi compatibili CdC e mini-andamento mensile |
| Barre «15 comuni usano il PS il doppio della media provinciale» | Accessi ogni 1.000 residenti, comuni con almeno 3.000 abitanti, media provinciale 74 |
| Tabella «Comuni con almeno 300 accessi» | Accessi, valore e tasso per comune |
| 4 card KPI | Comuni con accessi · Accessi ogni 1.000 ab. (provincia) · Quota primi 10 comuni · Accessi da fuori provincia |

## 6. Domanda potenziale (SP2)

| Elemento | Messaggio |
|---|---|
| Funnel «Da 75.664 accessi a 20.419 compatibili: la diagnosi è il filtro più selettivo» | La diagnosi esclude 25.374 accessi |
| Colonne «Più di 1 accesso su 4 (27%) è compatibile con una CdC» | Tre classi: compatibile (verde), non classificabile (ocra), non compatibile (grigio) |
| Mappa a forme dei comuni «Dove abitano i pazienti compatibili» | Compatibili per comune di residenza |
| 4 card KPI | Accessi compatibili · Valore compatibili · % valore compatibile · Quota presa in carico (ipotesi) |

Sottopagina **Classi e distribuzione**: le tre classi per mese; tabella per comune; funnel «Perché la quota base è il 50%»; slicer «Scenario CdC» (quota 0/30/50/70/100% e scenario «ampio»).

## 7. Rete CdC (SP3)

| Elemento | Messaggio |
|---|---|
| Mappa dei bacini | Dove aprire le CdC: stella = hub h24, croce = spoke 8–20, quadrato = PS, grigio = fuori territorio |
| «Perché 6 CdC» | Con 6 CdC il 93% della domanda è entro 10 km (soglia 90%) |
| «La domanda di ogni CdC, passo per passo» | Teorica → a CdC aperta → 50% presa in carico → entro la capacità |
| Tabella «Orari, personale, capacità e costi per CdC» | Hub h24 7/7, spoke 8–20 6/7 (DM 77); medici 38,72 €/h (ACN 2026) |
| 6 card KPI | CdC proposte · Visite gestite/anno · Accessi PS in meno · Km medi · Domanda entro 10 km · Costo annuo |

## 8. Confronto (SP4)

| Elemento | Messaggio |
|---|---|
| 6 card KPI (scostamenti Proposta − DG) | CdC · Km medi · Entro 10 km · Visite gestite/anno · Accessi PS in meno · Costo annuo |
| Tabella «Le due configurazioni sugli stessi indicatori» | Accessibilità, risposta alla domanda e costi |
| Due mappe affiancate | Proposta (6 CdC) e Direzione Generale (10 CdC) |
| **Nota decisionale** | Raccomandazione e tre evidenze (testo in [07](07-rete-cdc-e-confronto.md)) |

Sottopagine: **Scenari e dettaglio** (fasce di distanza, sensibilità 30/50/70%, tutti gli scenari, dotazioni delle sedi) e **Impatto sul Pronto Soccorso** (accessi deviati e turni critici per scenario: «Meno accessi non bastano: i turni critici scendono solo oltre il 70%»).

## 9. Leggimi

È la pagina del metodo, richiesta dalla traccia: **fonti, anomalie e decisioni, definizione dei KPI, numeri di controllo**, più il metodo e le ipotesi.

**Come è fatta.** Cinque riquadri, ognuno con un titolo, poche righe di sintesi e, in fondo, un **pulsante GitHub** (con il logo) che apre il documento completo di questa cartella. Le righe sono corte di proposito: il dettaglio sta nei documenti.

| Riquadro | Contenuto sulla pagina | Pulsante GitHub apre |
|---|---|---|
| Fonti | Flusso dei 7 PS (75.664 accessi), codifiche ICD-9, ISTAT, DM 77/2022 e AGENAS, costi ACN e RGS (il resto è IPOTESI) | [02 – Fonti](02-fonti.md) |
| Anomalie e decisioni | 1.526 senza dimissione; 2.483 con diagnosi assente o senza capitolo; 1.747 arrivi «non rilevato»; 153 senza triage; 22 residenze non utilizzabili; 3 pazienti con sesso diverso; nessun accesso cancellato | [03 – Anomalie](03-anomalie-e-decisioni.md) |
| Numeri di controllo | Accessi totali, pazienti distinti, valore totale, accessi senza dimissione, codici bianchi (misure vive del modello, formato italiano) | [04, sezione 5](04-kpi-e-misure.md#5-numeri-di-controllo-pagina-leggimi) |
| Definizione dei KPI | I 6 KPI della Direzionale con formula e valore | [04 – KPI e misure](04-kpi-e-misure.md) e [04b – Catalogo delle misure](04b-catalogo-misure.md) |
| Metodo e ipotesi | Imbuto unico (20.419 compatibili, 1.245 non classificabili), quota 50%, rete di 6 sedi, stime teoriche | [01 – Metodo](01-metodo.md) |

**Indirizzo dei pulsanti.** I pulsanti non hanno l'indirizzo scritto dentro: lo leggono dalle misure della cartella `9 Grafica\GitHub` del modello (una per pulsante, tutte costruite da `GitHub indirizzo base`). Oggi `GitHub indirizzo base` vale `https://github.com/giacomo-fedeli/Progettazione-Territoriale-CdC/blob/main/docs/` (con la barra finale): ogni pulsante apre il documento giusto di questa cartella nell'anteprima di GitHub. Se il repository cambia, basta cambiare **quella sola misura**.

**Le due sottopagine** («Imbuto CdC e code» e «Rete CdC (SP3 e SP4)») hanno lo stesso stile: due riquadri con titolo, tre numeri grandi, poche righe di sintesi e un pulsante GitHub.

| Sottopagina | Riquadro | Numeri grandi | Pulsante GitHub apre |
|---|---|---|---|
| Imbuto CdC e code | Imbuto CdC | 20.419 compatibili · 1.245 non classificabili · 54.000 non compatibili | [06 – Domanda potenziale](06-domanda-potenziale-cdc.md) |
| Imbuto CdC e code | Studio delle code e scenari CdC | 8 su 21 turni critici oggi · 6 con quota 70% · 5 con quota 100% | [04, sezione 4](04-kpi-e-misure.md#4-studio-delle-code-facoltativo-sp1) |
| Rete CdC (SP3 e SP4) | Rete CdC (SP3) | 6 CdC · 93% entro 10 km · 3,86 M€ | [07 – Rete CdC e confronto](07-rete-cdc-e-confronto.md) |
| Rete CdC (SP3 e SP4) | Confronto con la Direzione (SP4) | 10 CdC · −1,41 M€ · +1.343 visite/anno (Proposta − DG) | [07 – Rete CdC e confronto](07-rete-cdc-e-confronto.md) |

Gli indirizzi sono le misure `GitHub link imbuto`, `GitHub link code` e `GitHub link rete`, costruite anch'esse da `GitHub indirizzo base`.

---

## 10. Convenzioni del progetto grafico

- **Palette** (ASST Sette Laghi / Regione Lombardia): verde scuro `#093625` (menu e copertina), verde `#007A3D`, verde chiaro `#4CB848`, sfondo `#F3F6F4`, riquadri bianchi con bordo `#E1E8E4`, testo `#10231B`.
- **Colori dei grafici** (validati per il daltonismo, in questo ordine): `#007A3D`, `#1F6FA8`, `#C27C00`, `#7B5EA7`, `#C8553D`, `#0F9FB5`, `#3F9E3C`, `#A64D79`.
- **Angoli** arrotondati con raggio 17 px; **font** Segoe UI.
- **Nomi:** gli oggetti di grafica hanno prefisso `ds_` (menu, intestazione, pulsanti, filtri, card KPI); i filtri che nascondono i codici anomali hanno prefisso `ds_f_anom_`. I visual senza `ds_` sono i grafici di analisi.
- **Card KPI:** immagini SVG disegnate da misure DAX (vedi [04](04-kpi-e-misure.md), sezione 6).

Descrizione dell'evoluzione della dashboard (storia delle scelte) in [10](10-limiti-e-riproducibilita.md), sezione «Come è cambiato il lavoro».

**Torna all'[indice](README.md).**

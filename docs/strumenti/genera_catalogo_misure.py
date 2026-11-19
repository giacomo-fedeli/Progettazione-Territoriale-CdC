"""Genera il catalogo delle misure DAX (docs/04b-catalogo-misure.md) dai file del progetto Power BI.

Legge i file TMDL del modello e i file PBIR del report: niente è scritto a mano, quindi il DAX
nel catalogo è sempre quello vero del modello.

Uso (da qualunque cartella):
    python genera_catalogo_misure.py <cartella "definition" del SemanticModel> <cartella "definition" del Report> <file .md di uscita>

Esempio, dalla radice del repository:
    python docs/strumenti/genera_catalogo_misure.py powerbi/PW4.SemanticModel/definition powerbi/PW4.Report/definition docs/04b-catalogo-misure.md

Servono solo Python 3.9+ e la libreria standard.
"""
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

# ----------------------------------------------------------------------------------------------
# 1. Lettura delle misure dal modello (TMDL)
# ----------------------------------------------------------------------------------------------


def indent_of(line):
    n = 0
    for ch in line:
        if ch == "\t":
            n += 1
        else:
            break
    return n


PROP = re.compile(
    r"^(formatString|lineageTag|displayFolder|isHidden|dataType|summarizeBy|sourceColumn|dataCategory|sortByColumn|"
    r"annotation|changedProperty|isDataTypeInferred|description|mode|source|isKey|extendedProperty|formatStringDefinition)\b"
)


def read_measures(model_def):
    """Ritorna la lista di misure: dict(name, table, folder, fmt, doc, expr, hidden)."""
    measures = []
    for path in sorted((model_def / "tables").glob("*.tmdl")):
        lines = path.read_text(encoding="utf-8-sig").replace("\r", "").split("\n")
        table = None
        doc = []
        i = 0
        while i < len(lines):
            raw = lines[i]
            s = raw.strip()
            ind = indent_of(raw)
            if s.startswith("///"):
                doc.append(s[3:].strip())
                i += 1
                continue
            if ind == 0 and s.startswith("table "):
                table = s[6:].strip().strip("'")
                doc = []
                i += 1
                continue
            if ind == 1 and s.startswith("measure "):
                rest = s[len("measure "):]
                if rest.startswith("'"):
                    end = rest.index("'", 1)
                    name = rest[1:end]
                    remainder = rest[end + 1:].strip()
                else:
                    m = re.match(r"([^\s=]+)\s*(.*)$", rest)
                    name, remainder = m.group(1), m.group(2)
                expr_first = remainder[1:].strip() if remainder.startswith("=") else ""
                body = []
                i += 1
                if expr_first.startswith("```"):
                    first = expr_first[3:]
                    if first.strip():
                        body.append(first)
                    while i < len(lines) and "```" not in lines[i]:
                        body.append(lines[i].lstrip("\t"))
                        i += 1
                    if i < len(lines):
                        tail = lines[i].split("```")[0].strip()
                        if tail:
                            body.append(tail)
                    i += 1
                else:
                    if expr_first:
                        body.append(expr_first)
                    while i < len(lines):
                        r2 = lines[i]
                        s2 = r2.strip()
                        ind2 = indent_of(r2)
                        if s2 == "":
                            j = i + 1
                            while j < len(lines) and lines[j].strip() == "":
                                j += 1
                            if j < len(lines) and indent_of(lines[j]) >= 3 and not PROP.match(lines[j].strip()):
                                body.append("")
                                i += 1
                                continue
                            break
                        if ind2 >= 3 and not (ind2 == 2) and not PROP.match(s2):
                            body.append(r2.lstrip("\t") if ind2 <= 3 else "\t" * (ind2 - 3) + s2)
                            i += 1
                            continue
                        break
                meas = {"name": name, "table": table, "folder": "", "fmt": "", "doc": " ".join(doc),
                        "expr": "\n".join(body).strip(), "hidden": False}
                doc = []
                # proprietà (indent 2)
                while i < len(lines):
                    r3 = lines[i]
                    s3 = r3.strip()
                    if s3 == "":
                        i += 1
                        if i < len(lines) and indent_of(lines[i]) <= 1:
                            break
                        continue
                    if indent_of(r3) < 2:
                        break
                    if s3.startswith("formatString:"):
                        meas["fmt"] = s3.split(":", 1)[1].strip()
                    elif s3.startswith("displayFolder:"):
                        meas["folder"] = s3.split(":", 1)[1].strip()
                    elif s3 == "isHidden":
                        meas["hidden"] = True
                    i += 1
                measures.append(meas)
                continue
            i += 1
    return measures


# ----------------------------------------------------------------------------------------------
# 2. Dove si vede ogni misura (visual del report)
# ----------------------------------------------------------------------------------------------


def page_kind(display, visibility, ptype):
    if ptype == "Tooltip" or display.startswith("Tooltip"):
        return "tooltip"
    if display.startswith("Bozza"):
        return "bozza"
    if visibility == "HiddenInViewMode":
        return "sottopagina"
    return "principale"


def read_usage(report_def, names):
    """Ritorna {misura: {pagina: tipo}}."""
    usage = defaultdict(dict)
    pages_dir = report_def / "pages"
    pat = re.compile(r'"Property"\s*:\s*"([^"]+)"')
    nameset = set(names)
    for pdir in sorted(p for p in pages_dir.iterdir() if p.is_dir()):
        pj = json.loads((pdir / "page.json").read_text(encoding="utf-8"))
        display = pj.get("displayName", pdir.name)
        kind = page_kind(display, pj.get("visibility", ""), pj.get("type", ""))
        texts = [(pdir / "page.json").read_text(encoding="utf-8")]
        vdir = pdir / "visuals"
        if vdir.exists():
            for vf in vdir.glob("*/visual.json"):
                texts.append(vf.read_text(encoding="utf-8"))
        for t in texts:
            for m in pat.findall(t):
                if m in nameset:
                    usage[m][display] = kind
    # segnalibri e report.json
    for extra in [report_def / "report.json"] + list((report_def / "bookmarks").glob("*.json") if (report_def / "bookmarks").exists() else []):
        if extra.exists():
            for m in pat.findall(extra.read_text(encoding="utf-8")):
                if m in nameset:
                    usage[m].setdefault("(report)", "principale")
    return usage


# ----------------------------------------------------------------------------------------------
# 3. Descrizioni (solo per le misure senza descrizione nel modello)
# ----------------------------------------------------------------------------------------------

DESC = {
    "Accessi": "Numero di accessi: un accesso è una riga della tabella dei fatti (un episodio al Pronto Soccorso).",
    "Pazienti": "Pazienti distinti (conteggio distinto di FK_Paziente). Un paziente può avere più accessi.",
    "Accessi per paziente": "Accessi divisi per pazienti distinti.",
    "Paziente top": "Codice del paziente con più accessi nel contesto di filtro.",
    "Max accessi per paziente": "Numero massimo di accessi di un singolo paziente.",
    "Valore €": "Somma del valore economico delle prestazioni. È una valorizzazione tariffaria, non un costo.",
    "Scostamento ticket €": "Ticket stimato − ticket registrato: differenza tra la stima della traccia (25 € × codici bianchi in uscita) e l'importo registrato nel flusso.",
    "Accessi V+B": "Accessi con triage in INGRESSO verde o bianco (gruppo «Minore (V/B)»). Idea di partenza della sottoprova 2, non è un KPI.",
    "% V+B": "Quota di accessi con triage in ingresso verde o bianco.",
    "Valore € V+B": "Valore delle prestazioni degli accessi con triage in ingresso verde o bianco.",
    "Durata mediana (min)": "Mediana accettazione → dimissione, in minuti, calcolata riga per riga (solo accessi con dimissione). Il KPI ufficiale è «Permanenza mediana (min)».",
    "Fascia di picco": "Ora del giorno con più accessi nel contesto, come testo «hh:00».",
    "% codici bianchi": "Accessi con triage in USCITA bianco ÷ tutti gli accessi.",
    "Accessi codice bianco": "Accessi con triage in USCITA = B (bianco). La traccia chiede il triage in uscita.",
    "Attesa mediana (min)": "Mediana di (presa in carico − arrivo), in minuti.",
    "Attesa P90 (min)": "90° percentile di (presa in carico − arrivo), in minuti (PERCENTILE.INC).",
    "Permanenza mediana (min)": "Mediana di (dimissione − arrivo), in minuti. Gli accessi senza dimissione non entrano.",
    "Permanenza P90 (min)": "90° percentile di (dimissione − arrivo), in minuti. Gli accessi senza dimissione non entrano.",
    "Prestazioni": "Somma del numero di prestazioni registrate.",
    "Ticket stimato €": "Accessi con codice bianco in uscita × importo del ticket (25 €). Stima della compartecipazione, non costo del servizio.",
    "Accessi mese prec": "Accessi del mese precedente al mese di riferimento (ignora il filtro mese).",
    "Mese rif": "Numero dell'ultimo mese con dati nel periodo scelto: è il «mese di riferimento» dei confronti.",
    "Var % accessi": "Variazione % degli accessi: mese di riferimento rispetto al mese precedente.",
    "Accessi mese": "Accessi del mese di riferimento (ignora il filtro mese).",
    "Lettura accessi": "Testo di lettura: ▲ in aumento / ▼ in calo / ● stabile (banda di stabilità ±2%).",
    "Tempo medio permanenza (min)": "Media accettazione → dimissione (formato giorni, non minuti). Non usata nel report: si usano mediana e P90.",
    "Riduzione accessi PS %": "Accessi deviati ÷ accessi totali. Stima teorica a tutte le ore.",
    "Durata Minutti Accettazione-PresaInCarico (min)": "Media arrivo → presa in carico, in minuti. Non usata nel report (si usano mediana e P90).",
    "Durata Minutti Accettazione-Dimissione (min)": "Media arrivo → dimissione, in minuti. Non usata nel report.",
    "Durata Minutti PresaInCarico-Dimissione (min)": "Media presa in carico → dimissione, in minuti. Non usata nel report.",
    "FNL Step 0 - Accessi Totali": "Imbuto, passo 0: tutti gli accessi.",
    "FNL Step 1 - Triage Ingresso": "Imbuto, passo 1: accessi con triage in ingresso compatibile (verde o bianco).",
    "FNL Step 2 - + Diagnosi": "Imbuto, passo 2: … e diagnosi primaria compatibile.",
    "FNL Step 3 - + Esito": "Imbuto, passo 3: … ed esito compatibile.",
    "FNL Step 4 - + Durata": "Imbuto, passo 4: … e durata presa in carico → dimissione ≤ 2 ore.",
    "FNL Step 5 - + Triage Uscita": "Imbuto, passo 5: … e triage in uscita compatibile.",
    "FNL Step 6 - + Diagnosi Secondaria": "Imbuto, passo 6: … e diagnosi secondaria compatibile, se presente.",
    "FNL Step 7 - Episodio Compatibile CdC": "Imbuto, passo 7 (ultimo): accessi con Episodio_Compatibile_CdC = TRUE. Coincide con «Accessi compatibili CdC».",
    "FNL Valore": "Valore mostrato dal funnel «Da 75.664 accessi a 20.419 compatibili»: sceglie la misura FNL Step in base alla fase.",
    "% Accessi Compatibili CdC": "Accessi compatibili CdC ÷ tutti gli accessi.",
    "Valore economico compatibili CdC": "Somma del valore delle prestazioni degli accessi compatibili CdC.",
    "% valore economico  compatibili CdC": "Valore dei compatibili ÷ valore totale delle prestazioni.",
    "Media Mobile 7 Giorni": "Media mobile a 7 giorni degli accessi giornalieri (toglie l'effetto del giorno della settimana).",
    "Presenti (media)": "Pazienti presenti per ora, media sui giorni (tabella Tab_Presenti_Ora_Istituto).",
    "In coda (media)": "Pazienti arrivati ma non ancora presi in carico, in media per ora.",
    "Personale (media)": "Personale presente in media per ora e per PS, dalla tabella dei turni.",
    "Personale (tab)": "Personale presente per ora, dalla tabella calcolata.",
    "Coda per operatore": "Pazienti in coda ÷ personale presente.",
}

# ----------------------------------------------------------------------------------------------
# 4. Gruppi del catalogo
# ----------------------------------------------------------------------------------------------

PRESENTAZIONE_PREFIX = ("KPI card ", "KPI sub ", "KPI stile ", "KPI Direzionale ", "KPI Flussi ", "KPI Attese ",
                        "KPI Territorio ", "KPI Domanda ", "KPI Rete CdC ", "KPI Confronto ", "Colore ", "Tooltip ", "Lettura valore",
                        "Lettura attesa", "Lettura permanenza", "Lettura codici", "Lettura accessi", "Lettura scenario", "Lettura medici",
                        "SP4 Lettura")

GROUPS = [
    ("A. Volumi, pazienti e valore", [
        "Accessi", "Pazienti", "Accessi per paziente", "Paziente top", "Max accessi per paziente", "Valore €", "Prestazioni",
        "Accessi medi giornalieri", "Valore medio per accesso €", "Media Mobile 7 Giorni", "Fascia di picco", "Accessi V+B", "% V+B", "Valore € V+B",
        "% arrivi autonomi", "Prestazioni per accesso", "% ricovero o trasferimento", "Accessi maschi", "Accessi femmine",
        "Ritorni entro 72 ore", "% ritorni entro 72 ore", "Pazienti con 4+ accessi", "% accessi pazienti con 4+ accessi",
        "% dei pazienti", "% accessi per frequenza", "% degli accessi"]),
    ("B. Codici bianchi e ticket", [
        "Accessi codice bianco", "% codici bianchi", "Ticket stimato €", "Ticket registrato €", "Scostamento ticket €"]),
    ("C. Attese, permanenza e pazienti presenti", [
        "Attesa mediana (min)", "Attesa P90 (min)", "Permanenza mediana (min)", "Permanenza P90 (min)",
        "Attesa mediana bianchi e verdi (min)", "Permanenza mediana bianchi e verdi (min)", "% attesa oltre 1 ora", "% permanenza oltre 6 ore", "% permanenze oltre 24 ore", "Attesa mediana (h min)", "Permanenza mediana (h min)", "Attesa P90 (h min)", "Permanenza P90 (h min)",
        "Accessi senza dimissione", "Durata mediana (min)", "Tempo medio permanenza (min)",
        "Durata Minutti Accettazione-PresaInCarico (min)", "Durata Minutti Accettazione-Dimissione (min)",
        "Durata Minutti PresaInCarico-Dimissione (min)", "Pazienti in coda (media)", "Pazienti presenti (P90)",
        "Presenti (media)", "In coda (media)", "Accessi (media per ora)", "Personale (media)", "Personale (tab)", "Coda per operatore"]),
    ("D. Territorio", [
        "Accessi per 1.000 ab.", "Accessi per 1.000 ab. provincia Varese", "Accessi per 1.000 ab. comuni da 3.000 ab.", "Comuni con accessi",
        "Quota accessi sul totale", "Quota accessi top 10 comuni", "% accessi da fuori provincia"]),
    ("E. Confronto con il mese precedente (KPI della Direzionale)", [
        "Mese rif", "Mese rif breve", "Mese prec breve", "Accessi mese", "Accessi mese prec", "Var % accessi", "Media mensile accessi",
        "Valore € mese", "Valore € mese prec", "Var % valore", "Attesa mediana mese", "Attesa mediana mese prec", "Var % attesa mediana",
        "Permanenza P90 mese", "Permanenza P90 mese prec", "Var % permanenza P90", "% codici bianchi mese", "% codici bianchi mese prec",
        "Var % codici bianchi"]),
    ("F. Domanda potenziale CdC (imbuto unico)", [
        "Accessi compatibili CdC", "Accessi non classificabili CdC", "Accessi non compatibili CdC", "% Accessi Compatibili CdC",
        "Valore economico compatibili CdC", "% valore economico  compatibili CdC", "Quota CdC base dati",
        "FNL Step 0 - Accessi Totali", "FNL Step 1 - Triage Ingresso", "FNL Step 2 - + Diagnosi", "FNL Step 3 - + Esito", "FNL Step 4 - + Durata",
        "FNL Step 5 - + Triage Uscita", "FNL Step 6 - + Diagnosi Secondaria", "FNL Step 7 - Episodio Compatibile CdC", "FNL Valore"]),
    ("G. Scenari CdC (quota di presa in carico)", [
        "Quota CdC compatibili", "Quota CdC non classificabili", "Scenario CdC attivo", "Accessi deviati alle CdC",
        "Riduzione accessi PS %"]),
    ("H. Rete CdC (SP3)", None),  # cartella «SP3 Rete CdC»
    ("I. Confronto con la Direzione Generale (SP4)", None),  # cartella «SP4 Confronto»
    ("L. Controlli per la pagina Leggimi", None),  # cartella «8 Controlli (Leggimi)»
]


# Elenco facoltativo di misure da non documentare: un nome per riga in `escludi_misure.txt` (file locale, non
# pubblicato). Si escludono anche le misure che le richiamano ([Nome] nel DAX).
_FILE_ESCLUSE = Path(__file__).with_name("escludi_misure.txt")
MISURE_ESCLUSE = set(_FILE_ESCLUSE.read_text(encoding="utf-8").splitlines()) - {""} if _FILE_ESCLUSE.exists() else set()


def senza_misure_escluse(measures):
    esclusi = set(MISURE_ESCLUSE)
    cambiato = True
    while cambiato:
        cambiato = False
        for m in measures:
            if m["name"] not in esclusi and any(f"[{e}]" in m["expr"] for e in esclusi):
                esclusi.add(m["name"])
                cambiato = True
    return [m for m in measures if m["name"] not in esclusi], esclusi


def is_presentazione(m):
    f = m["folder"]
    n = m["name"]
    if f.startswith("Grafica KPI") or f.startswith("9 Grafica"):
        return True
    if n.startswith(PRESENTAZIONE_PREFIX):
        return True
    return False


def md_escape(s):
    return s.replace("|", "\\|").replace("\n", " ")


def main():
    model_def, report_def, out = (Path(a) for a in sys.argv[1:4])
    measures = read_measures(model_def)
    measures, esclusi = senza_misure_escluse(measures)
    by_name = OrderedDict((m["name"], m) for m in measures)
    usage = read_usage(report_def, list(by_name))

    # dipendenze tra misure: [Nome] dentro il DAX
    used_by = defaultdict(set)
    for m in measures:
        for ref in re.findall(r"\[([^\]]+)\]", m["expr"]):
            if ref in by_name and ref != m["name"]:
                used_by[ref].add(m["name"])

    pres = [m for m in measures if is_presentazione(m)]
    calc = [m for m in measures if not is_presentazione(m)]

    def where(m):
        u = usage.get(m["name"], {})
        main = sorted(p for p, k in u.items() if k == "principale")
        sub = sorted(p for p, k in u.items() if k in ("sottopagina", "tooltip"))
        boz = sorted(p for p, k in u.items() if k == "bozza")
        parts = []
        if main:
            parts.append(", ".join(main))
        if sub:
            parts.append(f"+ {len(sub)} sottopagin{'a' if len(sub) == 1 else 'e'}")
        if not parts and boz:
            parts.append("solo bozze")
        # card KPI: la misura è mostrata dalle misure SVG «KPI <pagina> …»
        dep = sorted(used_by.get(m["name"], []))
        card_pages = sorted({d.split(" ")[1] for d in dep if d.startswith("KPI ") and len(d.split(" ")) > 2
                             and d.split(" ")[1] in ("Direzionale", "Flussi", "Attese", "Territorio", "Domanda", "Rete", "Confronto")})
        if card_pages and not main:
            parts = ["card KPI di " + ", ".join(card_pages)] + ([p for p in parts if p.startswith("+")])
        elif card_pages:
            parts.append("card KPI di " + ", ".join(card_pages))
        if not parts:
            vis = [d for d in dep if usage.get(d)]
            if vis:
                parts.append("indiretta (via " + ", ".join(vis[:2]) + (" …" if len(vis) > 2 else "") + ")")
            elif dep:
                parts.append("indiretta (via " + ", ".join(dep[:2]) + ")")
            else:
                parts.append("non usata")
        return " · ".join(parts)

    def desc(m):
        if m["doc"]:
            return m["doc"]
        return DESC.get(m["name"], "")

    # assegnazione ai gruppi
    assigned = {}
    for title, names in GROUPS:
        if names:
            for n in names:
                if n in by_name:
                    assigned[n] = title
    for m in calc:
        if m["name"] in assigned:
            continue
        f = m["folder"]
        if f == "SP3 Rete CdC":
            assigned[m["name"]] = "H. Rete CdC (SP3)"
        elif f in ("SP4 Confronto", "SP4 Mappa"):
            assigned[m["name"]] = "I. Confronto con la Direzione Generale (SP4)"
        elif f.startswith("8 Controlli"):
            assigned[m["name"]] = "L. Controlli per la pagina Leggimi"
    missing = [m["name"] for m in calc if m["name"] not in assigned]

    lines = []
    w = lines.append
    w("# Catalogo delle misure DAX")
    w("")
    w("> **File generato** dallo script [`strumenti/genera_catalogo_misure.py`](strumenti/genera_catalogo_misure.py) "
      "leggendo i file del modello (TMDL) e del report (PBIR). Non modificarlo a mano: cambia il modello e rilancia lo script.")
    w("")
    w(f"Il catalogo descrive **{len(measures)} misure**: **{len(calc)} di calcolo** (questo catalogo, con formula DAX) e "
      f"**{len(pres)} di presentazione** (SVG delle card KPI, colori, testi dei sottotitoli: non calcolano numeri di business, vedi sezione M).")
    w("")
    w("Per le definizioni dei KPI in linguaggio semplice leggi prima [04 – KPI e misure](04-kpi-e-misure.md). "
      "Questo catalogo serve a chi vuole la formula esatta.")
    w("")
    w("**Come leggere le colonne**")
    w("- *Cosa misura*: descrizione scritta nel modello o, se manca, qui nello script.")
    w("- *Formato*: formato numerico DAX (`#,0` = intero con separatore, `0.0%` = percentuale con un decimale, …).")
    w("- *Dove si vede*: pagine del report che usano la misura in un visual. «Indiretta» = non è in un visual ma la usa un'altra misura. «Non usata» = né in un visual né in altre misure.")
    w("")
    fuori = [m for m in measures if m["table"] != "_Misure"]
    tabelle = sorted({m["table"] for m in fuori})
    w(f"Tutte le misure stanno nella tabella `_Misure`, tranne {len(fuori)} che stanno nelle tabelle di supporto "
      + ", ".join(f"`{t}`" for t in tabelle) + ".")
    w("")

    unused = []
    for title, _ in GROUPS:
        grp = [m for m in calc if assigned.get(m["name"]) == title]
        if not grp:
            continue
        w(f"## {title}")
        w("")
        w("| Misura | Cosa misura | Formato | Dove si vede |")
        w("|---|---|---|---|")
        for m in grp:
            wh = where(m)
            if wh == "non usata":
                unused.append(m["name"])
            w(f"| `{m['name']}` | {md_escape(desc(m))} | `{md_escape(m['fmt'])}` | {md_escape(wh)} |" if m["fmt"]
              else f"| `{m['name']}` | {md_escape(desc(m))} | – | {md_escape(wh)} |")
        w("")
        w(f"<details><summary>Formule DAX · {title}</summary>")
        w("")
        for m in grp:
            w(f"**{m['name']}**")
            w("")
            w("```dax")
            w(m["expr"] if m["expr"] else "(vuota)")
            w("```")
            w("")
        w("</details>")
        w("")

    if missing:
        w("## Altre misure di calcolo")
        w("")
        w("| Misura | Cosa misura | Formato | Dove si vede |")
        w("|---|---|---|---|")
        for n in missing:
            m = by_name[n]
            wh = where(m)
            if wh == "non usata":
                unused.append(m["name"])
            w(f"| `{n}` | {md_escape(desc(m))} | `{md_escape(m['fmt'])}` | {md_escape(wh)} |")
        w("")
        w("<details><summary>Formule DAX · altre misure</summary>")
        w("")
        for n in missing:
            w(f"**{n}**")
            w("")
            w("```dax")
            w(by_name[n]["expr"] or "(vuota)")
            w("```")
            w("")
        w("</details>")
        w("")

    # M. presentazione
    w("## M. Misure di presentazione (non calcolano numeri di business)")
    w("")
    fam = OrderedDict()
    for m in pres:
        key = m["folder"] or "(senza cartella)"
        fam.setdefault(key, []).append(m["name"])
    w("Servono solo a disegnare il report: card KPI in SVG (numero, freccia di variazione, linea mensile), colori condizionali, testi dei sottotitoli e tooltip della mappa. "
      "Ogni card KPI usa una misura di calcolo (colonna «Misura sorgente» nella descrizione dentro il modello): il numero mostrato è sempre quello della misura di calcolo.")
    w("")
    w("| Cartella nel modello | N. misure | Esempi |")
    w("|---|---:|---|")
    for k, names in fam.items():
        w(f"| {md_escape(k)} | {len(names)} | {md_escape(', '.join(names[:3]))}{' …' if len(names) > 3 else ''} |")
    w("")
    w("<details><summary>Elenco completo delle misure di presentazione</summary>")
    w("")
    for k, names in fam.items():
        w(f"**{k}**")
        w("")
        for n in names:
            w(f"- `{n}`")
        w("")
    w("</details>")
    w("")

    if unused:
        w("## Misure non usate")
        w("")
        w("Misure di calcolo che, leggendo i file del report e del modello, non compaiono in nessun visual e non sono richiamate da altre misure. "
          "Sono rimaste da prove precedenti. Prima di cancellarle apri il report e controlla con «Visualizza dipendenze» di Power BI.")
        w("")
        for n in unused:
            w(f"- `{n}`")
        w("")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"scritto {out}: {len(measures)} misure ({len(calc)} di calcolo, {len(pres)} di presentazione); non usate: {len(unused)}; senza gruppo: {len(missing)}")
    if missing:
        print("senza gruppo:", missing)


if __name__ == "__main__":
    main()

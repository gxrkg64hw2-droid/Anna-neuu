# Literaturrecherche in DACH-Datenbanken

Leitfaden fuer die systematische Literaturrecherche bei Bachelorarbeiten im
BWL-, Marketing- und Wirtschaftsbereich.

## Uebersicht

Die wichtigsten Datenbanken fuer DACH-Bachelorarbeiten im Ueberblick.

| Datenbank | Inhaltsschwerpunkt | Zugang | Besonderheit |
|---|---|---|---|
| **GBV** (Gemeinsamer Bibliotheksverbund) | Buecher, Sammelbaende, Dissertationen, Hochschulschriften | Hochschulbibliothek (Fernleihe) | Groesster deutschsprachiger Verbundkatalog, direkte Fernleihe |
| **DBIS** (Datenbank-Infosystem) | Meta-Verzeichnis aller Hochschuldatenbanken | Kostenlos ueber Hochschule | Startpunkt fuer Lizenz-Check der eigenen Hochschule |
| **wiso / GENIOS** | Deutschsprachige BWL- und Wirtschaftszeitschriften, Wirtschaftspresse | Hochschullizenz | Volltext-Zugang zu NZZ, Handelsblatt, FAZ-Archiv u.v.m. |
| **JSTOR** | Internationale Journals, breiter Fachfokus | Hochschullizenz | Gut fuer aeltere Klassiker-Artikel (pre-2010) |
| **Beck-Online** | Rechtswissenschaft, Steuerrecht, BWL-Kommentare | Hochschullizenz (juristisch) | Pflicht bei rechtlichen oder steuerlichen Fragestellungen |
| **EBSCO Business Source** | Internationale BWL, Marketing, Management | Hochschullizenz | Umfassende Peer-Review-Filter, relevante Impact-Journals |
| **OpenAlex** | 250 Mio.+ Publikationen, Open Access | Kostenlos, kein API-Key | Programmatisch nutzbar, gut fuer Zitationsanalyse |
| **Google Scholar** | Alles (breit, undifferenziert) | Kostenlos | Snowballing-Tool, aber kein Peer-Review-Filter, mit Vorsicht nutzen |

Mindestens drei Datenbanken kombinieren: wiso/GENIOS fuer deutsche
Wirtschaftsliteratur, EBSCO Business Source fuer internationale Journals,
OpenAlex oder Google Scholar fuer Snowballing.

## Suchstrategie fuer DACH-BA

Fuenf aufeinander aufbauende Schritte, reproduzierbar und pruefungssicher.

### Schritt 1: Kernbegriffe definieren

Aus der Forschungsfrage die zentralen Konzepte ableiten. Jedes Konzept bildet
einen eigenen Suchblock. Beispiel:

```
Forschungsfrage: "Einfluss von Social-Media-Marketing auf Kaufbereitschaft (Gen Z)"
Block A: Social-Media-Marketing  |  Block B: Kaufbereitschaft  |  Block C: Generation Z
```

### Schritt 2: Synonyme und englische Aequivalente ergaenzen

Deutsch und Englisch getrennt suchen, da Datenbanken nicht automatisch uebersetzen.

```
Block A DE: "Social-Media-Marketing", "Social Media Werbung", "Influencer-Marketing"
Block A EN: "social media marketing", "social media advertising", "influencer marketing"

Block B DE: "Kaufbereitschaft", "Kaufabsicht", "Kaufverhalten"
Block B EN: "purchase intention", "willingness to buy", "consumer behavior"

Block C DE: "Generation Z", "Gen Z", "Digital Natives"
Block C EN: "Generation Z", "Gen Z", "digital natives", "centennials"
```

### Schritt 3: Boolesche Operatoren anwenden

| Operator | Bedeutung | Beispiel |
|---|---|---|
| `AND` | Beide Terme muessen vorkommen | `"social media marketing" AND "purchase intention"` |
| `OR` | Mindestens ein Term muss vorkommen | `"purchase intention" OR "willingness to buy"` |
| `NOT` | Term darf nicht vorkommen | `"social media" NOT "B2B"` |
| `"..."` | Exakte Phrase | `"Generation Z"` |
| `*` | Trunkierung (Wortstamm) | `kaufbereit*` findet "Kaufbereitschaft", "kaufbereit" |

Kombination mit Klammern:

```
("social media marketing" OR "influencer marketing")
AND ("purchase intention" OR "kaufbereitschaft")
AND ("Generation Z" OR "Gen Z")
```

### Schritt 4: Ergebnisse filtern

- **Erscheinungsjahr:** Aktuelle Studien letzte 5 Jahre (2021-2026). Klassiker ohne Jahresfilter.
- **Peer-Review:** In EBSCO und JSTOR als Filter setzen. wiso/GENIOS: entfaellt (praxisorientiert).
- **Sprache:** Deutsch UND Englisch. Ergebnisse getrennt dokumentieren.
- **Dokumenttyp:** Zeitschriftenartikel bevorzugen, Buchkapitel ergaenzend.

### Schritt 5: Suchprotokoll fuehren

Jeden Suchdurchlauf dokumentieren: Datum, Datenbank, exakter Query, Trefferzahl,
Anzahl relevanter Treffer. Wird oft als Anhang der Bachelorarbeit erwartet.

---

## Beispiel-Suchprotokoll

Nachvollziehbarkeitsbeleg fuer Betreuende. Als Anhang der Bachelorarbeit
oder als separates Dokument im Arbeitsordner ablegen.

| Datum | Datenbank | Query (gekuerzt) | Treffer gesamt | Relevant (nach Screening) |
|---|---|---|---|---|
| 2026-04-10 | EBSCO Business Source | ("social media marketing" OR "influencer marketing") AND "purchase intention" AND "Generation Z" | 84 | 12 |
| 2026-04-10 | wiso/GENIOS | "Social-Media-Marketing" AND "Kaufbereitschaft" AND "Generation Z" | 21 | 5 |
| 2026-04-11 | OpenAlex | social media marketing purchase intention Generation Z (Titelsuche) | 310 | 9 |
| 2026-04-12 | Google Scholar | "social media marketing" "Generation Z" "purchase intention" site:scholar.google.com | 1200+ | 7 (Snowballing) |

Query immer exakt kopieren. "Relevant" = nach Lesen von Titel und Abstract
als zitierwuerdig eingestuft. Google Scholar Gesamtzahlen nicht belastbar,
deshalb "Snowballing" als Methode explizit vermerken.

---

## PRISMA-Flowdiagramm

PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
dokumentiert die Quellenauswahl transparent. Bei Bachelorarbeiten genuegt
eine vereinfachte Variante. Bei explizit "systematischer Literaturrecherche"
und bei Metaanalysen ist es Pflicht.

### Vereinfachte Struktur (ASCII)

```
+----------------------------------+
|   IDENTIFICATION                 |
|   Gefunden in Datenbanken: N=xxx |
|   Duplikate entfernt: -N         |
+----------------------------------+
            |
            v
+----------------------------------+
|   SCREENING                      |
|   Titel/Abstract gescreent: N    |
|   Ausgeschlossen: -N             |
|   (Begruendung: nicht relevant,  |
|    falsches Thema, zu alt, ...)  |
+----------------------------------+
            |
            v
+----------------------------------+
|   ELIGIBILITY                    |
|   Volltext geprueft: N           |
|   Ausgeschlossen: -N             |
|   (Begruendung: kein Volltext,   |
|    Methodik ungeeignet, ...)     |
+----------------------------------+
            |
            v
+----------------------------------+
|   INCLUDED                       |
|   Finale Quellen: N              |
|   + Quellen via Snowballing: +N  |
+----------------------------------+
```

---

## Snowballing

Snowballing findet Quellen ausserhalb der Datenbanksuche: Klassiker, die selten
in modernen Indizes auftauchen, und aktuelle Weiterentwicklungen bekannter Konzepte.

### Backward Snowballing (Rueckwaertssuche)

Literaturverzeichnisse der besten 5-10 Datenbankfunde durchgehen. Autoren die
mehrfach auftauchen, sind Kernwerke. Gut fuer Theoriekapitel: Klassiker wie
Davis 1989 (TAM) oder Rogers 1983 tauchen im Datenbankscreening oft nicht auf.

### Forward Snowballing (Vorwaertssuche)

In Google Scholar unter einem Treffer auf "Zitiert von: N" klicken, dann nach
Datum sortieren. Findet aktuelle Weiterentwicklungen eines Klassikers, z.B.
Studien 2022-2026, die ein 2015er Konzept auf Social Media oder DACH uebertragen.

### Kombinierter Ablauf

```
Datenbank-Suche (10-15 relevante Quellen)
    -> Backward: Literaturverzeichnisse -> Klassiker
    -> Forward (Google Scholar "Zitiert von") -> aktuelle Weiterentwicklungen
    -> Neue Treffer in Zotero, .bib exportieren, PDFs in pdfs/-Ordner
    -> python -m rag index --thesis <name>  (inkrementell, schnell)
```

---

## Zotero-Workflow

Zotero + Better BibTeX ergibt einen automatisch synchronisierten Workflow
ohne manuelle Bibliographie-Pflege.

### Einrichtung (einmalig)

1. Zotero Desktop: https://www.zotero.org/download/
2. Better BibTeX Plugin: https://github.com/retorquere/zotero-better-bibtex/releases
3. Zotero Connector (Browser-Extension) fuer 1-Klick-Import aus Datenbanken.

### Workflow

```
Datenbank-Treffer -> Zotero Connector -> Eintrag + PDF in Zotero
    -> Rechtsklick Sammlung -> "Exportieren"
       Format: "Better BibTeX", Option "Keep updated" aktivieren
    -> Export-Ziel: thesen/<name>/bibliography.bib
```

### Was Better BibTeX automatisch schreibt

Better BibTeX generiert eindeutige Zitierschluessel (z.B. `rogersInnovation1983`)
und schreibt `file = {filename.pdf}` in die `.bib`. Beispiel:

```bibtex
@book{rogersInnovation1983,
  author    = {Rogers, Everett M.},
  title     = {Diffusion of Innovations},
  year      = {1983},
  publisher = {Free Press},
  file      = {:rogers-1983.pdf:PDF}
}
```

Der Auto-Linker liest das `file = {...}` Feld und verknuepft den Bibkey mit der
`sources`-Zeile in der Corpus-DB. Nach `python -m rag index` haben alle
Suchtreffer fertig formatierte Zitiersyntax.

### Lean-Modus (kein Zotero verfuegbar)

PDFs direkt in `thesen/<name>/pdfs/` ablegen, dann:

```bash
python -m rag bib --thesis <name> --build
```

Extrahiert DOIs aus den ersten drei PDF-Seiten, sucht via OpenAlex und Crossref,
erstellt Bibkeys automatisch. Danach `index` ausfuehren.

---

## Verbindung zum Bachelorarbeits-System

Das RAG-Toolkit und die Literaturrecherche greifen ineinander.

### Fluss von der Recherche zum zitierfaehigen Treffer

```
1. Literaturrecherche (diese Anleitung)
        |
        v
2. PDFs gesammelt und in thesen/<name>/pdfs/ kopiert
   bibliography.bib exportiert nach thesen/<name>/bibliography.bib
        |
        v
3. python -m rag index --thesis <name>
   -> Volltext wird extrahiert und in 512-Token-Chunks zerlegt
   -> Embeddings werden berechnet (OpenAI text-embedding-3-large)
   -> BM25-Index wird gebaut
   -> Auto-Linker verknuepft Bibkeys mit Quellen via file=-Felder
        |
        v
4. python -m rag search "Konzept aus der Theorie" --thesis <name>
   -> Gibt Treffer mit Seitenangabe (gedruckte Seite) zurueck
   -> Gibt citation_suggestion direkt als LaTeX aus:
      \parencite[S. 47]{rogersInnovation1983}
        |
        v
5. Treffer im .tex-Kapitel verwenden
   python -m rag verify-quote --text "paraphrasierter Satz" --thesis <name>
   -> Prueft, ob die Formulierung zu nah am Originaltext ist
```

| Aufgabe | RAG-System | Literaturrecherche |
|---|---|---|
| Neue Quellen finden | Nein | Ja |
| Theoriegeruest strukturieren | Nein | Ja (Literature-Review-Skill) |
| Relevante Stellen in Corpus abrufen | Ja (rag search) | Nein |
| Seitenkonkretes Zitieren | Ja | Nein |
| Plagiatsselbstcheck | Ja (verify-quote) | Nein |
| Zitierkonsistenz pruefen | Ja (extract-citations) | Nein |

Die Literaturrecherche befuellt den Corpus. Das RAG-System nutzt ihn fuer
praezises, seitenkonkretes Schreiben. Beide Teile ersetzen sich nicht.

```bash
python -m rag corpus --thesis <name> --pretty
```

Zeigt Quellen, Bibkeys, Chunks und Erkennungsqualitaet. Vor dem Schreiben
pruefen, ob alle erwarteten Quellen erscheinen.

---

## Checkliste vor Verfassen des Theoretischen Rahmens

### Recherche

- [ ] Mindestens 3 Datenbanken systematisch durchsucht
- [ ] Suchprotokoll vollstaendig dokumentiert (Datum, DB, Query, Treffer, Relevant)
- [ ] Kernwerke (klassische Theoriebegriffsquellen) durch Backward Snowballing identifiziert
- [ ] Aktuelle Studien (letzte 5 Jahre) abgedeckt, mindestens 5-8 Treffer
- [ ] Peer-Review-Filter in relevanten Datenbanken gesetzt (EBSCO, JSTOR)
- [ ] Englische und deutsche Suchbegriffe beide probiert

### Quellenverwaltung

- [ ] Alle relevanten Quellen in Zotero gesammelt
- [ ] PDFs in Zotero hinterlegt (nicht nur Metadaten)
- [ ] Better BibTeX Export mit "Keep updated" aktiviert
- [ ] `bibliography.bib` liegt in `thesen/<name>/bibliography.bib`
- [ ] Alle PDF-Dateien in `thesen/<name>/pdfs/` kopiert

### Corpus-Aufbau

- [ ] `python -m rag index --thesis <name>` erfolgreich durchgelaufen (Exit Code 0)
- [ ] `python -m rag corpus --thesis <name> --pretty` zeigt alle erwarteten Quellen
- [ ] Bibkey-Linking erfolgreich: `bibkey_linking.linked` > 0 in der Index-Ausgabe
- [ ] Warnungen im Index-Output geprueft: keine ungeloesten `page_offset_low_confidence`-Fehler

### Schreibvorbereitung

- [ ] Fuer jedes geplante Theorie-Konzept: `python -m rag search "<konzept>" --thesis <name>` einmal testhalber ausgefuehrt
- [ ] Mindestens ein `citation_suggestion` ist nicht null (Beweis, dass Bibkey-Linking funktioniert)
- [ ] `python -m rag extract-citations --thesis <name> --tex tex/main.tex --check-bib --check-corpus` eingerichtet als finaler Pruefschritt

---

*Erstellt fuer das Bachelorarbeits-System. Gueltig ab v0.1.2.*

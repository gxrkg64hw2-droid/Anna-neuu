# Zitierweisen in DACH-Bachelorarbeiten

Dieses Dokument beschreibt die gaengigen Zitierweisen fuer Bachelorarbeiten im
deutschsprachigen Raum. Es enthaelt Beispiele, BibLaTeX-Konfigurationen und
Hinweise zur Arbeit mit dem Bachelorarbeits-System.

---

## Uebersicht

| Zitierweise | Kurzbeschreibung | Typische Fakultaeten |
|---|---|---|
| APA-DE | Autor-Jahr in Klammern, englische Terminologie angepasst | Psychologie, Sozialwissenschaften, Paedagogik |
| Harvard-DE | Autor-Jahr, deutsche Terminologie ("u. a.") | BWL, VWL, Wirtschaftsinformatik |
| Deutsche Zitierweise (Fussnoten) | Vollbeleg in Fussnote, Kurztitel bei Wiederholung | Rechtswissenschaft, Geschichte, Germanistik |
| DIN 1505-2 | Nummeriert, eckige Klammern | Ingenieurwissenschaften, manche FHs |

Wenn der Lehrstuhl keine Vorgabe macht: APA-DE fuer empirische Arbeiten,
Harvard-DE fuer betriebswirtschaftliche Arbeiten.

---

## APA-DE im Text

Grundformat: `(Nachname, Jahr, S. X)` fuer direktes Zitat,
`(vgl. Nachname, Jahr, S. X)` fuer Paraphrase.

```latex
% Direktes Zitat:
\parencite[S.~14]{mueller2021ki}
% Ergebnis: (Mueller, 2021, S. 14)

% Paraphrase mit "vgl.":
\parencite[vgl.][S.~23]{mueller2021ki}
% Ergebnis: (vgl. Mueller, 2021, S. 23)

% Autor im Satzfluss:
\textcite[S.~23]{mueller2021ki} zeigt, dass ...
% Ergebnis: Mueller (2021, S. 23) zeigt, dass ...

% Ab drei Autoren sofort et al.:
\parencite[S.~45]{jones2020survey}
% Ergebnis: (Jones et al., 2020, S. 45)
```

---

## APA-DE Bibliographieformat

**Monographie** (`@book`): `author`, `title`, `year`, `publisher`, `address`, `doi`.
Eintrag: `Mueller, H. (2021). Einfuehrung in die Kuenstliche Intelligenz. Springer.`

**Sammelbandkapitel** (`@incollection`): `author`, `title`, `booktitle`, `editor`, `pages`, `year`, `publisher`.
Eintrag: `Schmidt, A. (2019). NLP im Ueberblick. In K. Weber (Hrsg.), Handbuch der Digitalisierung (S. 101-130). de Gruyter.`

**Zeitschriftenartikel** (`@article`): `author`, `title`, `journal`, `volume`, `pages`, `year`, `doi`.
Eintrag: `Jones, P., Brown, L., & Clark, M. (2020). A Survey of RAG. Journal of AI Research, 68, 120-158.`

**Online-Quelle** (`@online`): `author`, `title`, `year`, `url`, `urldate`.

```bibtex
@online{statista2025chatbots,
  author  = {{Statista}},
  title   = {Nutzung von Chatbots in deutschen Unternehmen 2025},
  year    = {2025},
  url     = {https://de.statista.com/statistik/daten/studie/123456/},
  urldate = {2025-03-15}
}
```

---

## Harvard-DE im Text

Harvard-DE funktioniert wie APA-DE, aber mit deutschen Konventionen.

```latex
% Direktes Zitat (kein Komma zwischen Autor und Jahr):
\parencite[S.~14]{mueller2021ki}
% Ergebnis (mit ext-authoryear): (Mueller 2021, S. 14)

% Paraphrase:
\parencite[vgl.][S.~23]{mueller2021ki}
% Ergebnis: (vgl. Mueller 2021, S. 23)

% Drei und mehr Autoren mit "u. a." statt "et al.":
\parencite[S.~45]{jones2020survey}
% Ergebnis: (Jones u. a. 2020, S. 45)
```

Bibliographieformat identisch mit APA-DE. "Hrsg." statt "Eds.", "u. a." fuer
mehrere Autoren. Konsistenz innerhalb der Arbeit halten.

---

## Deutsche Zitierweise (Fussnoten)

Quellen werden in Fussnoten belegt. Im Fliessttext keine Klammern.

**Erster Beleg: Vollreferenz in der Fussnote:**

```
¹ Hans Mueller, Einfuehrung in die Kuenstliche Intelligenz, Berlin: Springer
  2021, S. 14.
```

**Folgebeleg desselben Werks: Kurztitel:**

```
² Mueller, Einfuehrung KI, S. 23.
```

**Rueckverweis auf Erstbeleg-Nummer:**

```
³ Mueller (Anm. 1), S. 45.
```

**BibLaTeX-Befehle:**

```latex
% Einzelne Fussnote:
\footcite[S.~14]{mueller2021ki}

% Mehrere Quellen in einer Fussnote:
\footcites[S.~3]{mueller2021ki}[S.~88]{schmidt2019nlp}
```

**Sammelbandkapitel in der Fussnote:**

```
⁴ Anna Schmidt, NLP im Ueberblick, in: Klaus Weber (Hrsg.), Handbuch der
  Digitalisierung, Berlin: de Gruyter 2019, S. 101-130, hier S. 115.
```

---

## DIN 1505-2

Verbreitet an technischen Hochschulen. Quellen nummeriert in eckigen Klammern:
`[3]` oder `[3, S. 14]`. Mehrere Quellen: `[3, 7, 12]`.

```latex
\usepackage[
  backend=biber,
  style=numeric-comp,   % Nummernlisten komprimieren: [1-3] statt [1,2,3]
  language=ngerman,
  sortlocale=de_DE,
  sorting=none          % Reihenfolge des Erscheinens (Vancouver-Variante)
]{biblatex}
```

---

## BibLaTeX-Setup

**APA-DE (Standardempfehlung):**

```latex
\usepackage[
  backend=biber,        % Biber statt BibTeX: Unicode, modernes Sortierer
  style=apa,            % APA 7th edition
  language=ngerman,     % Ausgabe auf Deutsch: "Hrsg.", "Aufl." etc.
  sortlocale=de_DE,     % Alphabetisch nach deutschem Locale
  natbib=true,          % Kompatibilitaet mit \citet, \citep
  url=false,            % URLs nicht anzeigen (ausser @online-Eintraege)
  doi=true,             % DOIs anzeigen
  eprint=false          % arXiv-IDs nicht anzeigen
]{biblatex}
\addbibresource{bibliography.bib}
```

**Harvard-DE:**

```latex
\usepackage[
  backend=biber,
  style=ext-authoryear,
  language=ngerman,
  sortlocale=de_DE,
  maxcitenames=2,       % Ab 3 Autoren sofort "u. a." im Text
  maxbibnames=99        % Alle Autoren im Literaturverzeichnis
]{biblatex}
% "u. a." statt "et al." aktivieren:
\DefineBibliographyStrings{ngerman}{andothers = {u.\,a\adddot}}
```

**Fussnotenstil (Deutsche Zitierweise):**

```latex
\usepackage[
  backend=biber,
  style=verbose-trad2,  % Vollbeleg beim Erstnachweis, Kurztitel danach
  language=ngerman,
  sortlocale=de_DE,
  ibidtracker=constrict % "Ebd." nur bei direkt aufeinanderfolgenden Zitaten
]{biblatex}
% Alternativ: style=footnote-dw (Paket biblatex-dw)
```

**DIN 1505-2:**

```latex
\usepackage[
  backend=biber,
  style=ext-numeric,
  language=ngerman
]{biblatex}
```

---

## Page-prefix-Konventionen (Deutsch)

| Angabe | Bedeutung | Hinweis |
|---|---|---|
| `S. 23` | Einzelne Seite | Standardfall |
| `S. 23 f.` | Seiten 23 und 24 (genau zwei) | Nur bei exakt zwei Seiten |
| `S. 23 ff.` | Seite 23 und folgende (unbestimmt) | Viele Lehrstuehle bevorzugen expliziten Bereich |
| `S. 23-25` | Seitenbereich | Bevorzugte Alternative zu "ff." |
| `vgl.` | Vor Autor-Jahr: Paraphrase, kein woertliches Zitat | `(vgl. Mueller, 2021, S. 23)` |
| `zitiert nach` | Sekundaerzitat | Nur wenn Originalquelle nachweislich nicht beschaffbar |

```latex
\parencite[S.~23]{key}           % einzelne Seite
\parencite[S.~23\,f.]{key}       % zwei Seiten
\parencite[S.~23--25]{key}       % Bereich (bevorzugt)
\parencite[vgl.][S.~23]{key}     % Paraphrase
```

---

## "et al." vs "u. a."

| Stil | Abkuerzung | Schreibweise |
|---|---|---|
| APA-DE | `et al.` | Roman (nicht kursiv) |
| Harvard-DE | `u. a.` | Roman |
| Deutsche Zitierweise | Vollstaendige Liste in Fussnote oder "u. a." | Je nach Lehrstuhlvorgabe |
| DIN 1505-2 | `u. a.` oder `et al.` | Norm schreibt kein Kursiv vor |

Innerhalb einer Arbeit konsistent bleiben. Kein Wechsel zwischen "et al."
und "u. a." in derselben Arbeit.

BibLaTeX: "u. a." global aktivieren:

```latex
\DefineBibliographyStrings{ngerman}{andothers = {u.\,a\adddot}}
```

---

## Online-Quellen

Online-Quellen erfordern immer ein Zugriffsdatum. Ohne `urldate` ist der
Beleg wissenschaftlich nicht verwertbar.

Im Text (APA-DE): `(Statista, 2025)` oder `(Statista, 2025, online)`

BibTeX:

```bibtex
@online{statista2025chatbots,
  author  = {{Statista}},
  title   = {Anteil der Unternehmen, die KI-Chatbots einsetzen, 2025},
  year    = {2025},
  url     = {https://de.statista.com/statistik/daten/studie/123456/},
  urldate = {2025-03-15}
}
```

Hinweise:
- Koerperschaft als Autor: doppelte geschweifte Klammern `{{Statista}}`.
- `year`: Jahr der Erhebung oder letzten Aktualisierung, nicht das Abrufdatum.
- URLs gehoeren ins Literaturverzeichnis, nicht in den Fliessttext.

Fussnotenstil:

```
⁵ Statista, Anteil der Unternehmen..., https://de.statista.com/... (Stand: 15.03.2025).
```

---

## Sekundaerzitate

Format (APA-DE): `(Mueller, 2010, zit. nach Schmidt, 2023, S. 45)`

```latex
% Manuell im Text:
(Mueller 2010, zit.\,nach \citealt[S.~45]{schmidt2023})
```

Empfehlung: Sekundaerzitate in Bachelorarbeiten vermeiden. Die meisten
Originalquellen sind ueber Bibliothekszugaenge, Google Scholar, Unpaywall
oder ResearchGate zugaenglich. Wenn die Originalquelle nicht beschaffbar ist,
das Sekundaerzitat begruenden.

---

## Zusammenarbeit mit dem Bachelorarbeits-System

Nach `python -m rag index --thesis <name>` enthaelt jeder Suchtreffer das
Feld `citation_suggestion` mit einem fertig formatierten BibLaTeX-String:

```json
{
  "citation_suggestion": "\\parencite[S. 14]{mueller2021ki}"
}
```

Diesen String direkt in den LaTeX-Quelltext einfuegen. Das System hat den
Druckseiten-Offset bereits berechnet.

Regeln:

1. `citation_suggestion` nicht manuell korrigieren, ausser
   `print_offset_confidence` ist kleiner als 0.7. Dann Seite im Original
   verifizieren.
2. Quellen ausserhalb des Corpus (z. B. Webstatistiken): manuell einen
   `@online`-Eintrag in `bibliography.bib` anlegen.
3. Niemals Zitationen erfinden. Wenn `verify-quote` `NO_MATCH` und `search`
   keinen Treffer liefert, gibt es keine Quelle im Corpus.
4. Paraphrase vor dem Speichern pruefen:

```bash
python -m rag verify-quote \
  --text "RAG-Systeme verbinden Sprachmodelle mit externem Wissen." \
  --thesis <name>
```

---

## Checkliste vor Abgabe

- [ ] Eine Zitierweise konsistent durchgehalten (kein Stilmix)
- [ ] Alle Zitate haben Seitenzahlen (sofern Quelle paginiert)
- [ ] Bibliographie alphabetisch nach Erstautorenachname sortiert
- [ ] DOIs vorhanden, wo verfuegbar
- [ ] Online-Quellen mit Stand-Datum (`urldate` in BibTeX)
- [ ] "ff." durch expliziten Seitenbereich ersetzt oder Lehrstuhlvorgabe geprueft
- [ ] "et al." vs "u. a." konsistent in der gesamten Arbeit
- [ ] Sekundaerzitate begruendet und als solche gekennzeichnet
- [ ] Abschlusspruefung mit dem Bachelorarbeits-System:

```bash
python -m rag extract-citations \
  --tex tex/main.tex \
  --thesis <name> \
  --check-bib \
  --check-corpus \
  --check-orphans \
  --strict
# Erwartetes Ergebnis: Exit-Code 0, 0 Issues
```

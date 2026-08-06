# Deutsche Konventionen fuer scientific-visualization

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen.

## Skill-spezifische DACH-Adaption

### Beschriftungssprache

Charts in deutschsprachigen BAs haben deutsche Achsenbeschriftungen, deutsche Legenden-Eintraege, deutsche Caption-Texte. Englisch nur, wenn die gesamte Arbeit englisch geschrieben ist.

### Caption-Konvention

- Tabellen: Caption darueber. Format: "Tabelle 4.2: Stichprobenbeschreibung".
- Abbildungen: Caption darunter. Format: "Abbildung 5.1: Pfaddiagramm des Strukturmodells".
- Nummerierung kapitelweise (4.2 = Kapitel 4, zweite Tabelle).
- Quellenangabe in der Caption: "(eigene Darstellung)" oder "(in Anlehnung an Mueller, 2023, S. 12)" oder Zitierung.

### Farbkonventionen

- Colorblind-friendly Palette aus K-Dense `references/color_palettes.md` (Viridis-aehnlich).
- Keine Rot-Gruen-Kombination ohne zusaetzliches Encoding (Form, Schraffur).
- Schwarz-Weiss-tauglich pruefen: Druckversion einer BA wird oft schwarz-weiss kopiert.

### DPI und Format

- Vektor-Formate (PDF, EPS) bevorzugen fuer LaTeX.
- Raster (PNG) nur bei Photos, mindestens 300 DPI.
- `figure_export.py` aus K-Dense `scripts/` ist behalten worden, hilft bei Mehrformat-Export.

### Komma als Dezimaltrennzeichen

In deutschen Charts: Achsenticks "23,5" statt "23.5". Mit matplotlib via `matplotlib.ticker.FuncFormatter` und `lambda x, _: f"{x:.1f}".replace(".", ",")`.

### Verbindung zum LaTeX-Workflow

Wenn ein Chart in `thesen/<name>/figures/<chart>.pdf` liegt, einbinden via `\includegraphics` mit `\caption` und `\label`. Im `_common`-Layer sind Caption-Macros vordefiniert.

### Cross-References fuer diese Skill

- `references/color_palettes.md` (Original)
- `references/journal_requirements.md` (Original)
- `references/publication_guidelines.md` (Original)
- `references/matplotlib_examples.md` (Original)
- `scripts/figure_export.py` (behalten, nutzbar)
- `scripts/style_presets.py` (behalten, nutzbar)

## Cross-References zu anderen DACH-Files

- DACH-Reporting-Standards: `references/dach_reporting_standards.md` (in statistical-analysis und peer-review)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Charts visualisieren Daten aus dem Korpus oder eigene Erhebungen. Bei Daten aus dem Korpus: rag search liefert die Quelle, die in die Caption gehoert.

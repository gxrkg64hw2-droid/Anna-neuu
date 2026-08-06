# Deutsche Konventionen fuer market-research-reports

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen.

## Skill-spezifische DACH-Adaption

### Wann diese Skill genutzt wird

Marketing- und BWL-BAs mit Marktanalyse-Kapitel. Die Skill ist NICHT fuer eigenstaendige McKinsey-Stil-Reports gedacht, sondern liefert die strategischen Frameworks (Porter, PESTLE, SWOT, BCG) als Strukturgeber fuer einzelne Kapitel oder Abschnitte.

### Integration mit dem `marketing-case-study`-LaTeX-Profil

Das Profil bringt vorbereitete TikZ-Templates fuer:
- Porter Five Forces (Pentagon mit beschrifteten Ecken)
- BCG-Matrix (4-Felder-Quadrant)
- SWOT-Quadrant
- TAM/SAM/SOM (konzentrische Kreise)

Diese werden NICHT durch K-Dense-Scripts generiert (die wurden gestrippt), sondern aus den Profil-Templates befuellt.

### Datenquellen fuer DACH-Marktanalysen

- Statista (kostenpflichtig, viele Hochschulen haben Lizenz)
- Destatis (Statistisches Bundesamt, Deutschland, kostenlos)
- Eurostat (EU)
- wiso (GENIOS) fuer Wirtschaftspresse-Snippets mit Marktzahlen
- Branchenverbaende (z.B. BVDW fuer Digital, BVR fuer Verbraucher)
- Brave MCP / Firecrawl MCP fuer aktuelle 2025/2026-Daten, die nicht in Datenbanken sind. Zitieren als `@online` mit URL und Stand-Datum.

### Sprache: kein Consulting-Buzzword-Bullshit

Die K-Dense SKILL.md tendiert zu McKinsey-Sprache ("disruption", "leverage synergies"). In einer DACH-BA wirkt das schnell unwissenschaftlich. Ueberarbeite Buzzword-Saetze in nuechtern-deutsche akademische Sprache.

### Pflichtangaben pro Markt-Statistik

Jede Marktzahl in der BA enthaelt:
- Wert (z.B. "12,3 Mrd. Euro")
- Bezugsjahr ("im Jahr 2025")
- Geographische Abgrenzung ("in Deutschland")
- Quelle mit Citation
- Stand-Datum, falls aus Online-Quelle

### Cross-References fuer diese Skill

- `references/report_structure_guide.md` (Original, englisch)
- `references/data_analysis_patterns.md` (Original, englisch)
- `references/visual_generation_guide.md` (Original, englisch)

## Cross-References zu anderen DACH-Files

- DACH-Zitierweisen: `references/dach_zitierweisen.md` (in scientific-writing)
- DACH-Reporting-Standards: `references/dach_reporting_standards.md` (in statistical-analysis)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Marktdaten kommen oft NICHT aus dem Korpus, sondern via Brave/Firecrawl MCPs. Die Bridge-Skill verlangt URL und Stand-Datum bei jeder Online-Quelle und legt einen `@online`-Eintrag in `bibliography.bib` an.

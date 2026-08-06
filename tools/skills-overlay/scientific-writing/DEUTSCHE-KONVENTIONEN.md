# Deutsche Konventionen fuer scientific-writing

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest. Bei englischsprachigen Texten kannst du die Hinweise hier ignorieren und auf die Hauptinhalte der SKILL.md zurueckgreifen.

## Typographische Grundregeln (gilt fuer alle deutschen Texte)

- Umlaute IMMER korrekt: oe ae ue ss als Ersatz sind verboten ausser in URLs oder DOIs.
- Em-Dash und En-Dash sind absolut verboten. Stattdessen: Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen: deutsche Form via `\enquote{...}` aus dem `csquotes`-Paket.
- Komma als Dezimaltrennzeichen im Fliesstext (4,23). In Tabellen darf konsistent Punkt verwendet werden, wenn das ganze Manuskript so verfaehrt.

## Skill-spezifische DACH-Adaption

### IMRAD vs klassisch deutsch

K-Dense' SKILL.md schlaegt IMRAD-Struktur vor (Introduction, Methods, Results, And Discussion). Fuer eine DACH-Bachelorarbeit ist das nicht zwingend. Klassisch deutsche Struktur:

1. Einleitung (Problemstellung, Forschungsfrage, Zielsetzung, Aufbau)
2. Theoretischer Rahmen / Grundlagen
3. Methodik bei empirischen Arbeiten
4. Ergebnisse bei empirischen Arbeiten
5. Diskussion / Synthese
6. Fazit

Wenn die Hochschule keine Vorgabe macht: an die klassisch deutsche Struktur halten. Reine IMRAD-Struktur ist im DACH-Kontext eher fuer Tagungspaper als fuer Abschlussarbeiten.

### Two-stage outline-to-prose auf Deutsch

Stufe 1: Outline mit Kernaussagen pro Absatz, Stichpunkt-Form. JEDE Aussage bekommt einen Marker `[QUELLE: <konzept>]` als Reminder, dass dafuer eine Korpus-Suche faellig ist.

Stufe 2: Umsetzung in Fliessprosa, Stichpunkte werden zu vollstaendigen deutschen Saetzen mit korrekter Grammatik. WICHTIG: in Stufe 2 wird fuer jede `[QUELLE: ...]`-Markierung der Bridge-Skill-Workflow ausgefuehrt: `python -m rag search "<konzept>"` und `citation_suggestion` einsetzen.

### Stilhinweise

- Aktivsatz bevorzugt, Passive nur wo idiomatisch.
- Ich-Form mit Erstpruefer abklaeren. Tendenz 2026: in Methodik und Diskussion zunehmend akzeptiert.
- Nominalisierungen sparsam, Verbalstil oft klarer.
- Faustregel: max 25 Worte pro Satz.

### Zitate

- Direktes Zitat unter 40 Worten: "..." (Autor, Jahr, S. X) oder via `\parencite[S. X]{key}`.
- Direktes Zitat ab 40 Worten: Blockzitat ohne Anfuehrungszeichen, eingerueckt.
- Bei Auslassungen im Zitat: `[...]` (vier Zeichen, mit Leerzeichen davor und danach).

### Verbindung zu vorhandenen Werkzeugen

Die SKILL.md beschreibt einen `\parencite`-aehnlichen Befehl. In dieser Codebase ist das exakt der Stil, den `python -m rag search` als `citation_suggestion` zurueckgibt. NIEMALS Citations manuell konstruieren.

### Cross-References fuer diese Skill

- `references/dach_zitierweisen.md`: konkrete Zitierstile
- `references/dach_thesis_conventions.md`: gesamte BA-Konventionen
- `references/imrad_structure.md` (Original K-Dense, englisch): wenn IMRAD-Struktur gewaehlt wurde
- `references/writing_principles.md` (Original K-Dense, englisch): universelle Schreibprinzipien

## Cross-References zu anderen DACH-Files

- DACH-Zitierweisen: `references/dach_zitierweisen.md`
- DACH-Recherche: `references/dach_recherche.md` (in literature-review)
- DACH-Konventionen Bachelorarbeit: `references/dach_thesis_conventions.md`
- DACH-Reporting-Standards: `references/dach_reporting_standards.md` (in statistical-analysis und peer-review)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Repo-eigenen Bridge-Skill `bachelorarbeit-arbeitsweise`. Die Bridge-Skill orchestriert den Workflow: rag search vor jeder Aussage, verify-quote nach jedem Absatz, extract-citations vor jedem Commit. Diese Skill liefert das wissenschaftliche Schreibhandwerk; die Bridge-Skill verdrahtet es mit dem Korpus.

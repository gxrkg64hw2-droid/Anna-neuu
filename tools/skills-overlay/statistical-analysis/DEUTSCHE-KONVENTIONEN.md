# Deutsche Konventionen fuer statistical-analysis

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen im Fliesstext (Achtung: in APA-Tabellen mit p-Werten oft Punkt; pro Manuskript konsistent).

## Skill-spezifische DACH-Adaption

### Reporting nach APA-DE

Siehe `references/dach_reporting_standards.md` fuer ausfuehrliche Beispiele. Kurz:

- Komma als Dezimaltrennzeichen in deutschem Fliesstext.
- p < .001 statt p = 0,000.
- Effektgroessen IMMER mitberichten.
- Pruefgroessen-Format: t(df), F(df1, df2), chi^2(df, N=).

### Mayring qualitative Inhaltsanalyse

Wenn die BA qualitative Daten hat (Interviews, offene Fragebogenantworten), ist Mayring der DACH-Standard. Detaillierte Reporting-Vorgaben in `references/dach_reporting_standards.md`.

### Tools im DACH-Kontext

- R mit `lavaan` fuer SEM, `psych` fuer Reliabilitaet
- SmartPLS 4 fuer PLS-SEM
- SPSS noch verbreitet an einigen Hochschulen
- MAXQDA, ATLAS.ti, f4analyse fuer qualitative Auswertung

Reporting in der BA enthaelt Tool-Name + Version.

### Faustregeln Mindeststichprobe

- Quantitative Umfrage mit Strukturgleichungsmodell: n >= 100, besser n >= 200.
- Experiment mit Mediation: n >= 100.
- Faktorenanalyse: 5 bis 10 Faelle pro Item, mindestens n = 100.
- Qualitative Interviews: Saettigungspunkt, oft 8 bis 15 fuer eine BA.

Kommunizieren als "An der Befragung nahmen N = 187 Studierende teil".

### Cross-References fuer diese Skill

- `references/dach_reporting_standards.md`
- `references/effect_sizes_and_power.md` (Original, englisch)
- `references/test_selection_guide.md` (Original, englisch)
- `references/assumptions_and_diagnostics.md` (Original, englisch)
- `references/bayesian_statistics.md` (Original, englisch)

## Cross-References zu anderen DACH-Files

- DACH-Reporting-Standards: `references/dach_reporting_standards.md`

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Statistische Aussagen brauchen Theorie-Quellen aus dem Korpus (`rag search`) und Effektgroessen-Konventionen aus den Originalstudien. Die Bridge-Skill verdrahtet beides mit dem Schreibworkflow.

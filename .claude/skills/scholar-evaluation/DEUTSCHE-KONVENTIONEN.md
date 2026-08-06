# Deutsche Konventionen fuer scholar-evaluation

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen.

## Skill-spezifische DACH-Adaption

### Selbst-Audit vor Abgabe

Diese Skill ist die naheliegendste Anwendung im DACH-BA-Workflow: Selbst-Bewertung der eigenen Arbeit kurz vor Abgabe. Das ScholarEval-Framework gibt strukturiertes Feedback in vier Dimensionen:

1. Problemformulierung (Forschungsfrage klar? Relevanz begruendet?)
2. Methodik (geeignete Wahl? sauber dokumentiert?)
3. Analyse (Tiefe? kritische Auseinandersetzung?)
4. Schreibqualitaet (Klarheit, Argumentationsstruktur)

### Selbst-Audit-Workflow

1. Kapitel komplett durchschreiben.
2. ScholarEval-Skill auf das Kapitel anwenden.
3. Niedrig-bewertete Bereiche identifizieren.
4. Gezielt ueberarbeiten.
5. Zweite Evaluation, dann commit.

### Bewertungsstandards der DACH-Hochschulen

Typische Notenskala (1.0 bis 4.0, unter 4.0 nicht bestanden):

| Note | Bezeichnung |
|---|---|
| 1.0 bis 1.3 | sehr gut |
| 1.7 bis 2.3 | gut |
| 2.7 bis 3.3 | befriedigend |
| 3.7 bis 4.0 | ausreichend |

Gute BA-Standards (Note 1.5 oder besser):
- Forschungsfrage praezise
- Methodik replizierbar
- Theoretischer Rahmen kritisch synthetisiert (nicht aufgereiht)
- Limitationen ehrlich behandelt
- Sprache: max 25 Worte/Satz, Aktivsatz, keine Buzzwords

### Cross-References fuer diese Skill

- `references/evaluation_framework.md` (Original, englisch)

## Cross-References zu anderen DACH-Files

- DACH-Konventionen Bachelorarbeit: `references/dach_thesis_conventions.md` (in scientific-writing)
- DACH-Zitierweisen: `references/dach_zitierweisen.md` (in scientific-writing)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Vor dem Selbst-Audit sollte `python -m rag extract-citations --tex tex/main.tex --thesis <name> --check-bib --check-corpus --check-orphans --strict` mit Exit-Code 0 durchgelaufen sein. Ohne saubere Citation-Hygiene macht das ScholarEval keinen Sinn.

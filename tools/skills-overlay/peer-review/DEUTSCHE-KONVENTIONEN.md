# Deutsche Konventionen fuer peer-review

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen.

## Skill-spezifische DACH-Adaption

### Selbst-Review vor Abgabe

Hauptanwendung in DACH-BA-Kontext: strukturiertes Selbst-Review der eigenen Arbeit kurz vor Abgabe. Das ergaenzt das ScholarEval-Scoring (`scholar-evaluation`-Skill) um inhaltliche Pruefkriterien:

- Forschungsfrage und Zielsetzung kongruent?
- Theoretischer Rahmen liefert die noetigen Bausteine fuer die Methodik?
- Methodik passt zur Forschungsfrage?
- Ergebnisdarstellung sauber, ohne Ueberinterpretation?
- Diskussion verbindet Ergebnisse mit Theorie und vorigem Forschungsstand?
- Limitationen ehrlich?
- Fazit beantwortet die Forschungsfrage?

### CONSORT, STROBE und andere Reporting-Standards

CONSORT (Randomized Trials), STROBE (Beobachtungsstudien), PRISMA (systematische Reviews) sind primaer medizinische Standards. In DACH-BWL/Marketing gilt:

- Bei quantitativen Umfragen: APA-Reporting (siehe `references/dach_reporting_standards.md`).
- Bei qualitativen Interviews: COREQ-Checkliste oder SRQR.
- Bei Mayring: Mayring-spezifische Reporting-Punkte (siehe `references/dach_reporting_standards.md`).

### Tone-Konvention auf Deutsch

DACH-Pruefer erwarten konstruktiv-kritisch, nicht zerstoererisch. Zwischen "diese Arbeit zeigt Schwaechen in..." und "diese Arbeit hat fundamentale Methodendefizite" liegt Welten. Selbst-Review sollte Verbesserungsvorschlaege machen, nicht nur Maengel auflisten.

### Pre-Abgabe-Checkliste

- [ ] Forschungsfrage in Einleitung und Fazit identisch formuliert
- [ ] Alle Methodik-Entscheidungen begruendet, nicht nur beschrieben
- [ ] Ergebnisse vollstaendig (keine Auswahl ohne Begruendung)
- [ ] Diskussion vergleicht mit vorigem Forschungsstand explizit
- [ ] Limitationen behandeln Methodik, Theorie und Praxis
- [ ] `python -m rag extract-citations --tex tex/main.tex --thesis <name> --check-bib --check-corpus --check-orphans --strict` Exit-Code 0
- [ ] Sprache: keine em-Dashes, korrekte Umlaute, Komma als Dezimaltrennzeichen
- [ ] Eidesstattliche Erklaerung unterschrieben

### Cross-References fuer diese Skill

- `references/dach_reporting_standards.md`
- `references/common_issues.md` (Original, englisch)
- `references/reporting_standards.md` (Original, englisch)

## Cross-References zu anderen DACH-Files

- DACH-Reporting-Standards: `references/dach_reporting_standards.md`
- DACH-Zitierweisen: `references/dach_zitierweisen.md` (in scientific-writing)
- DACH-Konventionen Bachelorarbeit: `references/dach_thesis_conventions.md` (in scientific-writing)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Vor jedem Selbst-Review sollte das System einen Citation-Audit gemacht haben (extract-citations --strict). Ohne sauberes Citation-Profil ist ein Peer-Review-Ergebnis nicht aussagekraeftig.

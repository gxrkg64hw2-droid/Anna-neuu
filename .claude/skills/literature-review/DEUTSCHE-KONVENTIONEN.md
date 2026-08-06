# Deutsche Konventionen fuer literature-review

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash absolut verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen.

## Skill-spezifische DACH-Adaption

### Datenbanken-Reihenfolge fuer DACH-BA

Die K-Dense SKILL.md fokussiert PubMed, arXiv, Semantic Scholar, bioRxiv. Diese sind im naturwissenschaftlichen Bereich richtig. Fuer DACH-BWL/Marketing/Wirtschaft ist die Reihenfolge:

1. OpenAlex (kostenlos, breit, 250M+ Records) als erster Sweep.
2. wiso (GENIOS) fuer deutschsprachige BWL/Wirtschaftsfachzeitschriften und Wirtschaftspresse.
3. EBSCO Business Source und JSTOR fuer internationale Fachzeitschriften.
4. Beck-Online wenn rechtliche Aspekte vorkommen.
5. Google Scholar fuer Snowballing und Lueckenpruefung, mit Vorsicht.

### Theoretischer Rahmen vs Literature Review

In DACH-BAs ist das Kapitel "Theoretischer Rahmen" KEIN klassisches Literature Review im PRISMA-Sinne. Es synthetisiert Theorien und stellt sie in Beziehung zur eigenen Forschungsfrage. Es enthaelt:

- Kernkonzepte und Definitionen
- Modelle und Theorien (z.B. Diffusion of Innovations, TAM, S-O-R)
- Empirische Erkenntnisse, kritisch gewuerdigt, nicht aufgereiht
- Forschungsluecke, die die eigene Arbeit adressiert

Wenn die BA explizit eine "systematische Literaturuebersicht" als Methode hat, dann gilt PRISMA. Sonst nicht.

### Suchprotokoll-Pflicht

Auch wenn keine PRISMA-Struktur: bei DACH-BAs erwarten Pruefer in der Methodik oder im Anhang ein dokumentiertes Suchprotokoll. Tabelle: Datum, DB, Suchstring, Treffer, relevant.

### Snowballing in deutschen BAs

Forward (Citation Tracking via Google Scholar) und backward (Literaturlisten relevanter Werke abklopfen) gehoeren zu jeder ernsthaften DACH-BA-Recherche. Beide explizit erwaehnen.

### Verbindung zum Bachelorarbeits-System

- Die Skill liefert die STRUKTUR der Synthese.
- `python -m rag search` liefert die TREFFER mit Seitenzahlen.
- Zitate IMMER via `citation_suggestion` aus dem Search-Output, niemals manuell konstruieren.

### Cross-References fuer diese Skill

- `references/dach_recherche.md`: konkrete DACH-Datenbanken und Such-Workflow
- `references/dach_zitierweisen.md` (in scientific-writing): Zitierstile
- `references/database_strategies.md` (Original, englisch): allgemeine Suchstrategien

## Cross-References zu anderen DACH-Files

- DACH-Recherche: `references/dach_recherche.md`
- DACH-Zitierweisen: `references/dach_zitierweisen.md` (in scientific-writing)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Die Bridge-Skill orchestriert den Workflow: rag search vor jeder Aussage, verify-quote nach jedem Absatz. Diese Skill liefert die Synthese-Struktur; das RAG-System liefert die verifizierten Quellen.

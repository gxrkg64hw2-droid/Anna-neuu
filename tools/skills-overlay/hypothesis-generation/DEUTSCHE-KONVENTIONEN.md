# Deutsche Konventionen fuer hypothesis-generation

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest.

## Typographische Grundregeln

- Umlaute IMMER korrekt.
- Em-Dash und En-Dash verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}`.
- Komma als Dezimaltrennzeichen.

## Skill-spezifische DACH-Adaption

### Wann Hypothesen in einer DACH-BA verlangt werden

Empirische BAs (deduktiv-quantitativ): Hypothesen MUESSEN explizit formuliert sein, bevor die Methodik beschrieben wird. Pruefer erwarten H0/H1-Notation oder bei mehreren Hypothesen H1, H2, ... mit Begruendung jeder einzelnen aus Theorie.

Qualitative BAs: keine Hypothesen, sondern Forschungsfragen oder "leitende Annahmen".

### Strukturgleichungsmodelle als typischer DACH-Kontext

In Marketing/BWL ist PLS-SEM (Partial Least Squares Structural Equation Modeling) sehr verbreitet, vor allem fuer Modelle mit latenten Konstrukten (z.B. Markenvertrauen, Kundenzufriedenheit). Hypothesen werden hier als Pfade im Modell visualisiert (`H1: Konstrukt A -> Konstrukt B (positiv)`).

Standardwerk: Hair, Hult, Ringle, Sarstedt (2022). A Primer on Partial Least Squares Structural Equation Modeling (PLS-SEM). 3rd ed. SAGE.

### TAM und S-O-R als typische Theorien

Marketing/AI-Marketing-BAs nutzen oft:

- TAM (Technology Acceptance Model, Davis 1989): perceived usefulness und perceived ease of use beeinflussen die Nutzungsintention.
- UTAUT/UTAUT2 (Venkatesh et al. 2003/2012): erweiterte Akzeptanztheorie.
- S-O-R (Stimulus-Organism-Response, Mehrabian und Russell 1974): Reizverarbeitung beim Konsumenten.

Hypothesen werden aus solchen Theorien deduziert.

### Hypothesen-Formulierungs-Patterns auf Deutsch

- Wirkungshypothese: "H1: Je hoeher die wahrgenommene Nuetzlichkeit eines Chatbots, desto hoeher die Nutzungsintention."
- Vergleichshypothese: "H1: Nutzer mit hoher Tech-Affinitaet weisen eine staerkere Nutzungsintention auf als Nutzer mit niedriger Tech-Affinitaet."
- Mediator-Hypothese: "H3: Vertrauen mediiert den Effekt von Transparenz auf Nutzungsintention."
- Moderator-Hypothese: "H4: Der Effekt von wahrgenommener Nuetzlichkeit auf Nutzungsintention wird durch Datenschutzbedenken moderiert."

### Cross-References fuer diese Skill

- `references/experimental_design_patterns.md` (Original, englisch)
- `references/hypothesis_quality_criteria.md` (Original, englisch)
- `references/literature_search_strategies.md` (Original, englisch)

## Cross-References zu anderen DACH-Files

- DACH-Reporting-Standards: `references/dach_reporting_standards.md` (in statistical-analysis)
- DACH-Zitierweisen: `references/dach_zitierweisen.md` (in scientific-writing)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Hypothesen werden aus Theorie deduziert, die im Korpus belegt ist. `python -m rag search` liefert die Theorie-Belege; die Bridge-Skill verdrahtet sie mit dem Schreibworkflow.

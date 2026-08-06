# Deutsche Konventionen fuer scientific-critical-thinking

## Wann diese Datei beachten

Lies diese Datei, wenn du diese Skill auf eine deutschsprachige Bachelorarbeit anwendest. Bei englischsprachigen Texten kannst du die Hinweise hier ignorieren.

## Typographische Grundregeln

- Umlaute IMMER korrekt (oe ae ue ss verboten als Ersatz).
- Em-Dash und En-Dash absolut verboten. Stattdessen Punkt, Komma, Doppelpunkt, Bindestrich (-).
- Anfuehrungszeichen via `\enquote{...}` aus `csquotes`.
- Komma als Dezimaltrennzeichen in deutschem Fliesstext.

## Skill-spezifische DACH-Adaption

### Wo diese Skill in einer DACH-BA Anwendung findet

- Diskussionskapitel: kritische Wuerdigung der eigenen Ergebnisse, Limitationen, Bias-Identifikation.
- Theoretischer Rahmen: kritische Auseinandersetzung mit dem Forschungsstand, nicht nur Aneinanderreihung.
- Bewertung von Quellen waehrend der Recherche: ist diese Studie methodisch belastbar?

### Limitations-Sektion auf Deutsch

In DACH-BAs gehoert eine explizite Limitations-Sektion ans Ende der Diskussion oder ins Fazit. Folgende Punkte muessen behandelt werden:

1. Methodische Limitationen: Stichprobengroesse, Auswahl, Operationalisierungen.
2. Theoretische Limitationen: Generalisierbarkeit, Reichweite der Theorie, ausgeklammerte Mechanismen.
3. Empirische Limitationen bei empirischen Arbeiten: Reliabilitaet, Validitaet, Konfundierung.
4. Praxis-Limitationen: Was kann aus der Arbeit nicht abgeleitet werden?

### GRADE und Cochrane Risk of Bias im DACH-Kontext

GRADE und Cochrane ROB stammen aus der Medizin und sind dort Standard. In BWL/Marketing/Sozialwissenschaften wendet man eher Quality-Frameworks wie:

- Critical Appraisal Skills Programme (CASP) Checklisten
- Joanna Briggs Institute (JBI) kritische Bewertungstools
- Fuer empirische BWL: Whittemore und Knafl (2005) integrative review quality criteria

Verwende GRADE/Cochrane nur, wenn die BA tatsaechlich klinische oder versorgungsforschungsrelevante Themen hat.

### Bias-Typen mit deutschen Bezeichnungen

| Englisch | Deutsch |
|---|---|
| Selection bias | Auswahlverzerrung |
| Confirmation bias | Bestaetigungsfehler |
| Publication bias | Publikationsbias |
| Hawthorne effect | Hawthorne-Effekt |
| Common-method bias | Common-Method-Bias |
| Survivorship bias | Survivorship-Bias |
| Recall bias | Erinnerungsverzerrung |

### Cross-References

- `references/common_biases.md` (Original, englisch)
- `references/logical_fallacies.md` (Original, englisch)
- `references/evidence_hierarchy.md` (Original, englisch)
- `references/scientific_method.md` (Original, englisch)
- `references/statistical_pitfalls.md` (Original, englisch)

## Cross-References zu anderen DACH-Files

- DACH-Reporting-Standards: `references/dach_reporting_standards.md` (in statistical-analysis und peer-review)

## Verbindung zum Bachelorarbeits-System

Diese Skill arbeitet zusammen mit der Bridge-Skill `bachelorarbeit-arbeitsweise`. Die Bridge-Skill orchestriert den Workflow: rag search vor jeder Aussage, verify-quote nach jedem Absatz. Diese Skill liefert die kritischen Bewertungskriterien; die Bridge-Skill verdrahtet sie mit dem Korpus.

---
name: bachelorarbeit-review-structure
description: |
  DE: Review-Skill C für Bachelorarbeits-Kapitel. Prüft Argumentationsfaden innerhalb eines Kapitels, Konsistenz zwischen Kapiteln (Forschungsfrage, Methodik, Begriffe), Vollständigkeit gegen den Plan, methodische Substanz und Lesbarkeit für den Erstprüfer. Wird von der Bridge-Skill `bachelorarbeit-arbeitsweise` nach jedem fertigen Kapitel zwingend ausgelöst.
  EN: Review skill C for Bachelor-thesis chapters. Checks argument flow within a chapter, consistency across chapters (research question, methodology, terminology), completeness against plan, methodological substance, and readability for the first examiner. Triggered mandatorily by the bridge skill after each completed chapter.
allowed-tools: Read Bash Grep
license: MIT
metadata:
  skill-author: Bachelorarbeits-System (Fabian + Claude)
---

# Review-C: Structure & Scientific Logic

## Wann diese Skill aktiv wird

Wird von der Bridge-Skill `bachelorarbeit-arbeitsweise` als Pflicht-Pass nach jedem fertigen Kapitel aktiviert. Besonders relevant vor Betreuer:innen-Terminen.

## Zielsetzung

Sicherstellen, dass der wissenschaftliche Argumentationsbau funktioniert: innerhalb des einzelnen Kapitels, im Verbund mit den anderen Kapiteln und im Verhältnis zu den dokumentierten Vorgaben (Exposé, PROJEKTUEBERSICHT.md, thesen/<name>/CLAUDE.md).

## Prüfdimensionen

### 1. Argumentations-Logik im Kapitel

- Folgt das Kapitel einem klaren roten Faden?
- Sind die Sätze zwischen Absätzen verbunden, oder springt es?
- Werden Begriffe vor ihrer Verwendung eingeführt?
- Gibt es Sätze ohne Beitrag zur Argumentation?
- Sind Zwischenfazits oder Brückensätze an passenden Stellen gesetzt?

### 2. Konsistenz zwischen Kapiteln

- Stimmt die Hauptforschungsfrage in der Einleitung WORTGLEICH mit dem Exposé bzw. der `PROJEKTUEBERSICHT.md` überein?
- Decken sich die Subforschungsfragen in der Einleitung mit den Hauptkategorien im Kategoriensystem-Kapitel? Wenn nicht: ist der Logiksprung erklärt?
- Stimmen die methodischen Aussagen in den Methodik-Kapiteln (Forschungsdesign, Datenerhebung, Kategoriensystem) mit der Methodik-Beschreibung in der Einleitung überein?
- Werden die im Theoriekapitel eingeführten Begriffe in den späteren Kapiteln konsistent verwendet (z.B. dieselbe Definition von „Hate Speech")?
- Werden Cross-References (`\ref{...}`) zwischen Kapiteln korrekt aufgelöst?

### 3. Vollständigkeit gegen den Plan

- Sind alle Sektionen, die das Kapitel-Skelett vorgesehen hat, mit Inhalt befüllt?
- Wo `% TODO`-Kommentare stehen: sind das wirklich nur Platzhalter für noch ausstehende Daten (z.B. Interview-Termine), oder wurde inhaltliche Arbeit verschoben?
- Bei Kapiteln mit Tabellen oder Vorlagen: ist klar markiert, was vor und was nach der Erhebung eingetragen wird?

### 4. Wissenschaftliche Substanz

- Werden Behauptungen mit Quellenbelegen, Begründungen oder Beispielen gestützt?
- Sind Schlussfolgerungen aus dem Material ableitbar oder erscheinen sie aufgesetzt?
- Unterscheidet das Kapitel zwischen eigenen Annahmen und etablierten Befunden?
- Gibt es methodische Schwächen, die die spätere Auswertung gefährden (z.B. unklare Sampling-Begründung, fehlender Pretest, schwache Reliabilitätsstrategie)?
- Werden Limitationen und Risiken offen ausgesprochen, statt versteckt?

### 5. Praxisnähe und Lesbarkeit für den Erstprüfer

- Ist das Kapitel ohne weitere Erklärung verständlich?
- Sind methodische Entscheidungen nachvollziehbar begründet?
- Gibt es methodische Risiken, die offen ausgesprochen werden sollten?
- Wird die Doppelrolle der Forscherin (sofern relevant, z.B. bei dualen Studierenden mit Praxispartner) reflektiert?
- Stimmt die Tonalität (wissenschaftlich-nüchtern, nicht plaudernd, nicht beratend)?

## Vorgehen

### Schritt 1: Eigenständiger Read-Through

Lies das Kapitel komplett durch. Markiere mental:

- Stellen, wo der Faden reißt
- Begriffe, die nicht eingeführt sind
- Aussagen ohne Beleg
- Übergänge, die fehlen

### Schritt 2: Konsistenzabgleich

Lies zusätzlich:

- `thesen/<name>/CLAUDE.md` — für Stammdaten und Konventionen
- `thesen/<name>/PROJEKTUEBERSICHT.md` — für Forschungsfrage, Subfragen, Methodik
- Andere bereits geschriebene Kapitel — für terminologische und argumentative Konsistenz

Vergleiche die im Review-Objekt vorgefundenen Aussagen mit den dort dokumentierten Setzungen.

### Schritt 3: Vollständigkeitsprüfung

```bash
# TODO-Kommentare im Kapitel
grep -nE "% *TODO" <datei>

# Cross-References
grep -nE "\\\\ref\{[^}]+\}" <datei>

# Nicht-aufgelöste Cross-References (nach erstem Compile sichtbar)
grep "Reference.*undefined" thesen/<name>/tex/main.log
```

### Schritt 4: Findings-Report

```markdown
# Review-C: Structure & Logic - <Kapitelname>

## Zusammenfassung
Gesamteindruck (3-4 Sätze). Was ist stark, was ist die zentrale Schwachstelle?

## Argumentations-Logik im Kapitel
- Stark: ...
- Schwach: ...

## Konsistenz mit anderen Kapiteln
- ...

## Substanz und Methodisch-Wissenschaftliches
- ...

## Empfehlungen für den nächsten Termin
(3-5 konkrete Schärfungen, mit Begründung)

## Was nach Erhebung / nach späteren Kapiteln ergänzt werden muss
(saubere Liste der echten TODO-Punkte)
```

## Severity-Definitionen

- **Critical**: Forschungsfrage zwischen Einleitung und PROJEKTUEBERSICHT divergiert; tragende Methodik-Aussage widerspricht zwischen zwei Kapiteln; Inhaltlich falsche Aussagen (z.B. „Interviews wurden durchgeführt", obwohl noch nicht).
- **Important**: Logiksprünge ohne Erklärung, fehlende Cross-References, schwache Begründung methodischer Entscheidungen, Plauderton im wissenschaftlichen Kontext.
- **Minor**: Stilistische Sprünge zwischen Absätzen, kleinere Inkonsistenzen in Begriffsverwendung, fehlende Brückensätze.

## Was diese Skill NICHT prüft

- Korrektheit einzelner Citations und Seitenzahlen (das macht `bachelorarbeit-review-citations`).
- Typographische Details (das macht `bachelorarbeit-review-style`).

## Disziplin

- Read-only.
- Konstruktiv-kritisch. Konkrete Vorschläge sind willkommen, aber jeder Vorschlag muss aus dem Quelltext begründet sein.
- Konkrete file:line-Referenzen, wo möglich.
- Bei Konflikten zwischen Kapiteln: beide Stellen zitieren.

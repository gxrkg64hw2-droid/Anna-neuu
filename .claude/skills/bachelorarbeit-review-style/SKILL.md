---
name: bachelorarbeit-review-style
description: |
  DE: Review-Skill B für Bachelorarbeits-Kapitel. Prüft deutsche wissenschaftliche Typographie und Stilistik in einem oder mehreren .tex-Dateien: Umlaute, Em-/En-Dashes, deutsche Anführungszeichen, Komma als Dezimaltrennzeichen, Gendering-Konsistenz, Satzlänge, Aktivsatz-Tendenz, Plauderton-Reste, LaTeX-Konventionen. Wird von der Bridge-Skill `bachelorarbeit-arbeitsweise` nach jedem fertigen Kapitel zwingend ausgelöst.
  EN: Review skill B for Bachelor-thesis chapters. Checks German scientific typography and style in one or more .tex files: umlauts, em/en-dashes, German quotation marks, comma decimal separator, gendering consistency, sentence length, active-voice tendency, casual-tone residue, LaTeX conventions. Triggered mandatorily by the bridge skill after each completed chapter.
allowed-tools: Read Bash Grep
license: MIT
metadata:
  skill-author: Bachelorarbeits-System (Fabian + Claude)
---

# Review-B: German Style & Typography

## Wann diese Skill aktiv wird

Wird von der Bridge-Skill `bachelorarbeit-arbeitsweise` als Pflicht-Pass nach jedem fertigen Kapitel aktiviert. Kann auch ad hoc auf einzelne `.tex`-Dateien angewendet werden.

## Zielsetzung

Sicherstellen, dass das geprüfte Kapitel den Konventionen der wissenschaftlichen deutschen Schreibsprache entspricht und die im Repo dokumentierten Typographie-Regeln einhält.

## Prüfdimensionen

### 1. Typographie (zwingend einzuhalten)

| Prüfpunkt | Regel | Werkzeug |
|---|---|---|
| Umlaute im Fließtext | IMMER ö ä ü ß. Verboten als Ersatz: oe ae ue ss. | `grep -nE "[a-zA-Z]{2,}(ae\|oe\|ue)[a-z]" <datei>` |
| Em-Dash (—), En-Dash (–) | ABSOLUT VERBOTEN. Nur Punkt, Komma, Doppelpunkt, Bindestrich (-). | `grep -nE "—\|–" <datei>` |
| Anführungszeichen | Im Fließtext via `\enquote{...}` oder direkt „..." | `grep -nE "\"[a-zA-ZäöüÄÖÜß]" <datei>` (flagt straight quotes mit deutschem Folgezeichen) |
| Dezimaltrennzeichen | Komma im Fließtext, Punkt nur in Formel-/p-Wert-Kontexten | manuelle Stichprobe |

**Ausnahmen, die NICHT geflaggt werden:**

- Bibkeys (z.B. `muehlhoff2019`) dürfen ASCII bleiben. Konvention.
- Filenames in `\input{...}` und `file = {...}` dürfen ASCII bleiben. Cross-Plattform-Konvention.
- BibTeX-Felder in `bibliography.bib` sind kein Fließtext. Stichprobenartig prüfen, aber nicht jede Schreibung mit ASCII-Substitut markieren.
- PDF-Filenames im `file =` Feld der `.bib`. Niemals ändern.

### 2. Gendering-Konsistenz

Die übliche Konvention dieser Codebase ist Doppelpunkt-Gendering (Expert:innen, Mitarbeiter:innen, Forscher:innen). Die konkret aktive Konvention steht in der jeweiligen `thesen/<name>/CLAUDE.md`.

Prüfpunkte:

- Gibt es generisches Maskulinum (z.B. „die Mitarbeiter", „die Coder", „die Forscher") an Stellen, wo gemischt-geschlechtliche Personen gemeint sind?
- Werden alle Gender-Markierungen konsistent als Doppelpunkt (oder als die in der CLAUDE.md festgelegte Variante) gesetzt?
- Gibt es Stellen, wo eine geschlechtsneutrale Umformulierung (z.B. „Beschäftigte" statt „Mitarbeiter:innen") eleganter wäre?

### 3. Wissenschaftlicher Stil

| Prüfpunkt | Faustregel |
|---|---|
| Satzlänge | Max 25 Worte pro Satz. Flagge Sätze ab 30 Worten. |
| Aktiv vs. Passiv | Aktivsatz bevorzugt, Passive nur wo idiomatisch. Flagge überlange Passivketten. |
| Plauderton-Reste | „ganz genau", „echt", „natürlich" als Phatica, rhetorische Fragen außerhalb von Sektionseinleitungen, idiomatische Wendungen wie „Öl ins Feuer gießen" |
| Nominalisierungen | Sparsam. Flagge ganze Sätze in Nominalstil ohne Verb-Substanz. |
| Anglizismen | OK wenn etabliert (Marketing, Performance, Stakeholder, Hate Speech). Flagge nicht-etablierte. |
| Floskeln | „Es lässt sich festhalten", „an dieser Stelle sei erwähnt" — flagge wenn überlastet. |

### 4. LaTeX-spezifisch

- **Cross-References:** Sind `\ref{...}` und `\label{...}` konsistent? Liegen unaufgelöste Refs vor?
- **`\parencite` vs. `\textcite`:** Stilistisch sinnvoll? `\textcite` für narrative Bezugnahme, `\parencite` für eingeklammerte Belege.
- **`\enquote{...}`:** Im Fließtext für jedes Zitat?
- **`\emph{}` vs. `\textbf{}`:** Adäquat eingesetzt? Nicht jeder Fachbegriff muss kursiv sein.
- **Kommentare:** TODO-Kommentare im finalen Manuskript dürfen nicht stehen bleiben. Flagge alle `% TODO` vor Abgabe.

## Vorgehen

### Schritt 1: Mechanische Checks via Grep

```bash
# Substitute im Fließtext
grep -nE "[a-zA-Z]{2,}(ae|oe|ue)[a-z]" <datei> | \
  grep -vE "Veranstalt|aktuell|kontextu|individ|Manuell|loosenDasL|MMK23|interview|abkuerzungs|kuerz|Eintrae|Themenbloeck|virtueller|Feuerwache"

# Em/En-Dashes
grep -nE "—|–" <datei>

# Sätze über 30 Worte (heuristisch)
awk 'BEGIN{RS="."} {n=split($0,a," "); if (n>30) print NR":"n" Wörter: "$0}' <datei>

# Generisches Maskulinum bei wahrscheinlichen Gender-Wörtern
grep -nE "\b(Mitarbeiter|Forscher|Coder|Nutzer|Kollege|Veranstalter|Künstler|Studierende)\b" <datei>
```

### Schritt 2: Inhaltliche Prüfung (manuell)

- Lies die Datei vollständig durch.
- Markiere Plauderton-Reste, ineffektive Floskeln, überlange Schachtelsätze.
- Identifiziere Stellen, wo eine geschlechtsneutrale Umformulierung den Lesefluss verbessern würde.

### Schritt 3: Findings-Report

```markdown
# Review-B: Style & Typography - <Datei oder Kapitelname>

## Zusammenfassung
N Findings: X CRITICAL, Y IMPORTANT, Z MINOR. Gesamtnote: gut/ok/verbesserungswürdig.

## Critical Findings (Show-Stopper, sofort fixen)
- file:line — was ist falsch — was sollte stehen

## Important Findings
- file:line — was — Vorschlag

## Minor Findings
- ...

## Stilistische Gesamtbewertung
(2-3 Sätze)
```

## Severity-Definitionen

- **Critical**: Em-/En-Dashes, falsche Umlaute (oe/ae/ue/ss als Ersatz im Fließtext), straight quotes statt deutscher, % TODO im Endmanuskript.
- **Important**: Sätze >30 Worte, generisches Maskulinum bei vermutlich gemischter Gruppe, Gendering-Inkonsistenz, Plauderton-Reste.
- **Minor**: Floskeln, Nominal-Tendenzen, kleine LaTeX-Inkonsistenzen.

## Was diese Skill NICHT prüft

- Citations und Quellen (das macht `bachelorarbeit-review-citations`).
- Argumentations-Logik (das macht `bachelorarbeit-review-structure`).

## Disziplin

- Read-only.
- Konkrete file:line-Referenzen.
- Keine Geschmacksurteile, sondern Regeln aus den repo-eigenen Konventionsdateien (`CLAUDE.md`, `thesen/<name>/CLAUDE.md`, `.claude/skills/scientific-writing/DEUTSCHE-KONVENTIONEN.md`).

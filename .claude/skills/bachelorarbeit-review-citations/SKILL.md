---
name: bachelorarbeit-review-citations
description: |
  DE: Review-Skill A für Bachelorarbeits-Kapitel. Prüft alle Citations in einem oder mehreren .tex-Dateien einer Thesis: Bibkey-Existenz, Seitenzahl-Plausibilität, Inhaltsabgleich der zitierten Seite mit dem umgebenden Absatz. Wird von der Bridge-Skill `bachelorarbeit-arbeitsweise` nach jedem fertigen Kapitel zwingend ausgelöst. Ergebnis ist ein Findings-Report mit Severity-Klassen Critical/Important/Minor.
  EN: Review skill A for Bachelor-thesis chapters. Checks every citation in one or more .tex files: bibkey existence, page-number plausibility, semantic match between cited page and surrounding paragraph. Triggered mandatorily by the bridge skill `bachelorarbeit-arbeitsweise` after each completed chapter. Output is a findings report with severity classes Critical/Important/Minor.
allowed-tools: Read Bash Grep
license: MIT
metadata:
  skill-author: Bachelorarbeits-System (Fabian + Claude)
---

# Review-A: Citations & Source-Verification

## Wann diese Skill aktiv wird

Wird von der Bridge-Skill `bachelorarbeit-arbeitsweise` als Pflicht-Pass nach jedem fertigen Kapitel aktiviert. Kann auch ad hoc auf einzelne `.tex`-Dateien angewendet werden, etwa vor einem Betreuer-Termin.

## Zielsetzung

Sicherstellen, dass jede `\parencite`/`\textcite`/`\footcite`-Anweisung in dem geprüften Kapitel folgende drei Eigenschaften hat:

1. Bibkey existiert in `bibliography.bib`.
2. Cited page liegt im Seitenbereich des PDF-Dokuments.
3. Inhalt der zitierten Seite stützt die im Absatz aufgestellte Behauptung tatsächlich (semantischer Abgleich).

Bei Verstößen werden konkrete Fundstellen mit Severity-Klassifikation gemeldet.

## Vorgehen

### Schritt 1: Automatischer Audit via CLI

```bash
python -m rag extract-citations \
  --tex <pfad/zur/datei.tex> \
  --thesis <name> \
  --check-bib --check-corpus --check-orphans --check-page-content \
  --pretty
```

Dieser Befehl prüft:

- `--check-bib`: Bibkey existiert in `bibliography.bib`. Bei Fehlen → `MISSING_BIBKEY` mit Suggest-Match.
- `--check-corpus`: Bibkey hat einen indizierten PDF-Eintrag in der Korpus-DB. Bei Fehlen → `BIBKEY_NOT_IN_CORPUS`.
- `--check-orphans`: Bib-Einträge, die in keiner `.tex`-Datei zitiert werden. Optional, beim Pre-Abgabe-Check sinnvoll.
- `--check-page-content`: Semantischer Abgleich zwischen Absatz im `.tex` und Inhalt der zitierten Seite. Bei zu geringer Ähnlichkeit (Default-Threshold 0,30) → `PAGE_CONTENT_MISMATCH`.

### Schritt 2: Manuelle Stichprobe bei den meistgenutzten Quellen

Zusätzlich zum automatischen Check: Die fünf am häufigsten zitierten Bibkeys identifizieren (mit `grep -o '\\parencite\[.*\]{[^}]*}' tex/kapitel/*.tex | sort | uniq -c | sort -rn | head -5`). Für jeden dieser Bibkeys eine Stichprobenprüfung mit `python -m rag search "<aussage>" --thesis <name> --filter-source <bibkey>` machen, um den Inhalt der zitierten Seite manuell zu sichten.

### Schritt 3: Heuristik-Checks

- **Same-page-clustering:** Wenn drei oder mehr aufeinanderfolgende Citations dieselbe Seite haben (z.B. `[S. 32]`, `[S. 32]`, `[S. 32]`), kann das ein Kopier-Aus-dem-Gedächtnis-Anti-Pattern sein. Stichprobenartig prüfen, ob die Aussagen tatsächlich auf derselben Seite belegt sind.
- **Page-number rounding:** Seiten wie `[S. 50]`, `[S. 100]`, `[S. 200]` sind statistisch über-vertreten, wenn aus dem Gedächtnis zitiert wurde. Stichprobenprüfung.
- **Cross-Quelle-für-eine-Aussage:** Wenn dieselbe Aussage mehrfach im Manuskript auftaucht und dabei verschiedene Quellen zitiert: Stichprobe.

### Schritt 4: Findings-Report

Output als Markdown mit dieser Struktur:

```markdown
# Review-A: Citations - <Datei oder Kapitelname>

## Zusammenfassung
N Citations geprüft, davon X CRITICAL, Y IMPORTANT, Z MINOR.

## Critical Findings (Show-Stopper)
- file:line — <Citation> — <was ist falsch> — <Suggest>

## Important Findings (vor Abgabe fixen)
- ...

## Minor Findings
- ...

## Beobachtungen zur Bibliographie
(z.B. fehlende Felder, suspekte Einträge, Orphans)

## Empfehlung
(2-3 Sätze: ist die Citation-Schicht abgabereif?)
```

## Severity-Definitionen

- **Critical**: `MISSING_BIBKEY` (Citation kompiliert nicht), `BIBKEY_NOT_IN_CORPUS` für Quellen, die für die Argumentation tragend sind. Show-Stopper.
- **Important**: `PAGE_CONTENT_MISMATCH` (Semantische Ähnlichkeit zu niedrig, Citation ist wahrscheinlich falsch verortet), Seitenzahl liegt außerhalb des PDF-Bereichs, eindeutige Fehlattribution.
- **Minor**: Stilistisch: `\textcite{}` vs. `\parencite{}` unpassend gewählt, Seitenzahl-Format inkonsistent (mal `S. 23 f.`, mal `S. 23-24`).

## Was diese Skill NICHT prüft

- Stilistische Aspekte der Prosa (das macht `bachelorarbeit-review-style`).
- Argumentations-Logik und Strukturkonsistenz (das macht `bachelorarbeit-review-structure`).
- Plagiat im engeren Sinne (das macht `python -m rag verify-quote` direkt am Absatz).

## Disziplin

- Die Skill modifiziert KEINE Dateien. Read-only Review.
- Die Skill erfindet KEINE Issues. Findings sind nur, was tatsächlich nachweisbar nicht stimmt.
- Bei Unsicherheit: `python -m rag search "<aussage>" --thesis <name>` ausführen und den Treffer mit der Citation abgleichen.
- Concrete file:line-Referenzen in jedem Finding, sonst ist der Report nicht handlungsrelevant.

## Verbindung zur Bridge-Skill

Wenn diese Review-Skill von `bachelorarbeit-arbeitsweise` aufgerufen wird, läuft sie parallel mit `bachelorarbeit-review-style` und `bachelorarbeit-review-structure`. Die Bridge-Skill aggregiert die drei Reports, fixt zusammen mit dem Nutzer alle Critical und Important Findings, sammelt Minor in einer TODO-Sektion und committet erst nach erfolgreichem Re-Compile.

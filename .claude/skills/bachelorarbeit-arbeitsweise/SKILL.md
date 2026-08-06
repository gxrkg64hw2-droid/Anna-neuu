---
name: bachelorarbeit-arbeitsweise
description: |
  DE: Verbindliche Arbeitsweise beim Schreiben oder Überarbeiten von Bachelorarbeits-Inhalten in dieser Codebase. Aktiviere diese Skill, wenn du eine .tex-Datei in thesen/<name>/tex/ editierst oder wenn der Nutzer dich bittet, einen Thesis-Abschnitt zu schreiben oder zu überarbeiten. Orchestriert das Bachelorarbeits-System: rag search vor JEDER Aussage, verify-quote nach jedem Absatz, extract-citations vor jedem Commit, Brave/Firecrawl nur für Material außerhalb des Korpus. Pflicht-Reviews nach jedem fertigen Kapitel.
  EN: Mandatory workflow when writing or revising Bachelor-thesis content in this codebase. Activate this skill when editing .tex files in thesen/<name>/tex/ or when asked to write or revise a thesis chapter section. Orchestrates the Bachelorarbeits-System: rag search before EVERY claim, verify-quote after every paragraph, extract-citations before every commit, Brave/Firecrawl only for material outside the corpus. Mandatory reviews after every completed chapter.
allowed-tools: Read Write Edit Bash Grep Glob Task
license: MIT
metadata:
  skill-author: Bachelorarbeits-System (Fabian + Claude)
---

# Bachelorarbeit-Arbeitsweise

## Ziel dieser Skill

Diese Skill ist KEIN Schreib-Skill. Sie ist die Stütze, die sicherstellt, dass beim Schreiben einer Bachelorarbeit jede Aussage Quellen-belegt ist, jeder Absatz auf Plagiat geprüft wurde und kein Zitat erfunden ist. Wenn diese Skill aktiv ist, gelten ihre Regeln strikt vor jeder anderen Skill.

## ⛔ HARTE GRUNDREGEL ⛔

**Es gibt eine Regel, die NIEMALS, unter KEINEN Umständen, übergangen werden darf, egal wie zeitkritisch die Aufgabe ist, egal wie offensichtlich eine Aussage scheint, egal ob du dieselbe Quelle vor zwei Sätzen schon zitiert hast:**

> **JEDE einzelne Aussage, die in den Fließtext der Arbeit geht und mit `\parencite`, `\textcite`, `\footcite` oder einer anderen Citation belegt wird, MUSS unmittelbar vor dem Schreiben durch einen frischen `python -m rag search`-Aufruf abgesichert werden. Die `citation_suggestion` aus dem Treffer wird VERBATIM eingesetzt. Citation-Strings dürfen NIEMALS aus dem Gedächtnis, aus früheren Absätzen oder aus „weiß-ich-doch"-Wissen rekonstruiert werden.**

**Begründung:** Bei Reviews am 2026-05-07 wurden in der Methodik-Schicht der Bachelorarbeit von Luana Lassandro vier falsche Seitenzahlen gefunden (loosen2014 S. 50 statt S. 13; loosen2014 S. 65 statt S. 46 zweimal; kaiser2021 S. 75 statt S. 74). Ursache: Citations wurden aus dem Gedächtnis konstruiert statt frisch gesucht. Solche Fehler sind im Endprodukt nicht akzeptabel, weil sie eine Bachelorarbeit unter Plagiats- und wissenschaftlichen-Redlichkeits-Aspekten angreifbar machen.

## Eskalation bei Versuchung, die Regel zu übergehen

Wenn du als Claude während des Schreibens den Impuls verspürst:

- „Diese Quelle hatte ich vorhin schon zitiert, ich nehme einfach die alte Citation"
- „Ich kann mir aus dem Gedächtnis die Seite ungefähr merken"
- „Eine Suche dauert zu lange, lass mich erstmal den Absatz schreiben"
- „Diese Aussage ist so allgemein, da brauche ich keine spezifische Seitenzahl"
- „Der Nutzer wartet, ich kürze ab"

→ **STOP. ESKALATION.** Diese Gedanken sind das Frühwarnsystem für genau den Fehler, der diese Regel ausgelöst hat. Schreib in den Antwort-Text an den Nutzer eine Zeile:

```
[ESKALATION] Habe gerade den Impuls, eine Citation aus dem Gedächtnis zu setzen
für die Aussage „<Aussage>". Führe stattdessen frischen rag search aus.
```

Dann führe den Search aus. Punkt. Kein Verhandeln mit dir selbst.

## Bevor du mit Schreiben beginnst

1. Lies `thesen/<name>/CLAUDE.md`. Dort steht: Thesis-Topic, gewähltes Profil, Modus (Premium/Lean), Konventionen, Status, aktive TODOs, Spezialanweisungen des Verfassers.
2. Wenn du den Korpus in dieser Session noch nicht inventarisiert hast: `python -m rag corpus --thesis <name> --pretty`. Damit weißt du, was an Quellen verfügbar ist.
3. Identifiziere, welcher vendored K-Dense-Skill zum Kapiteltyp passt (Tabelle siehe unten).

## Sieben-Schritt-Ritual pro Absatz (NICHT VERHANDELBAR)

Jeder Absatz, der eine Aussage macht, durchläuft diese Schritte:

1. **Kernaussage identifizieren.** Welches Konzept oder welche Behauptung ist der Kern dieses Absatzes? Wenn der Absatz mehrere Aussagen enthält: pro Aussage ein eigener Search-Zyklus.

2. **Frische Korpus-Suche.** `python -m rag search "<konzept>" --thesis <name> --top 5 --pretty`. Frisch heißt: nicht aus dem Cache der Vorabsätze, nicht aus dem Gedächtnis. Auch wenn du dieselbe Quelle vor drei Absätzen schon zitiert hast: für die neue Aussage neu suchen, weil sich die zu belegende Aussage geändert hat und damit die richtige Seitenzahl.

3. **Bei Relevanz: `citation_suggestion` VERBATIM übernehmen.** Das Feld liefert die fertige `\parencite[S. X]{key}`-Form. Kopiere sie zeichengenau ins .tex. Konstruiere NIEMALS selbst, errate NIEMALS Bibkey oder Seitenzahl.

4. **Bei keinem Hit und der Behauptung ist eine Korpus-Tatsache:** STOP. Frage den Nutzer: „Soll ich diese Quelle dem Korpus hinzufügen, oder formulieren wir um?" Niemals erfinden.

5. **Bei keinem Hit und es ist eine externe/aktuelle Tatsache** (Marktdaten 2025/2026, Tool-Website, jüngste Meldung): nutze Brave MCP für die Suche, Firecrawl MCP für tiefe Inhalte. URL und Stand-Datum festhalten. Eintrag in `bibliography.bib` als `@online`. Citation: `\parencite[Online: <URL>, Stand: <YYYY-MM-DD>]{webX}`.

6. **Absatz schreiben.** Deutsche Typographie strikt einhalten:
   - Korrekte Umlaute (ö ä ü ß), niemals oe ae ue ss als Ersatz
   - KEINE Em-Dashes (—), KEINE En-Dashes (–). Nur Punkt, Komma, Doppelpunkt, Bindestrich (-)
   - Deutsche Anführungszeichen via `\enquote{...}` aus `csquotes`
   - Komma als Dezimaltrennzeichen
   - Gendering-Konvention aus `thesen/<name>/CLAUDE.md`
   - Max 25 Worte pro Satz als Faustregel

7. **Verify-Quote.** `python -m rag verify-quote --text "<gerade geschriebener Schlüsselsatz>" --thesis <name>`. Regel:
   - `STRICT_MATCH`: zu nah am Original. Umschreiben oder als wörtliches Zitat in Anführungszeichen setzen.
   - `FUZZY_MATCH`: zu nah als Paraphrase. Umschreiben oder Citation hinzufügen.
   - `THEMATIC_MATCH`: gleiche Idee. Citation für das Konzept hinzufügen.
   - `NO_MATCH`: ok, weiter.

## Pflicht-Reviews nach jedem fertigen Kapitel

Wenn ein Kapitel fertig geschrieben ist (auch wenn nur als Erstentwurf), MÜSSEN drei Review-Pässe parallel ausgeführt werden, BEVOR der nächste Schreibschritt beginnt oder ein Commit gepusht wird:

1. **Review-A: Citations & Sources** (Skill `bachelorarbeit-review-citations`). Verifiziert für jede Citation, dass Bibkey existiert, Seitenzahl im PDF-Bereich liegt und Inhalt der zitierten Seite die Behauptung tatsächlich stützt. Nutzt automatisch `python -m rag extract-citations --check-page-content`.

2. **Review-B: German Style & Typography** (Skill `bachelorarbeit-review-style`). Prüft Umlaute, Em-/En-Dashes, deutsche Anführungszeichen, Gendering-Konsistenz, Satzlänge, wissenschaftlichen Ton.

3. **Review-C: Structure & Scientific Logic** (Skill `bachelorarbeit-review-structure`). Prüft Argumentationsfaden, Konsistenz zwischen Kapiteln, Methodische Substanz, Lesbarkeit für den Erstprüfer.

**Pflicht-Workflow nach Kapitel-Fertigstellung:**

```
[Eingabe: ein fertig geschriebenes Kapitel, z.B. tex/kapitel/02-theorie.tex]

1. Dispatche die drei Review-Skills parallel als Task-Agents (eine Task-Tool-Aufruf pro Skill).
2. Sammle die drei Reports (typischerweise nach 1 bis 3 Minuten).
3. Wende ALLE Critical und Important Findings an, bevor du das Kapitel als „fertig" markierst.
4. Minor Findings sammeln in einer TODO-Sektion oder direkt fixen, je nach Zeitbudget.
5. Re-compile, re-verify, dann erst commit.
```

Es gibt keinen „Schnell-Modus", der diese Reviews überspringt. Auch nicht wenn der Erstprüfer übermorgen das Kapitel sehen will. Eskalation lieber an den Nutzer (`„Ich brauche 5 Minuten für die Reviews, das Kapitel ist sonst nicht abgabereif"`) als ein Kapitel ohne Reviews abzugeben.

## Skill-Auswahl pro Kapiteltyp

| Kapitel | Vorrangig zu nutzende Skill |
|---|---|
| Einleitung, Fazit | `scientific-writing` |
| Theoretischer Rahmen, Begriffsapparat | `scientific-writing` + `literature-review` |
| Hypothesenentwicklung | `hypothesis-generation` |
| Methodik (quantitativ) | `statistical-analysis` |
| Methodik (qualitativ, Mayring) | siehe `dach_reporting_standards.md` in `statistical-analysis` oder `peer-review` |
| Ergebnisse | `statistical-analysis` + `scientific-visualization` |
| Diskussion, Limitationen | `scientific-critical-thinking` |
| Marktanalyse-Kapitel | `market-research-reports` |
| Selbst-Audit vor Abgabe | `scholar-evaluation`, `peer-review` |
| Früh-Phase Forschungsfrage | `scientific-brainstorming` |

## Wann externe MCPs (Brave, Firecrawl)

- **Brave MCP**: aktuelle Statistiken, Marktdaten, News, Tool-Websites. Eingang für alles, was nicht in Buchform im Korpus ist.
- **Firecrawl MCP**: tiefe Web-Inhalte (Whitepaper, ausführliche Hersteller-Dokus, Blogposts). Wenn Brave nur Snippets liefert.
- WICHTIG: Externe Funde gehen IMMER mit URL und Stand-Datum in die `bibliography.bib` als `@online`. Niemals „ich weiß das aus Training", immer mit Quelle.

## Verbotene Handlungen

1. **Citations aus dem Gedächtnis konstruieren.** Niemals `\parencite{key}` ohne dass `key` und Seitenzahl direkt aus einem frischen `rag search`-Treffer dieser Aussage stammen. Das Wiederverwenden von Citations aus Vorabsätzen, weil „die Quelle ist ja dieselbe", ist ebenfalls verboten, weil die Seitenzahl mit der Aussage variiert.
2. **Em-Dash oder En-Dash schreiben.** Punkt, Komma, Doppelpunkt oder Bindestrich (-) sind die einzigen Trennzeichen.
3. **Umlaute durch oe/ae/ue/ss ersetzen.** Korrekte Schreibweise immer (ö ä ü ß).
4. **Einen Absatz committen ohne `verify-quote`.**
5. **Ein Kapitel committen ohne die drei Pflicht-Reviews.**
6. **Quellen erfinden, wenn der Korpus leer ist.** Stop, frage den Nutzer.
7. **In `thesen/<name>/index/` editieren.** Das ist generierter Output. Bei Bedarf `python -m rag index --thesis <name> --rebuild`.

## Vor jedem Commit ins thesen-Verzeichnis

```bash
python -m rag extract-citations \
  --tex thesen/<name>/tex/main.tex \
  --thesis <name> \
  --check-bib --check-corpus --check-orphans --check-page-content --strict
```

Wenn der Befehl mit Exit-Code 1 zurückkommt: Issues beheben, dann erst commit. Niemals `--strict` weglassen, niemals `--check-page-content` weglassen.

## Eskalationsregeln

- **Nicht im Korpus + nicht via Brave/Firecrawl auffindbar:** Stop. Frage Nutzer: „Soll ich diese Quelle dem Korpus hinzufügen, oder formulieren wir um?"
- **`verify-quote` schlägt unklar an** (Score knapp unter Threshold): zeige dem Nutzer den `diff_preview` und frage nach Entscheidung.
- **`extract-citations --check-page-content` zeigt PAGE_CONTENT_MISMATCH:** Citation ist falsch verortet. Frischer `rag search` für die Aussage, korrekte `citation_suggestion` einsetzen.
- **Zwei Skills haben in derselben Aufgabe widersprüchliche Empfehlungen:** Diese Bridge-Skill hat Vorrang. Folge den hier dokumentierten Regeln, nicht den allgemeinen Skill-Empfehlungen.
- **Du verspürst den Impuls, das 7-Schritt-Ritual abzukürzen:** STOP, melde Eskalation per Antwort-Text an den Nutzer, dann ritualgetreu fortsetzen.

## Sprachhinweis

Wenn die Bachelorarbeit englisch geschrieben wird (selten in DACH, aber möglich), gelten die Schritte 1-7 unverändert. Statt deutscher Typographie englische Konventionen ("..." statt deutsche Anführungszeichen), Punkt als Dezimaltrennzeichen, APA in englischer Standardform.

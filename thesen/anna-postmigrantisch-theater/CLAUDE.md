# CLAUDE.md (Thesis Brief) — anna-postmigrantisch-theater

**Profil:** `theoretisch-konzeptionell` · **Modus:** Lean · **Sprache:** Deutsch

> Dies ist eine **Seminararbeit** (Theoriearbeit), kein voller BA-Umfang. Die Bridge-Skill
> `bachelorarbeit-arbeitsweise` gilt trotzdem vollständig, sobald `.tex`- oder Thesis-Inhalt
> geschrieben wird. Root-`CLAUDE.md` bleibt übergeordnet.

## Thema und Fragestellung

- **Arbeitstitel:** „Kunst und Gesellschaftskritik – Theater und Satire als Räume postmigrantischer Sichtbarkeit und Zugehörigkeit"
- **Forschungsfrage:** Welche Rolle spielen postmigrantisches Theater und Satire als Formen der Gesellschaftskritik bei der Hinterfragung dominanter Vorstellungen von Migration und Zugehörigkeit?
- **Zentrale These (laut Betreuer-Feedback Rotter):** Postmigrantisches Theater und Satire sind Ausdruck postmigrantischer Perspektiven, weil sie die theoretische Kritik am methodologischen Migrantismus praktisch umsetzen und dadurch dominante Vorstellungen von Migration und Zugehörigkeit infrage stellen.

## Formale Vorgaben (aus der Aufgabenstellung, Fotos)

- **Umfang:** 8–10 Seiten Fließtext, **mindestens 2.840 Wörter**, Abgabe als **PDF**.
- **Deadline:** **09. August 2026** (Begutachtungsfrist 1 Monat).
- **Schrift:** Times New Roman 12 / Zeilenabstand 1,5 (alternativ Calibri, Aptos oder Arial 11 / 1,5).
- **Ränder:** links 2,5 cm, rechts 3,5 cm. **Blocksatz** mit automatischer Silbentrennung.
- **Gendergerechte Sprache** (konsistent, z. B. Doppelpunkt: „Migrant:innen").
- **Zitation:** direkte Zitate und Paraphrasen so genau wie möglich, **immer mit Seitenzahl**.
- **Formaler Aufbau:** Titelblatt (Name, Studienkennzahl, Matrikelnummer, Seminartitel, Leiter, Semester, Thema, Abgabedatum) · Inhaltsverzeichnis · Einleitung (nicht nummeriert) · Hauptteil (Kapitel/Unterkapitel) · Resümee/Ausblick · Literaturverzeichnis (alphabetisch).

## Betreuer-Methodik (Rotter) — WICHTIG für den Aufbau

Es ist **keine** klassische Analyse (Theorie → Analyse → Fazit), sondern eine Theoriearbeit mit
Richtung **Theorie → theoretisch begründete Ableitung → Beispiel als Praxisform → Fazit**.
Die Beispiele (Theater, Satire) dienen dazu, die vorher aus der Theorie abgeleitete These zu
**stützen/veranschaulichen/plausibel machen** (nicht „beweisen"). Ableitungen immer als aus der
Literatur entwickelte Schlussfolgerungen formulieren, nicht als eigene normative Aussagen darüber,
„wie Kunst sein müsste".

## Kapitelstruktur mit Wortbudget

| Teil | Inhalt | Wörter |
|---|---|---|
| Einleitung | Hinführung, Forschungsfrage, Begründung, Vorgehen, Übersicht | 250–350 |
| Kap. 1 Theoretische Grundlagen | 1.1 Methodologischer Migrantismus · 1.2 Postmigrantische Perspektive · 1.3 Zwischenfazit | 900–1.100 |
| Kap. 2 Von der Theorie zur Praxis | Ableitung + 4 Kategorien (Wir/Andere hinterfragen; Migration als Normalität; neue Zugehörigkeit; Gesellschaftskritik) | 400–600 |
| Kap. 3 Theater als Praxisform | Ballhaus Naunynstraße (ggf. Maxim Gorki), Langhoff-Interview | 600–800 |
| Kap. 4 Satire als Praxisform | Die Datteltäter (Video-Zitate mit Link/Jahr/Titel/**Minute**) | 600–800 |
| Fazit | Beantwortung der Forschungsfrage, zentrale These, Ausblick | 250–350 |

## Bearbeitungsstand (Stand: Übergabe)

- **Kap. 1:** FERTIG und offline verifiziert (Bibkeys/Jahre/Seiten geprüft, Plagiatscheck ok) in `arbeit.md`. Korrektur ggü. Entwurf: Kanak Attak = Yıldız 2025, S. 126 (nicht Visionen S. 56).
- **KRITISCH:** Im Entwurf stehen überall Platzhalter „(Jahr)" und noch **nicht verifizierte
  Seitenzahlen**. Vor jeder Übernahme in den Fließtext: frischer `rag search`, `citation_suggestion`
  verbatim, echte Bibkeys + geprüfte Seiten. Kein Zitat aus dem Gedächtnis.
- **Kap. 2 (Von der Theorie zur Praxis):** FERTIG, verifiziert. „Community"-Lücke geschlossen: alle Beispiele (Unmündigen, Fest des deutschen Mitbürgers, gesternJahre, Rückkehrer-Stammtisch) aus Yıldız 2025 belegt.
- **Kap. 3 (Theater als Praxisform):** FERTIG, verifiziert. Ballhaus Naunynstraße via Carvalho/Larsson 2022, Sharifi/Skwirblies 2022, Balme 2022, Langhoff 2011.
- **Kap. 4 (Satire):** FERTIG, verifiziert. Datteltäter vollständig aus Yıldız 2025 (S. 133–135 Kollektiv, S. 237 Theorie) belegt. KEIN Video nötig.
- **Einleitung + Fazit:** FERTIG.
- **ROHFASSUNG KOMPLETT:** 2.858 Wörter, alle Belege offline geprüft, Plagiatscheck bestanden.
  Ausgabe: `Seminararbeit-postmigrantisch.pdf` (via `tools/anna-build-pdf.py`, PyMuPDF; LibreOffice im Container defekt)
  und `Seminararbeit-postmigrantisch.docx` (via `tools/anna-build-docx.py`, editierbar in Word).
  OFFEN nur: Titelblatt-Daten (Name, Studienkennzahl, Matrikelnummer, Seminartitel, Leitung, Semester)
  in `arbeit.md`/Generator eintragen. Optional: konkretes Datteltäter-Video mit Minutenangabe.

## Korpus (Lean-Modus, 7 PDFs in `pdfs/`, NICHT im Git)

Die Buch-Scans sind urheberrechtlich geschützt und per `.gitignore` vom Push ausgeschlossen
(`thesen/*/pdfs/*.pdf`). Sie liegen nur lokal für `rag index`. Bei Neustart neu bereitstellen
(siehe `SETUP-NETZWERK.md`).

| Datei | Werk | Gedruckte Seiten (aus Dateiname) |
|---|---|---|
| `postmigrantisch-denken-teil1.pdf` | Yıldız (Hg.), Postmigrantisch denken | S. 1–142 |
| `postmigrantisch-denken-teil2.pdf` | dass. | S. 143–283 |
| `postmigrantische-visionen-teil1.pdf` | Hill & Yıldız (2018), Postmigrantische Visionen | S. 1–129 |
| `postmigrantische-visionen-teil2.pdf` | dass. | S. 130–257 |
| `theaterwissenschaft-postkolonial-teil1.pdf` | Sharifi & Skwirblies (2022), Theaterwissenschaft postkolonial/dekolonial | S. 1–150 |
| `theaterwissenschaft-postkolonial-teil2.pdf` | dass. | S. 151–299 |
| `interview-langhoff-2011-bpb.pdf` | Langhoff (2011), Interview „Die Herkunft spielt keine Rolle", bpb.de | Web (@online) |

Der Print-Offset pro Teil ist beim Indexieren zu prüfen (`corpus --pretty`); bei Bedarf
`overrides.toml` setzen. Teil-2-Dateien haben einen Offset (z. B. Teil2 PDF-Seite 1 = gedruckte S. 143).

## Fehlende Quellen (BLOCKER für Kap. 2 und 4)

1. **Yıldız & Rotter, „Community"** (S. 405–413): Beispiele „Die Unmündigen" („Ihr seid gefährlich!"),
   Ausstellung „gesternJahre – 50 Jahre gastArbeiter", „Rückkehrer-Stammtisch" (Transtopie),
   „Kunst gegen Rassismus" / „Fest des deutschen Mitbürgers". In keinem hochgeladenen PDF enthalten.
   → Von der Verfasserin als PDF nachfordern.
2. **Datteltäter** (Kap. 4): konkretes Video/Sketch wählen; Zitierweise Link + Jahr + Titel + Minute.
   → Auswahl mit der Verfasserin klären (oder recherchieren, sobald Netz erlaubt Brave/Firecrawl).

Weitere in der Gliederung genannte, noch nicht im Korpus: Alkin & Geuer (2022) Postkolonialismus und
Postmigration; Donlic (2025). Nur nutzen, wenn als PDF bereitgestellt.

## Modus

- [x] **Lean**: nur PDFs. `uv run python -m rag bib --thesis anna-postmigrantisch-theater --build`
  baut die `bibliography.bib` (DOI/OpenAlex/Crossref/Titelsuche) und verlinkt Bibkeys.
- [ ] Premium (kein Zotero-Export vorhanden).

## Ausgabeformat (Entscheidung offen halten)

Im Cloud-Container ist **kein LaTeX** installiert → `.tex` kann hier nicht kompiliert werden.
`libreoffice/soffice` ist vorhanden. Zwei Optionen:
1. **`.docx` → PDF** (via LibreOffice), exakt nach obiger Formvorgabe (TNR 12, Ränder 2,5/3,5, Blocksatz).
   Rendert im Container. Empfohlen, weil es die Word-Vorgaben des Betreuers 1:1 trifft.
2. Strikt LaTeX-Workflow (`tex/`), Verfasserin kompiliert extern.
Die RAG-Zitatprüfung (`rag search` + `verify-quote`) ist formatunabhängig und wird in beiden Fällen
voll genutzt.

## Konventionen

- **Deutsche Typographie:** echte Umlaute (ö ä ü ß), KEINE Em-/En-Dashes, `\enquote{...}` bzw.
  deutsche Anführungszeichen „…", Komma als Dezimaltrennzeichen, max. ~25 Wörter/Satz.
- **Gendering:** Doppelpunkt-Form („Migrant:innen"), konsistent durchhalten.
- **Bibkeys:** sprechend, z. B. `yildizPostmigrantischDenken`, `hillYildizVisionen2018`,
  `sharifiSkwirblies2022`, `langhoff2011`, `yildizRotterCommunity`.

## Netzwerk-Voraussetzung

Das RAG-System braucht `openrouter.ai` (Embeddings) und `openaipublic.blob.core.windows.net`
(tiktoken). Beide müssen in der Netzwerk-Policy der Cloud-Umgebung erlaubt sein
(Custom-Allowlist oder Full). Details und Neustart-Ablauf: `SETUP-NETZWERK.md`.

## Nützliche Befehle

```bash
uv run python -m rag corpus  --thesis anna-postmigrantisch-theater --pretty
uv run python -m rag index   --thesis anna-postmigrantisch-theater
uv run python -m rag bib      --thesis anna-postmigrantisch-theater --build --pretty
uv run python -m rag search   "methodologischer Migrantismus" --thesis anna-postmigrantisch-theater --top 5 --pretty
uv run python -m rag verify-quote --text "..." --thesis anna-postmigrantisch-theater
```

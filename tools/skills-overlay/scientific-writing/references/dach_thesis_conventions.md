# DACH-Konventionen fuer Bachelorarbeiten

Orientierungswerte fuer Bachelorarbeiten im deutschsprachigen Raum. Der
verbindliche Rahmen ergibt sich aus dem Pruefungsamt oder dem Style-Guide
der jeweiligen Hochschule.

---

## Aufbau einer typischen DACH-BA

Standardreihenfolge (optionale Teile in Klammern):

1. Titelblatt: Titel, Typ der Arbeit, Studiengang, Hochschule, Betreuer,
   Autor, Matrikelnummer, Abgabedatum.
2. (Sperrvermerk) bei Unternehmenskooperation mit Geheimhaltung.
3. (Abstract / Zusammenfassung) je nach Hochschulvorgabe hier oder nach Verzeichnissen.
4. Inhaltsverzeichnis.
5. Abkuerzungsverzeichnis (empfohlen ab ca. 5 Abkuerzungen).
6. Abbildungsverzeichnis (ab einer Abbildung).
7. Tabellenverzeichnis (ab einer Tabelle).
8. (Symbolverzeichnis) nur in stark formalisierten Arbeiten mit Notation.
9. Einleitung: Problemstellung, Zielsetzung, Forschungsfrage, Aufbau.
10. Theoretischer Rahmen / Literaturueberblick.
11. Methodik: Forschungsdesign, Datenerhebung, Auswertung, Guetekriterien.
12. Ergebnisse: neutrale Darstellung der Befunde.
13. Diskussion: Interpretation, Vergleich mit Literatur, Limitationen.
14. Fazit: Beantwortung der Forschungsfrage, Ausblick.
15. Literaturverzeichnis.
16. (Anhang): Frageborgen, Transkripte, Rohdaten, ergaenzende Tabellen.
17. Eidesstattliche Erklaerung (in Deutschland meist am Ende, Pflicht).

---

## Forschungsfrage formulieren

Eine Forschungsfrage ist praezise, beantwortbar und thematisch eingegrenzt.

**Typen:**
- Deskriptiv (beschreibend): "Wie verbreitet ist X in Y?"
- Explanatorisch (erklaerend): "Welchen Einfluss hat X auf Y unter Bedingung Z?"
- Gestaltungsorientiert (konstruktiv): "Wie kann X entwickelt werden, um Y zu erreichen?"

**Beispiele:**

Informatik, technischer RAG-Chatbot (gestaltungsorientiert):
"Wie kann ein Retrieval-Augmented-Generation-System fuer die Wissensbasis einer
Hochschulbibliothek konzipiert werden, um die Praezision von Quellenangaben
gegenueber einem rein parametrischen Sprachmodell messbar zu erhoehen?"

BWL/Marketing, Konsumentenadoption (explanatorisch):
"Welche Faktoren beeinflussen die Adoptionsbereitschaft junger Erwachsener
(18-30 Jahre) gegenueber KI-gestuetzten Empfehlungssystemen in deutschen
E-Commerce-Plattformen?"

VWL, Marktanalyse (deskriptiv/explanatorisch):
"In welchem Ausmass hat die Einfuehrung des deutschen Mindestlohns 2015 die
Beschaeftigungsniveaus in der Gastronomiebranche beeinflusst?"

**Hinweise:** Forschungsfragen beginnen mit "Wie", "Welche", "Inwiefern",
"In welchem Ausmass". "Warum" ist schwer operationalisierbar. Eine BA hat
in der Regel eine Hauptfrage und ein bis zwei Teilfragen.

---

## Eidesstattliche Erklaerung (Standardwortlaut DGB)

Der folgende Wortlaut ist weit verbreitet und von vielen deutschen Hochschulen
akzeptiert. Spezifischer Hochschulwortlaut hat Vorrang.

---

Ich erklaere hiermit an Eides statt, dass ich die vorliegende Arbeit
selbststaendig und ohne Benutzung anderer als der angegebenen Hilfsmittel
angefertigt habe. Die aus fremden Quellen direkt oder indirekt uebernommenen
Gedanken sind als solche kenntlich gemacht. Die Arbeit wurde bisher in gleicher
oder aehnlicher Form keiner anderen Pruefungsbehoerde vorgelegt und auch noch
nicht veroeffentlicht.

Ort, Datum: ___________________________

Unterschrift: ___________________________

---

Seit 2023/2024 verlangen viele Hochschulen zusaetzlich eine Erklaerung zum
Umgang mit KI-Werkzeugen (ChatGPT, GitHub Copilot etc.). Die aktuelle Vorlage
des Pruefungsamts pruefen.

---

## Sperrvermerk (optional, wenn Unternehmen beteiligt)

Wird eingefuegt, wenn die Arbeit in Kooperation mit einem Unternehmen entstand
und vertrauliche Informationen enthaelt.

**Standardwortlaut:**

Die vorliegende Bachelorarbeit enthaelt vertrauliche Daten und Informationen
des Unternehmens [Unternehmensname], [Ort]. Die Arbeit ist daher fuer einen
Zeitraum von [2/3/5] Jahren ab dem Abgabedatum gegenueber Dritten gesperrt.
Veroeffentlichung, Vervielfaeltigung oder Einsichtnahme durch Unbefugte ist
ohne ausdrueckliche schriftliche Genehmigung des Unternehmens untersagt.

Ort, Datum: ___________________________   Unterschrift: ___________________________

**Hinweise:** Typische Sperrdauer 2 bis 5 Jahre. Gutachter und Pruefer haben
stets Leserecht. Sperrvermerk steht direkt nach dem Titelblatt.

---

## Gendering-Konventionen 2026

Vier gaengige Ansaetze im Ueberblick:

1. **Geschlechtsneutrale Formulierungen** (fuer wissenschaftliche Texte
   empfohlen): Substantivierungen und Kollektivbegriffe.
   Beispiel: "die Studierenden", "die Lehrenden", "die Beschaeftigten".

2. **Gender-Sternchen:** Sternchen zwischen Wortstamm und weiblicher Endung.
   Beispiel: "die Mitarbeiter*innen", "die Nutzer*innen".

3. **Binnen-I:** Grossgeschriebenes I im Wortinneren.
   Beispiel: "die MitarbeiterInnen", "die NutzerInnen".

4. **Generisches Maskulinum mit Hinweis:** Ausschliesslich maennliche Form,
   aber in der Einleitung explizit erklaert:
   "Aus Gruenden der Lesbarkeit wird das generische Maskulinum verwendet.
   Saemtliche Personenbezeichnungen gelten gleichermassen fuer alle Geschlechter."

**Empfehlung:** Hochschul-Style-Guide pruefen. Fehlt eine Vorgabe, ist Ansatz 1
die stilistisch sicherste Wahl.

**Systemintegration:** Der Standard in `_common/gendering.tex` ist
`\genderneutral`. Override via:

```latex
\renewcommand{\genderstil}{\genderstern}
```

---

## Schreibstil

- **Praezision vor Eleganz.** Jeder Satz soll genau einen Sachverhalt
  ausdruecken. Mehrdeutigkeiten sind kein Stilmittel.
- **Nuechternheit.** Wertungen ohne Beleg ("hervorragend", "leider") sind
  unzulaessig. Befunde zitieren, dann einordnen.
- **Passiv vs. Aktiv.** Passiv fuer Methoden und Ergebnisse; Aktiv fuer
  Argumentation ("Diese Arbeit argumentiert..."). Mix ist lesbar.
- **Anglizismen sparsam.** Fachbegriffe ohne deutsche Entsprechung sind
  akzeptabel ("Retrieval-Augmented Generation"). Umgangssprachliche
  Anglizismen ("macht Sinn", "gecancelt") vermeiden.
- **Nominalisierungen in Massen.** Typisch fuer deutschen Wissenschaftsstil,
  aber Haaufungen vermeiden. Faustregel: maximal zwei Substantivierungen
  pro Satz.
- **Satzlaenge max. 25 Worte** (Faustregel). Schachtelsaetze mit mehr als
  zwei Nebensaetzen vermeiden.
- **Komma als Dezimaltrennzeichen** im deutschen Text: 3,14 nicht 3.14.
- **Zeitform.** Methoden und Ergebnisse im Praeteritum oder Perfekt. Stand
  der Literatur und allgemeine Aussagen im Praesens.

---

## Verbotene Stilmittel

### Em-Dash und En-Dash

Em-Dash (U+2014) und En-Dash (U+2013) sind in allen Textausgaben dieses
Systems absolut verboten. Das gilt fuer Fliesstexte, Kommentare, generierte
Inhalte, UI-Texte und Markdown.

Falsch: "Das Ergebnis war eindeutig -- die Hypothese wurde bestaetigt."
Richtig: "Das Ergebnis war eindeutig: Die Hypothese wurde bestaetigt."

Falsch: "Der zweite Faktor -- die Usability -- wurde separat erhoben."
Richtig: "Der zweite Faktor, die Usability, wurde separat erhoben."

Erlaubte Satzzeichen fuer Pausen: Komma, Semikolon, Doppelpunkt, Klammern,
Trennstrich (U+002D, nur fuer Wortzusammensetzungen).

### Nicht-deutsche Anfuehrungszeichen in deutschen Sektionen

In deutschen Texten sind Anfuehrungszeichen in der unten-oben-Form korrekt.
Im LaTeX-Source stets `\enquote{...}` aus dem csquotes-Paket verwenden:

```latex
\usepackage[german]{csquotes}
% im Text:
\enquote{Das ist ein Zitat.}
```

### Umlaut-Ersatz verboten

Umlaute und Eszett immer korrekt schreiben. "oe", "ae", "ue", "ss" als Ersatz
fuer Umlaute und Eszett sind im Fliesstext verboten.

Ausnahme: Dateinamen, Shell-Variablen, YAML-Keys und andere technische
Kontexte ohne garantierte Unicode-Unterstuetzung.

---

## Laengen-Erwartungen

Hauptteil (Einleitung bis Fazit, ohne Verzeichnisse und Anhang) bei 12pt,
Zeilenabstand 1,5:

| Fachbereich | Erwarteter Umfang |
|---|---|
| BWL, Wirtschaftswissenschaften | 40 bis 60 Seiten |
| Informatik, Ingenieurwissenschaften | 30 bis 50 Seiten |
| Geistes- und Sozialwissenschaften | 50 bis 80 Seiten |

Hochschulspezifische Vorgaben koennen erheblich abweichen. Pruefungsordnung
und Pruefungsamt zuerst konsultieren.

Faustformel fuer das Verhaeltnis der Kapitel (Hauptteil = 100 %):
- Theoretischer Rahmen: 30 bis 40 %
- Methodik: 15 bis 20 %
- Ergebnisse: 20 bis 25 %
- Diskussion und Fazit: 20 bis 25 %

---

## Abstract / Zusammenfassung

Im DACH-Raum wird haeufig beides verlangt: eine deutsche Zusammenfassung und
ein englischer Abstract. Pruefe, ob die Hochschule beide oder nur eine Variante
vorschreibt.

**Umfang:** je ca. 250 Worte (Toleranz: 200 bis 300 Worte). Keine Referenzen,
keine unerklaerten Abkuerzungen, keine Abbildungen.

**Struktur (IMRaD-nah):**
1. Hintergrund/Kontext (2 bis 3 Saetze): Problem oder Forschungsluecke.
2. Methode (2 bis 3 Saetze): Was und wie untersucht wurde.
3. Ergebnisse (2 bis 3 Saetze): Wichtigste Befunde.
4. Schlussfolgerung (1 bis 2 Saetze): Bedeutung und Beitrag.

**Sprachliche Hinweise:**
- Zusammenfassung: korrekte deutsche Umlaute, wissenschaftlicher Stil.
- Abstract: britisches oder amerikanisches Englisch konsistent waehlen.
- Beide Varianten in der Vergangenheitsform (Arbeit ist bei Abgabe abgeschlossen).

**Platzierung:** Haeufig nach dem Titelblatt, vor dem Inhaltsverzeichnis.
Manche Hochschulen verlangen Platzierung nach den Verzeichnissen.

---

## Hochschul-Style-Guides (Beispiele)

Viele Hochschulen veroffentlichen eigene Leitfaeden. Diese haben stets Vorrang
vor allgemeinen Empfehlungen.

- **Universitaet Mannheim** (BWL): Leitfaden des Lehrstuhls regelt Schriftart
  (Times New Roman oder Arial), Randbreiten und Zitationsstil (APA oder Chicago).
- **TU Muenchen** (Ingenieurwissenschaften): Fakultaetsmerkblaetter regeln
  Anhangstruktur und Datenmanagement-Plan.
- **FU Berlin** (Geistes- und Sozialwissenschaften): Institutsabhaengige
  Vorgaben; viele Faecher nutzen Chicago Author-Date.
- **Fachhochschulen:** Kuerzere Leitfaeden, meist Deckblatt-Vorlage, Schriftart
  und maximaler Seitenumfang.

**Vorgehen:**
1. Pruefungsordnung lesen (Seitenumfang, Abgabemodalitaeten).
2. Leitfaden des betreuenden Lehrstuhls besorgen.
3. Abweichungen von Systemdefaults in `thesen/<name>/CLAUDE.md` vermerken.

---

## Verbindung zum Bachelorarbeits-System

Das System unterstuetzt das Schreiben auf zwei Ebenen:

**Inhaltliche Ebene (automatisiert):**
- `python -m rag search` findet belegte Aussagen und liefert direkt einfuegbare
  `\parencite`-Vorschlaege mit korrekter Seitenangabe.
- `python -m rag verify-quote` prueft, ob Paraphrasen zu nah an der Quelle
  sind (STRICT_MATCH, FUZZY_MATCH, THEMATIC_MATCH, NO_MATCH).
- `python -m rag extract-citations` auditiert das fertige `.tex`-File auf
  fehlende Bibliografieeintraege und unbelegte Bibkeys.

**Stilistische Ebene (manuell):**
Stilentscheidungen (Gendering-Ansatz, Ton, Satzstruktur, Einhaltung der
Konventionen in diesem Dokument) liegen beim Autor. Das System liefert
verifizierte Quellen und Zitierhilfen.

Das Bridge-Skill `bachelorarbeit-arbeitsweise` in
`tools/skills-overlay/scientific-writing/` verbindet die RAG-Kommandos mit
den hier beschriebenen Konventionen im Arbeitsablauf.

**Grundregel:** Das System erfindet keine Quellen. Liefert `verify-quote`
NO_MATCH und `search` keinen relevanten Treffer, ist die Behauptung im
aktuellen Korpus nicht belegt. Den Nutzer informieren, nicht raten.

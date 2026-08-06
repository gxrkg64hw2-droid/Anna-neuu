# DACH-Reporting-Standards (statistisch + qualitativ)

Grundlage: APA 7, DIN-Schreibweisen und Fachkonventionen deutschsprachiger Abschlussarbeiten.

## Quantitatives Reporting nach APA-DE

Allgemeine Schreibregeln fuer statistische Kennzahlen im deutschsprachigen Fliesstext:

- **Dezimaltrennzeichen**: Im deutschen Fliesstext gilt das Komma. Korrekt: "Der Mittelwert liegt
  bei M = 4,23 (SD = 0,87)". In Tabellen mit englischer Konvention ist der Punkt erlaubt, muss
  aber tabellenintern konsistent gehalten werden.
- **p-Werte**: Stets ohne fuehrende Null schreiben: "p = .023" oder "p = .001". Niemals "p = 0,023"
  oder "p = 0.000". Wenn p kleiner als .001, immer "p < .001" schreiben, nie einen exakten Wert
  angeben.
- **Effektgroessen**: IMMER zusammen mit dem Signifikanztest berichten. Gaengige Masse:
  - Cohens d (Mittelwertvergleiche zweier Gruppen): Richtwerte klein d = 0,2, mittel d = 0,5,
    gross d = 0,8.
  - Hedges g (korrigierte Variante bei ungleichen Gruppengroessen).
  - Eta-Quadrat eta2 und partielles Eta-Quadrat petaeta2 (ANOVA): klein .01, mittel .06, gross .14.
  - Omega-Quadrat omega2 (unverzerrte Alternative zu eta2).
  - Cramers V und Phi (Chi-Quadrat-Tests): klein .10, mittel .30, gross .50.
  - f2 (Regression nach Cohen): klein .02, mittel .15, gross .35.
- **Konfidenzintervalle**: 95 % CI [Untergrenze, Obergrenze] in eckigen Klammern. Die deutsche
  Variante "95 % KI" ist ebenfalls akzeptiert, aber innerhalb eines Dokuments konsistent halten.
  Beispiel: "95 % CI [0,12, 0,45]".
- **Pruefgroessen-Format**:
  - t-Test: t(df) = Wert, p = Wert, d = Wert
  - ANOVA: F(df1, df2) = Wert, p = Wert, eta2 = Wert
  - Chi-Quadrat: chi2(df, N = Stichprobengroesse) = Wert, p = Wert, V = Wert
  - Korrelation: r(df) = Wert, p = Wert
  - Regression: F(df1, df2) = Wert, p = Wert, R2 = Wert
- **Stichprobengroesse N**: Stets angeben, entweder direkt in der Pruefgroesse oder einmalig am
  Beginn des Ergebnisabschnitts als Kontextinformation.
- **Rundungsregel**: Pruefgroessen und Koeffizienten auf zwei Dezimalstellen, p-Werte auf drei
  Dezimalstellen (ausser "< .001").
- **Nullhypothesen-Signifikanztests allein genuegen nicht**: Immer Effektgroesse und
  Konfidenzintervall erwaehnen, damit Leser praktische Bedeutsamkeit beurteilen koennen.

## Beispiele formatierter Ergebnissaetze

Korrekt formatierte Ergebnissaetze fuer gaengige Verfahren:

1. **t-Test (unabhaengige Stichproben)**
   "Der Unterschied zwischen den Gruppen war statistisch signifikant, t(48) = 2,34, p = .024,
   d = 0,67, 95 % CI [0,09, 1,25]. Die Versuchsgruppe (M = 4,52, SD = 0,91) erzielte hoehere
   Werte als die Kontrollgruppe (M = 3,81, SD = 1,04)."

2. **Einfaktorielle ANOVA**
   "Die einfaktorielle Varianzanalyse ergab einen signifikanten Gruppeneffekt,
   F(2, 87) = 6,71, p = .002, eta2 = .13. Post-hoc-Tests (Tukey-HSD) zeigten, dass sich
   Gruppe A signifikant von Gruppe C unterschied (p = .003), nicht jedoch von Gruppe B (p = .241)."

3. **Chi-Quadrat-Test**
   "Die Haeufigkeitsverteilung unterschied sich signifikant von der erwarteten Verteilung,
   chi2(3, N = 120) = 9,84, p = .020, V = 0,29."

4. **Pearson-Korrelation**
   "Leistungsangst und Prokrastination korrelierten signifikant positiv, r(98) = .43, p < .001,
   95 % CI [.26, .58]."

5. **Multiple Regression**
   "Das Gesamtmodell war signifikant, F(3, 96) = 11,34, p < .001, R2 = .26. Selbstwirksamkeit
   (beta = .38, p < .001) und soziale Unterstuetzung (beta = .22, p = .031) sagten die
   Leistung signifikant vorher, Prokrastination hingegen nicht (beta = -.08, p = .347)."

6. **Mann-Whitney-U-Test (nicht-parametrisch)**
   "Der Mann-Whitney-U-Test ergab keinen signifikanten Unterschied zwischen den Gruppen,
   U = 312, z = -1,47, p = .141, r = .15."

7. **Mediationsanalyse (indirekter Effekt via Bootstrap)**
   "Der indirekte Effekt von Arbeitszufriedenheit auf Kuendigungsabsicht ueber emotionale
   Erschoepfung war signifikant, b = 0,18, 95 % CI [0,07, 0,31] (5.000 Bootstrap-Ziehungen)."

## Strukturgleichungsmodelle (PLS-SEM, CB-SEM)

Gueteberichterstattung auf zwei Ebenen: Messmodell und Strukturmodell.

### Messmodell (reflektiv)

| Guetekriterium | Schwellenwert | Bedeutung |
|---|---|---|
| Faktorladungen (outer loadings) | >= 0,70 | Indikator erklaert >= 49 % Varianz des Konstrukts |
| Average Variance Extracted (AVE) | >= 0,50 | Konvergenzvaliditaet |
| Composite Reliability (CR) | >= 0,70 (besser >= 0,80) | Interne Konsistenz |
| HTMT (Heterotrait-Monotrait Ratio) | < 0,85 (konservativ < 0,90) | Diskriminanzvaliditaet |
| Cronbachs Alpha | >= 0,70 | Ergaenzend angeben |

Ergaenzend: Cross-Loadings pruefen (jede Ladung soll hoeher auf dem Zielkonstrukt sein als auf
allen anderen).

### Strukturmodell

- **R-Quadrat (R2)**: Erklarte Varianz endogener Konstrukte. Schwellenwerte (PLS): schwach .25,
  moderat .50, substanziell .75 (Hair et al., 2022).
- **Q-Quadrat (Q2) via Blindfolding**: Q2 > 0 zeigt Prognoserelevanz des Modells.
- **Pfadkoeffizienten (beta)**: Mit t-Werten und p-Werten berichten (Bootstrapping mit mindestens
  5.000 Samples). Beispiel: beta = 0,42, t(499) = 5,83, p < .001.
- **Gesamteffekte fuer Mediationsmodelle**: Direkte Effekte, indirekte Effekte und Gesamteffekte
  tabellarisch aufluehren. Bootstrapped Konfidenzintervalle fuer den indirekten Effekt angeben.
- **Model Fit (CB-SEM)**: CFI >= 0,95, TLI >= 0,95, RMSEA <= 0,06, SRMR <= 0,08. Alternativ:
  chi2/df <= 3,0 als Daumenregel. Immer chi2-Wert, df und p berichten.
- **Common Method Bias**: Bei Selbstauskunftsdaten Harman-Single-Factor-Test oder CFA-Marker-
  Variablen-Ansatz beschreiben.

### Standardreferenz

Hair, J. F., Hult, G. T. M., Ringle, C. M., und Sarstedt, M. (2022). *A Primer on Partial Least
Squares Structural Equation Modeling (PLS-SEM)* (3. Aufl.). SAGE. doi:10.1007/978-3-030-80519-7

## Qualitative Inhaltsanalyse nach Mayring

De-facto-Standard fuer qualitative Auswertungen in deutschsprachigen Abschlussarbeiten.

### Pflichtbestandteile des Berichts

**1. Forschungsfrage und Materialgrundlage**
- Explizit formulierte Forschungsfrage, der die Analyse antwortet.
- Anzahl der Faelle bzw. Interviews sowie Auswahlbegruendung (theoretical sampling, maximale
  Variation, Expertenauswahl etc.).
- Kurzbeschreibung des Materials: Entstehungskontext, Erhebungsmethode, Aufzeichnung/
  Transkription, Anonymisierungsverfahren.

**2. Ablaufmodell**
Eines der drei Grundverfahren benennen und begruenden:
- *Zusammenfassung* (induktiv): Reduktion des Materials auf wesentliche Inhalte ohne vorherige
  Kategorien.
- *Strukturierung* (deduktiv): Anwendung eines vorab definierten Kategoriensystems auf das
  Material.
- *Explikation* (kontextbezogen): Erklaerung einzelner Textstellen durch engen oder weiten
  Kontext.

**3. Kategoriensystem**
Tabellarisch in folgender Form dokumentieren:

| Kategorie | Definition | Ankerbeispiel | Kodierregel |
|---|---|---|---|
| K1: Technologieakzeptanz | Aussagen, die Einstellungen gegenueber der Technologie beschreiben | "Das System ist intuitiv und spart mir viel Zeit." | Kodieren, wenn explizit Bewertung der Technologie (positiv oder negativ) vorliegt. |
| K2: Nutzungsbarrieren | Hinweise auf wahrgenommene Hindernisse bei der Nutzung | "Ich weiss nicht, wie ich anfangen soll." | Kodieren bei Aussagen ueber Unsicherheit, Fehlendes Wissen oder technische Probleme. |

**4. Intercoder-Reliabilitaet**
- Mindestens 2 unabhaengige Kodierer, die dasselbe Kategoriensystem auf eine Teilstichprobe
  des Materials anwenden (empfohlen: >= 20 % des Gesamtmaterials).
- Berechnung von Cohens Kappa. Mindestanforderung: kappa > 0,70 (gut), kappa > 0,80 (sehr gut).
- Formel: kappa = (P_o - P_e) / (1 - P_e), wobei P_o die beobachtete Uebereinstimmung und
  P_e die zufallig erwartete Uebereinstimmung darstellt.
- Diskrepanzen in einem Konsensgespraech klaeren und im Methodenteil dokumentieren.

**5. Auswertung und Darstellung**
- Haeufigkeitsanalyse: Anzahl der Kodierungen pro Kategorie und pro Fall.
- Repraesentative Ankerbeispiele (Zitate) aus dem Material, mit Quellenangabe (z. B.
  "Interview 3, Zeile 47-49").
- Zitate unveraendert uebernehmen, orthografische Eigenheiten beibehalten; Auslassungen mit
  [...] kennzeichnen.
- Schlussfolgerungen explizit aus den Kategorien ableiten, nicht frei interpretieren.

### Gaengige Software

- **MAXQDA**: De-facto-Standard im deutschsprachigen Raum, unterstuetzt mixed methods.
- **ATLAS.ti**: Verbreitet in der Sozialforschung, gute Netzwerkvisualisierung.
- **f4analyse**: Schlankes Tool, speziell fuer Interview-Transkripte, kostenlose Basisversion.

### Zentrales Nachschlagewerk

Mayring, Ph. (2022). *Qualitative Inhaltsanalyse: Grundlagen und Techniken* (13. Aufl.). Beltz.

## Qualitative Studien Reporting (allgemein)

Fuer qualitative Forschung jenseits der Inhaltsanalyse existieren etablierte Checklisten:

- **COREQ (Consolidated Criteria for Reporting Qualitative Research)**: 32-Item-Checkliste fuer
  Interviews und Fokusgruppen. Deckt Forschungsteam, Studiendesign, Analyse und Befunde ab.
  Referenz: Tong, A., Sainsbury, P., und Craig, J. (2007). doi:10.1093/intqhc/mzm042
- **SRQR (Standards for Reporting Qualitative Research)**: 21-Punkte-Checkliste fuer allgemeine
  qualitative Studien, breiter als COREQ. Referenz: O'Brien, B. C. et al. (2014). doi:10.1097/
  ACM.0000000000000388
- **CASP Qualitative Checklist**: Hilfreich zur Bewertung fremder qualitativer Studien im Rahmen
  eines Literaturreviews oder einer systematischen Synthese.

Bei Studien mit Interviews die jeweilige Checkliste als Appendix beifuegen und fehlende Kriterien
begruenden.

## Visualisierung von Ergebnissen

### Diagramme und Grafiken

- Keine 3D-Saeulen- oder Tortendiagramme. 3D-Effekte verzerren optisch und gelten als nicht
  wissenschaftlich.
- Klare deutsche Achsenbeschriftungen mit Einheitenangabe in eckigen Klammern, z. B.
  "Reaktionszeit [ms]".
- Farbpaletten colorblind-freundlich (z. B. Okabe-Ito oder viridis). Nie allein auf Farbe zur
  Datenkodierung verlaessen, zusaetzlich Muster oder Formunterscheidung nutzen.
- Fehlerbalken explizit in der Legende erklaeren: +/- 1 SD, +/- 1 SEM oder 95 % CI.
- Boxplots mit Einzeldatenpunkten (Jitter) bei n < 30 bevorzugen.

### Tabellen

- APA-7-Tabellenformat: Horizontale Linien nur am Tabellenanfang, nach dem Kopf und am Ende.
  Keine vertikalen Linien. In LaTeX: booktabs-Paket (\toprule, \midrule, \bottomrule).
- Tabellen vollstaendig beschriftend: Leser soll Tabelle ohne Blick in den Fliesstext verstehen.
- Signifikanzsterne wenn voehanden mit Legende erklaeren: *** p < .001, ** p < .01, * p < .05.
- Doppelte Berichterstattung vermeiden: Wenn eine Tabelle vorhanden ist, koennen Werte im
  Fliesstext zusammenfassend erwaehnt, aber nicht vollstaendig wiederholt werden.

### Beschriftungsregeln (Captions)

- **Tabellen**: Caption steht OBERHALB der Tabelle. Format: "Tabelle 4.2: Deskriptive Statistiken
  der Stichprobe". Nummerierung kapitelweise (4.2 = zweite Tabelle in Kapitel 4).
- **Abbildungen**: Caption steht UNTERHALB der Abbildung. Format: "Abbildung 4.1: Pfadmodell
  des Forschungsmodells nach Hair et al. (2022)."
- Quellenangabe bei uebernommenen Grafiken direkt in der Caption: "(eigene Darstellung)" oder
  "(Quelle: Autor Jahr, S. X)".

## Verbindung zu vorhandenen Werkzeugen

Vorlagen und Skripte im Bachelorarbeits-System, die direkt mit diesen Standards verknuepft sind:

- **scientific-visualization-Skill mit figure_export.py**: Plot-Setup exportiert Grafiken
  standardmaessig in 300 dpi (Print) und 96 dpi (Screen), je nach Ausgabepfad. Farbpalette
  colorblind-safe ist voreingestellt. Nutzung: `python figure_export.py --thesis <name>
  --figure <name> --dpi 300`.

- **mixed-methods-mayring-Profil**: Bringt `kategoriensystem.tex` mit, eine vorausgefuellte
  LaTeX-Tabelle im booktabs-Format fuer das Mayring-Kategoriensystem (Spalten: Kategorie,
  Definition, Ankerbeispiel, Kodierregel). Das Template liegt unter
  `tools/skills-overlay/statistical-analysis/templates/kategoriensystem.tex`.

- **empirisch-quantitativ-Profil**: Hat Tabellenvorlagen in `tabellen-vorlagen.tex`. Enthalten
  sind Vorlagen fuer Deskriptivstatistik, Korrelationsmatrizen, Regressionsoutput und
  Messmodellguete (PLS-SEM). Pfad: `tools/skills-overlay/statistical-analysis/templates/
  tabellen-vorlagen.tex`.

- **RAG-System (`python -m rag search`)**: Fuer jeden statistischen Begriff oder jede Methode
  zuerst `python -m rag search "<Methode>" --thesis <name>` laufen lassen, um korrekte
  Quellenbelege aus dem eigenen Korpus zu beziehen, bevor Standardwerke erwaehnt werden.

## Checkliste vor Abgabe des Ergebniskapitels

Alle Punkte vor jeder Einreichung abarbeiten.

### Quantitatives Reporting

- [ ] Alle Pruefgroessen mit Freiheitsgraden (df) und Stichprobengroesse (N) angegeben.
- [ ] Effektgroessen fuer jeden Signifikanztest berichtet (Cohens d, eta2, V etc.).
- [ ] 95 % Konfidenzintervalle angegeben, wo methodisch gefordert.
- [ ] Komma als Dezimaltrennzeichen im deutschen Fliesstext durchgaengig konsistent.
- [ ] p-Werte ohne fuehrende Null, kein "p = 0,000", stattdessen "p < .001".

### Strukturgleichungsmodelle

- [ ] Faktorladungen, AVE, CR und HTMT fuer das Messmodell tabellarisch berichtet.
- [ ] R2 und Q2 fuer alle endogenen Konstrukte angegeben.
- [ ] Pfadkoeffizienten mit Bootstrap-t-Werten, p-Werten und CI.
- [ ] Bei Mediation: direkter, indirekter und Gesamteffekt separat berichtet.

### Tabellen und Abbildungen

- [ ] Tabellen booktabs-formatiert (kein vertikales Gitter).
- [ ] Tabellen-Captions oberhalb, Abbildungs-Captions unterhalb.
- [ ] Kapitelweise Nummerierung korrekt (z. B. Tabelle 4.1, Abbildung 4.2).
- [ ] Abbildungen colorblind-freundlich und in ausreichender Aufloesung (>= 300 dpi fuer Print).
- [ ] Fehlerbalken in der Legende erklaert.

### Qualitative Studien

- [ ] Bei Mayring: Ablaufmodell und gewaaehltes Grundverfahren begruendet.
- [ ] Kategoriensystem mit Definition, Ankerbeispiel und Kodierregel vollstaendig dokumentiert.
- [ ] Intercoder-Reliabilitaet mit Cohens Kappa berichtet (kappa > 0,70).
- [ ] Zitate mit Quellenangabe (Interview-Nr., Zeile) belegt.
- [ ] Verwendete QDA-Software genannt.

### Allgemein

- [ ] Kein Ergebnis nur mit Signifikanz berichtet, ohne Effektgroesse.
- [ ] Alle Tabellen und Abbildungen im Text referenziert (z. B. "vgl. Tabelle 4.1").
- [ ] Literaturangaben fuer Schwellenwerte und Guetekriterien vorhanden.
- [ ] Methodik im Methoden-Kapitel entspricht dem, was im Ergebniskapitel berichtet wird.

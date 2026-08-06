# Profil: empirisch-quantitativ

Fuer empirisch-quantitative Bachelorarbeiten (BWL, Marketing, Sozialwissenschaften) mit Umfragen, Experimenten oder Strukturgleichungsmodellen.

**Kapitelstruktur:** Einleitung -> Theoretischer Rahmen -> Hypothesenentwicklung -> Methodik -> Ergebnisse -> Diskussion -> Fazit.

**Profil-spezifische Pakete:** `multirow`, `threeparttable`, erweiterte TikZ-Bibliotheken.

**Profil-spezifische Vorlagen** (in `tabellen-vorlagen.tex`):
- `\tabStichprobe` - Stichprobenbeschreibung
- `\tabReliabilitaet` - Reliabilitaet, CR, AVE
- `\tabPfadkoeffizienten` - Pfadkoeffizienten und Hypothesentests

**Compile:** `cd thesen/<name>/tex && latexmk -lualatex main.tex`

**Empfohlene Skills:**
- `hypothesis-generation` fuer Hypothesen
- `statistical-analysis` fuer Methodik und Ergebnisse
- `scientific-visualization` fuer Charts
- `scientific-critical-thinking` fuer Diskussion

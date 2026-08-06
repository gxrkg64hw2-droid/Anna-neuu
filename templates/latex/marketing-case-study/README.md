# Profil: marketing-case-study

Fuer Bachelorarbeiten in Marketing und BWL mit Marktanalyse-Charakter (Consulting-Stil).

**Kapitelstruktur:** Management Summary -> Marktanalyse -> Wettbewerbsanalyse -> Strategieempfehlung -> Roadmap -> Fazit.

**Profil-spezifische Pakete:** `colortbl`, `xcolor[table]`, erweiterte TikZ-Bibliotheken.

**TikZ-Frameworks** (in `frameworks.tex`):
- `\porterFiveForces{...}{...}{...}{...}{...}` - Porter Pentagon
- `\bcgMatrix{Stars}{QM}{CashCows}{Dogs}` - BCG-Matrix
- `\swotQuadrant{S}{W}{O}{T}` - SWOT-Quadrant
- `\tamSamSom{TAM}{SAM}{SOM}` - konzentrische Kreise

**Compile:** `cd thesen/<name>/tex && latexmk -lualatex main.tex`

**Empfohlene Skills:**
- `market-research-reports` als Strukturgeber
- `scientific-writing` fuer Schreibstil
- `scientific-critical-thinking` fuer Limitationen

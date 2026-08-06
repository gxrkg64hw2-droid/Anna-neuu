# Profil: theoretisch-konzeptionell

Fuer Bachelorarbeiten ohne Empirie: reine Literaturarbeiten, theoretische Synthesen, konzeptuelle Modellbildung.

**Kapitelstruktur:** Einleitung -> Begriffsapparat -> Theoretischer Rahmen -> Synthese -> Diskussion -> Fazit.

**Profil-spezifische Pakete:** minimal (`enumitem`).

**Profil-spezifische Vorlagen** (in `synthese-vorlagen.tex`):
- `\tabTheorienvergleich` - Theorienvergleichstabelle
- `\tabKonzeptmatrix` - Konzeptmatrix wer-sagt-was

**Compile:** `cd thesen/<name>/tex && latexmk -lualatex main.tex`

**Empfohlene Skills:**
- `scientific-writing` fuer Einleitung, Begriffsapparat, Fazit
- `literature-review` fuer Theoretischer Rahmen
- `scientific-brainstorming` fuer Synthese-Phase
- `scientific-critical-thinking` fuer Diskussion

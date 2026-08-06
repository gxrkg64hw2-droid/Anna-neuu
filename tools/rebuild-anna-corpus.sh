#!/bin/bash
# Rekonstruiert den lokalen Korpus der Thesis anna-postmigrantisch-theater aus der
# hochgeladenen Anna.zip (die geschützten PDFs liegen NICHT im Git).
#
# Aufruf:  bash tools/rebuild-anna-corpus.sh /pfad/zur/Anna.zip
set -euo pipefail

ZIP="${1:-}"
if [[ -z "$ZIP" || ! -f "$ZIP" ]]; then
  echo "Usage: bash tools/rebuild-anna-corpus.sh /pfad/zur/Anna.zip" >&2
  exit 1
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DST="$REPO/thesen/anna-postmigrantisch-theater/pdfs"
WORK="$(mktemp -d)"
mkdir -p "$DST"

echo "Entpacke $ZIP ..."
unzip -o -q "$ZIP" -d "$WORK"
SRC="$WORK/Anna"
[[ -d "$SRC" ]] || SRC="$(dirname "$(find "$WORK" -name 'Quelle - Postmigrantisch denken Teil1*' -print -quit)")"

echo "Kopiere Buch-PDFs ..."
cp "$SRC/Quelle - Postmigrantisch denken Teil1 S1-142.pdf"          "$DST/postmigrantisch-denken-teil1.pdf"
cp "$SRC/Quelle - Postmigrantisch denken Teil2 S143-283.pdf"        "$DST/postmigrantisch-denken-teil2.pdf"
cp "$SRC/Quelle - Postmigrantische Visionen Teil1 S1-129.pdf"       "$DST/postmigrantische-visionen-teil1.pdf"
cp "$SRC/Quelle - Postmigrantische Visionen Teil2 S130-257.pdf"     "$DST/postmigrantische-visionen-teil2.pdf"
cp "$SRC/Theaterwissenschaft postkolonialdekolonial Teil1 S1-150.pdf"   "$DST/theaterwissenschaft-postkolonial-teil1.pdf"
cp "$SRC/Theaterwissenschaft postkolonialdekolonial Teil2 S151-299.pdf" "$DST/theaterwissenschaft-postkolonial-teil2.pdf"

echo "Erzeuge Interview-PDF aus docx ..."
python3 - "$SRC/Interview Die Herkunft spielt keine Rolle.docx" > "$WORK/interview.txt" <<'PY'
import zipfile, re, html, sys
z = zipfile.ZipFile(sys.argv[1])
xml = z.read('word/document.xml').decode('utf-8','ignore')
xml = xml.replace('</w:p>','\n'); xml = re.sub(r'<w:tab[^>]*/>','\t', xml)
print(html.unescape(re.sub(r'<[^>]+>','', xml)))
PY

cd "$REPO"
uv run python - "$DST/interview-langhoff-2011-bpb.pdf" "$WORK/interview.txt" <<'PY'
import fitz, sys, textwrap
out, src = sys.argv[1], sys.argv[2]
paras = [p.strip() for p in open(src, encoding="utf-8").read().split("\n") if p.strip()]
doc = fitz.open(); left, leading, bottom = 60, 15, 780
def page(): return doc.new_page(width=595, height=842), 60
p, y = page()
def line(s, size=11):
    global p, y
    if y > bottom: p, y = page()
    p.insert_text((left, y), s, fontsize=size, fontname="helv"); y += leading
line("Die Herkunft spielt keine Rolle - Postmigrantisches Theater im Ballhaus Naunynstrasse", 12)
line("Interview mit Shermin Langhoff. bpb.de, 10.03.2011.", 10); y += 6
for para in paras[3:]:
    for w in (textwrap.wrap(para, width=95) or [""]): line(w)
    y += 6
doc.save(out); print("Interview-PDF:", doc.page_count, "Seiten ->", out)
PY

echo "Fertig. Korpus:"
ls -la "$DST"/*.pdf
echo "Nächster Schritt: uv run python -m rag index --thesis anna-postmigrantisch-theater"

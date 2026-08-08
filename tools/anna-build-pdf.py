#!/usr/bin/env python
import re, sys, html as _html, os, tempfile
import fitz

SRC = "/home/user/Anna-neuu/thesen/anna-postmigrantisch-theater/arbeit.md"
OUT = sys.argv[1]
TMP = tempfile.mkdtemp()

# ---------- Ränder / Seitenmaße ----------
CM = 28.3465
PAGE = fitz.paper_rect("a4")
L, R, T, B = 2.5*CM, 3.5*CM, 2.5*CM, 2.0*CM
WHERE = fitz.Rect(L, T, PAGE.width - R, PAGE.height - B)

CSS = """
* { font-family: serif; }
body { font-size: 12pt; line-height: 1.5; text-align: justify; }
h1 { font-size: 14pt; font-weight: bold; text-align: left; margin: 14pt 0 6pt 0; }
h2 { font-size: 12pt; font-weight: bold; text-align: left; margin: 10pt 0 4pt 0; }
p  { margin: 0 0 6pt 0; }
p.ref { margin: 0 0 6pt 0; padding-left: 22pt; text-indent: -22pt; text-align: left; }
"""

# ---------- Markdown -> HTML (Einleitung..Fazit) ----------
def esc(s): return _html.escape(s)
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s

lines = open(SRC, encoding="utf-8").read().splitlines()
body_html, started = [], False
for ln in lines:
    s = ln.rstrip()
    if s.startswith("# ") or s.startswith(">") or s.strip().startswith("<!--"): continue
    if s.strip() == "---": continue
    if s.startswith("### "):
        body_html.append(f"<h2>{inline(s[4:].strip())}</h2>"); started=True; continue
    if s.startswith("## "):
        body_html.append(f"<h1>{inline(s[3:].strip())}</h1>"); started=True; continue
    if not s.strip(): continue
    if not started: continue
    body_html.append(f"<p>{inline(s.strip())}</p>")

# Literaturverzeichnis
refs = [
 "Balme, Christopher B. (2022): Theaterwissenschaft und Postkolonialismus. Ein fachgeschichtlicher und persönlicher Rückblick. In: Sharifi, Azadeh/Skwirblies, Lisa (Hg.): Theaterwissenschaft postkolonial/dekolonial. Eine kritische Bestandsaufnahme. Bielefeld: transcript, S. 225–246.",
 "Carvalho, Wagner/Larsson, Fabian (2022): Ballhaus Naunynstraße. Theater einer offenen Gesellschaft. In: Sharifi, Azadeh/Skwirblies, Lisa (Hg.): Theaterwissenschaft postkolonial/dekolonial. Eine kritische Bestandsaufnahme. Bielefeld: transcript, S. 247–256.",
 "Hill, Marc/Yıldız, Erol (Hg.) (2018): Postmigrantische Visionen. Erfahrungen – Ideen – Reflexionen. Bielefeld: transcript.",
 "Langhoff, Shermin (2011): Die Herkunft spielt keine Rolle – „Postmigrantisches“ Theater im Ballhaus Naunynstraße. Interview, bpb.de, 10.03.2011. Online: https://www.bpb.de [Abruf: 06.08.2026].",
 "Sharifi, Azadeh/Skwirblies, Lisa (Hg.) (2022): Theaterwissenschaft postkolonial/dekolonial. Eine kritische Bestandsaufnahme. Bielefeld: transcript.",
 "Yıldız, Erol (2018): Vom methodologischen Nationalismus zu postmigrantischen Visionen. In: Hill, Marc/Yıldız, Erol (Hg.): Postmigrantische Visionen. Erfahrungen – Ideen – Reflexionen. Bielefeld: transcript, S. 43–62.",
 "Yıldız, Erol (2025): Postmigrantisch denken. Heimisch in einer globalisierten Gesellschaft. Bielefeld: transcript.",
]
body_html.append("<h1>Literaturverzeichnis</h1>")
for r in refs: body_html.append(f'<p class="ref">{esc(r)}</p>')
BODY = "<html><body>" + "\n".join(body_html) + "</body></html>"

def render_story(html, path, collect=False):
    story = fitz.Story(html=html, user_css=CSS)
    writer = fitz.DocumentWriter(path)
    headings = []
    def recorder(el):
        if collect and el.heading and (el.open_close & 1):  # nur beim Öffnen
            headings.append((el.text.strip(), el.heading, el.page))
    more, pno = 1, 0
    while more:
        dev = writer.begin_page(PAGE)
        more, _ = story.place(WHERE)
        story.element_positions(recorder, {"page": pno})
        story.draw(dev)
        writer.end_page()
        pno += 1
    writer.close()
    return pno, headings

# ---------- Pass 1: Body rendern (Heading-Seiten mitschreiben) ----------
body_pdf = os.path.join(TMP, "body.pdf")
n_body, headings = render_story(BODY, body_pdf, collect=True)

# Fußzeile (Seitenzahlen ab 1) auf Body-Seiten
docb = fitz.open(body_pdf)
for i, pg in enumerate(docb):
    pg.insert_text((PAGE.width/2 - 20, PAGE.height - B/2), f"{i+1}",
                   fontname="tiro", fontsize=10)

# ---------- TOC aus erfassten Headings (Seitenzahl = Fußzeile = page0+1) ----------
toc = [(t, lvl, p0 + 1) for (t, lvl, p0) in headings]

# ---------- Titelblatt ----------
TITLE = """<html><body>
<p style="text-align:center;margin-top:6pt">[Universität / Hochschule]</p>
<p style="text-align:center">[Institut / Fachbereich]</p>
<p style="text-align:center">Seminar: [Seminartitel]</p>
<p style="text-align:center">Leitung: [Titel Vorname Nachname]</p>
<p style="text-align:center;margin-bottom:60pt">[Semester, z. B. Sommersemester 2026]</p>
<p style="text-align:center;font-size:18pt;margin-top:80pt"><b>Kunst und Gesellschaftskritik</b></p>
<p style="text-align:center;font-size:14pt"><b>Theater und Satire als Räume postmigrantischer Sichtbarkeit und Zugehörigkeit</b></p>
<p style="text-align:center;margin-bottom:80pt">Seminararbeit</p>
<p style="text-align:center;margin-top:60pt">vorgelegt von</p>
<p style="text-align:center"><b>[Vor- und Nachname]</b></p>
<p style="text-align:center">Studienkennzahl: [xxx] · Matrikelnummer: [xxx]</p>
<p style="text-align:center">[E-Mail]</p>
<p style="text-align:center;margin-top:24pt">Abgabedatum: 09. August 2026</p>
</body></html>"""
title_pdf = os.path.join(TMP, "title.pdf"); render_story(TITLE, title_pdf)[0]

# ---------- Inhaltsverzeichnis (manuell: rechtsbündig + Punktführung) ----------
toc_doc = fitz.open()
tp = toc_doc.new_page(width=PAGE.width, height=PAGE.height)
x0, x1 = L, PAGE.width - R
y = T + 8
tp.insert_text((x0, y), "Inhaltsverzeichnis", fontname="tibo", fontsize=14); y += 30
dotw = fitz.get_text_length(".", fontname="tiro", fontsize=12)
for text, lvl, p in toc:
    indent = 20 if lvl == 2 else 0
    tx = x0 + indent
    num = str(p)
    numw = fitz.get_text_length(num, fontname="tiro", fontsize=12)
    tw = fitz.get_text_length(text, fontname="tiro", fontsize=12)
    tp.insert_text((tx, y), text, fontname="tiro", fontsize=12)
    tp.insert_text((x1 - numw, y), num, fontname="tiro", fontsize=12)
    ds, de = tx + tw + 4, x1 - numw - 4
    if de > ds:
        n = int((de - ds) / dotw)
        tp.insert_text((ds, y), "." * n, fontname="tiro", fontsize=12, color=(0.4,0.4,0.4))
    y += 22

# ---------- Zusammensetzen: Titel + TOC + Body ----------
final = fitz.open()
final.insert_pdf(fitz.open(title_pdf))
final.insert_pdf(toc_doc)
final.insert_pdf(docb)
final.save(OUT, deflate=True)
print(f"PDF: {final.page_count} Seiten (Body {n_body}) -> {OUT}")
print("TOC:", [(t, p) for t, l, p in toc])

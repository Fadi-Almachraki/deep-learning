#!/usr/bin/env python3
"""Build the offline HTML and the printable PDF from index.html.

index.html loads its typefaces from Google Fonts. This script fetches those
faces, subsets them to the ~160 characters the page actually uses, pins the
optical-size axis (the page never varies it), embeds them as base64 woff2, and
wraps the result in a full HTML document — producing a single file that renders
identically with no network at all.

    pip install fonttools brotli playwright
    python3 build-offline.py

Outputs Barcelona-to-Madrid.html and, if Playwright is installed,
Barcelona-to-Madrid.pdf.
"""
import base64, html, io, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
OUT_HTML = os.path.join(HERE, "Barcelona-to-Madrid.html")
OUT_PDF = os.path.join(HERE, "Barcelona-to-Madrid.pdf")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# Newsreader has no arrow glyphs; arrows only ever render in the display and
# mono faces, so that gap is intentional rather than a coverage failure.
EXEMPT = {"Newsreader": set("←→")}


def wanted_characters(src):
    chars = set(html.unescape(src)) | {chr(c) for c in range(32, 127)}
    chars |= set("—–·…‘’“”«»€°×→←•±ºª¿¡")
    chars |= set("áéíóúüñÁÉÍÓÚÜÑàèìòùÀÈÌÒÙâêîôûçÇïÏäöëÄÖËŀ")
    return sorted(c for c in chars if ord(c) > 31 and ord(c) != 127)


def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()


def embed_fonts(src, chars):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    from fontTools.pens.boundsPen import BoundsPen

    link = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com[^"]+)"', src)
    if not link:
        sys.exit("no Google Fonts stylesheet found in index.html")
    css = fetch(html.unescape(link.group(1))).decode()

    faces = []
    for block in re.findall(r"@font-face\s*\{.*?\}", css, re.S):
        family = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        style = re.search(r"font-style:\s*([^;]+);", block).group(1).strip()
        url = re.search(r"url\((https://[^)]+)\)", block).group(1)
        need = [c for c in chars if c not in EXEMPT.get(family, set())]

        font = TTFont(io.BytesIO(fetch(url)))
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.notdef_outline = True
        opts.drop_tables += ["DSIG"]
        sub = subset.Subsetter(options=opts)
        sub.populate(text="".join(need))
        sub.subset(font)
        if "fvar" in font and any(a.axisTag == "opsz" for a in font["fvar"].axes):
            font = instancer.instantiateVariableFont(font, {"opsz": 16})

        cmap = font.getBestCmap()
        missing = [c for c in need if ord(c) not in cmap]
        if missing:
            sys.exit(f"{family} {style} is missing {missing!r}")
        pen = BoundsPen(font.getGlyphSet())
        font.getGlyphSet()[cmap[ord("B")]].draw(pen)
        if not pen.bounds or pen.bounds[2] <= 0:
            sys.exit(f"{family} {style} subsetted to empty outlines")

        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        font.close()
        print(f"  {family:14} {style:7} {buf.tell()/1024:5.1f} KB  {len(cmap)} glyphs")
        data = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
        faces.append(re.sub(r"url\(https://[^)]+\)", "url(" + data + ")", block).strip())

    src = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", src)
    src = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>',
                 '<style id="embedded-fonts">\n' + "\n".join(faces) + "\n</style>", src, count=1)
    assert "fonts.googleapis.com" not in src and "fonts.gstatic.com" not in src
    return src


def wrap(body):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<meta name="description" content="Wharton MBA for Executives, Global Business '
            'Week 2026 — the Barcelona to Madrid itinerary, with venue histories, fun facts '
            'and map links.">\n<meta name="color-scheme" content="light dark">\n'
            "<style>html{color-scheme:light dark}body{margin:0}img{max-width:100%}"
            "[hidden]{display:none!important}</style>\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")


def render_pdf():
    script = r"""
import sys
from playwright.sync_api import sync_playwright
out, page_url = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1100, "height": 1400})
    ctx.route("**", lambda r: r.continue_() if r.request.url.startswith("file:") else r.abort())
    p = ctx.new_page()
    p.goto(page_url, wait_until="load")
    p.evaluate("document.fonts.ready")
    p.wait_for_timeout(1200)
    p.pdf(path=out, format="A4", print_background=True,
          margin={"top": "13mm", "right": "13mm", "bottom": "15mm", "left": "13mm"},
          display_header_footer=True, header_template="<div></div>",
          footer_template=('<div style="width:100%;font:7.5pt Helvetica,sans-serif;color:#8a9095;'
                           'padding:0 13mm;display:flex;justify-content:space-between;letter-spacing:.06em">'
                           '<span>GBW SPAIN 2026 &nbsp;&middot;&nbsp; BARCELONA TO MADRID</span>'
                           '<span class="pageNumber"></span></div>'))
    b.close()
"""
    subprocess.run([sys.executable, "-c", script, OUT_PDF, "file://" + OUT_HTML], check=True)


if __name__ == "__main__":
    source = open(SRC, encoding="utf-8").read()
    print("subsetting fonts:")
    page = embed_fonts(source, wanted_characters(source))
    open(OUT_HTML, "w", encoding="utf-8").write(wrap(page))
    print(f"wrote {OUT_HTML}  ({os.path.getsize(OUT_HTML)/1024:.0f} KB)")
    try:
        render_pdf()
        print(f"wrote {OUT_PDF}  ({os.path.getsize(OUT_PDF)/1024:.0f} KB)")
    except Exception as exc:
        print(f"skipped PDF ({exc})")

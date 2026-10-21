#!/usr/bin/env python3
"""
Builds bird.pdf from bird.md in the same visual style as
IQJ-manifest.pdf (pdf/template.html): stdlib + a system
google-chrome-stable/chromium doing the HTML -> PDF conversion headless.

    python3 bird_build.py [source.md] [out.pdf]

bird.md follows README.md's heading shape, so it is read directly:
    # <title>                         -> <h1>   (document title)
    ## 🜁 Глава Первая. <title>       -> <h2>   (chapter, 🜁 printed as △)
    ### §N                            -> <h3>   (section, numbered through)
    blank-line separated text         -> <p>

pdf/build.py and pdf/template.html are left untouched; the CSS below is
their stylesheet adapted to prose (chapters instead of books, red-line
indents instead of spaced paragraphs).
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "tools"))
import manifesto  # noqa: E402  (inline() and format_updated() only)

SOURCE = ROOT / "bird.md"
OUT_PDF = ROOT / "bird.pdf"

CHROME_CANDIDATES = [
    "google-chrome-stable",
    "google-chrome",
    "chromium-browser",
    "chromium",
]

TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title><!--TITLE--></title>
<style>
  @page { size: A4; margin: 22mm 20mm 22mm 20mm; }
  * { box-sizing: border-box; }
  body {
    font-family: "Liberation Serif", "DejaVu Serif", "Noto Serif", serif;
    font-size: 11.5pt; line-height: 1.55; color: #241a12; background: #fdfaf3;
  }
  h1 {
    font-family: "Liberation Serif", serif; font-size: 20pt; text-align: center;
    letter-spacing: 0.02em; margin: 0 0 10mm 0; padding-bottom: 6mm;
    border-bottom: 2px solid #7a4a1e; color: #4a2e0e; page-break-after: avoid;
  }
  h2 {
    font-size: 15pt; color: #7a3b12; margin-top: 14mm; margin-bottom: 4mm;
    padding-bottom: 2mm; border-bottom: 1px solid #c9a86a;
    page-break-after: avoid; page-break-before: auto;
  }
  h1 + h2 { margin-top: 0; }
  h3 { font-size: 12.5pt; color: #5a3a1a; margin-top: 7mm; margin-bottom: 2.5mm; page-break-after: avoid; }
  p { margin: 0 0 1.5mm 0; text-indent: 7mm; text-align: justify; orphans: 3; widows: 3; }
  h3 + p { text-indent: 0; }
  em { color: #6b4423; font-style: italic; }
  strong { color: #3a2410; }
  hr { border: none; border-top: 1px solid #c9a86a; margin: 8mm 0; }
  /* Colophon: last-updated timestamp, the very last line of the document */
  .colophon {
    text-indent: 0; text-align: center; font-style: italic; font-size: 9pt; color: #9a7a4a;
    letter-spacing: 0.05em; margin-top: 10mm; page-break-before: avoid;
  }
</style>
</head>
<body>
<!--BODY-->
</body>
</html>
"""


def find_chrome() -> str:
    for name in CHROME_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    sys.exit(
        "No headless-capable Chrome/Chromium found on PATH "
        f"(tried: {', '.join(CHROME_CANDIDATES)}). Install one, or edit "
        "CHROME_CANDIDATES in bird_build.py to point at yours."
    )


def build_html(source: Path) -> str:
    title = source.stem
    parts = []
    chapters = 0
    for block in source.read_text(encoding="utf-8").split("\n\n"):
        block = " ".join(block.split())
        if not block:
            continue
        if block.startswith("### "):
            parts.append(f"<h3>{block[4:]}</h3>")
        elif block.startswith("## "):
            chapters += 1
            if chapters > 1:
                parts.append("<hr />")
            # Same substitution as pdf/build.py: 🜁 falls back to an ugly
            # glyph in print fonts, the plain triangle reads the same.
            heading = manifesto.inline(block[3:]).replace("🜁", "△")
            parts.append(f"<h2>{heading}</h2>")
        elif block.startswith("# "):
            title = block[2:]
            parts.append(f"<h1>{manifesto.inline(title)}</h1>")
        else:
            parts.append(f"<p>{manifesto.inline(block)}</p>")
    parts.append(f'<p class="colophon">{manifesto.format_updated(source)}</p>')

    out = TEMPLATE.replace("<!--TITLE-->", manifesto.inline(title))
    return out.replace("<!--BODY-->", "\n".join(parts))


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE
    out_pdf = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT_PDF
    chrome = find_chrome()
    html_out = build_html(source)

    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "bird.html"
        html_path.write_text(html_out, encoding="utf-8")

        subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--no-pdf-header-footer",
                f"--print-to-pdf={out_pdf.resolve()}",
                "--print-to-pdf-no-header",
                f"file://{html_path}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    size_kb = out_pdf.stat().st_size // 1024
    print(f"wrote {out_pdf} ({size_kb} KB)")


if __name__ == "__main__":
    main()

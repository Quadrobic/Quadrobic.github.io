#!/usr/bin/env python3
"""
Builds bird.html from bird.md — the "Сухая грусть на дне очей" bonus story,
reusing the treatise site's own look, scroll choreography, TTS reader and
text-size controls (css/style.css, js/main.js, js/ink.js) via bird_template.html.

Deliberately NOT routed through tools/manifesto.py: that parser's grammar
(Книга/§N-with-title/Аксиоматика/Словарь/...) is shaped for the treatise,
and bird.md is a different kind of document - plain chapters of continuous
prose, with bare, untitled "### §N" scene markers rather than numbered,
titled sections. Only manifesto.inline() (bold/italic/§-ref markup) and
manifesto.format_updated() (the footer colophon) are borrowed from it.

RU-only by design (no English/Thai translation of this text is planned),
so unlike build.py there is no per-language loop here.

    python3 build_bird.py

(also run by ./rebuild.sh alongside the treatise site and PDF)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "tools"))
import manifesto  # noqa: E402  (inline() and format_updated() only)

SOURCE = ROOT / "bird.md"
TEMPLATE = ROOT / "bird_template.html"
OUT = ROOT / "bird.html"

CHAPTER_RE = re.compile(r"Глава (\S+)\.\s*(.+)")

# Scene-setting for the ink background, one mood per chapter - see
# js/ink.js for what each mood looks like. The arc runs from the ordinary
# ("flow") down into the story's murk and settles on "calm" for its quiet,
# emptied-out ending.
CHAPTER_MOODS = ["flow", "murk", "murk", "calm"]


def parse(md: str):
    """-> (title, [{"title": str, "roman": str, "paragraphs": [html,...]}])"""
    title = None
    chapters = []
    current = None

    for block in md.split("\n\n"):
        block = " ".join(block.split())
        if not block:
            continue
        if block.startswith("# "):
            title = manifesto.inline(block[2:])
        elif block.startswith("## "):
            m = CHAPTER_RE.match(block[3:].lstrip("🜁").strip())
            roman = manifesto.BOOK_NUM_WORDS.get(m.group(1), str(len(chapters) + 1)) if m else str(len(chapters) + 1)
            chapter_title = manifesto.inline(m.group(2)) if m else manifesto.inline(block[3:])
            current = {"title": chapter_title, "roman": roman, "paragraphs": []}
            chapters.append(current)
        elif block.startswith("### "):
            # Bare scene marker ("§N") - not rendered as a heading, just a
            # cue to break the flow with a scene divider before what's next.
            if current is not None and current["paragraphs"]:
                current["paragraphs"].append(None)  # None = scene-break marker
        else:
            if current is not None:
                current["paragraphs"].append(manifesto.inline(block))

    return title, chapters


def render_chapter(chapter, index):
    mood = CHAPTER_MOODS[(index - 1) % len(CHAPTER_MOODS)]
    body = []
    for p in chapter["paragraphs"]:
        if p is None:
            body.append('<div class="scene-break" aria-hidden="true">◆</div>')
        else:
            body.append(f'<p class="reveal">{p}</p>')
    return f"""
<section class="book" id="chapter-{index}" data-book="{index}" data-mood="{mood}">
  <div class="book-divider">
    <span class="book-roman">{chapter["roman"]}</span>
    <h2 class="book-title reveal-title">{chapter["title"]}</h2>
    <span class="glyph-line" aria-hidden="true">△</span>
  </div>
  <div class="book-body story-body">
    {''.join(body)}
  </div>
</section>
"""


def render_nav(chapters):
    items = []
    for i, ch in enumerate(chapters, start=1):
        items.append(
            f'<a href="#chapter-{i}" class="nav-dot" data-target="chapter-{i}" title="{ch["title"]}">'
            f'<span class="nav-glyph">{ch["roman"]}</span><span class="nav-label">{ch["title"]}</span></a>'
        )
    return "\n".join(items)


def main():
    title, chapters = parse(SOURCE.read_text(encoding="utf-8"))
    updated = manifesto.format_updated(SOURCE)

    chapters_html = "\n".join(render_chapter(ch, i) for i, ch in enumerate(chapters, start=1))
    nav_html = render_nav(chapters)

    out = TEMPLATE.read_text(encoding="utf-8")
    out = out.replace("<!--TITLE-->", title)
    out = out.replace("<!--DESC-->", "Сухая грусть на дне очей - рассказ.")
    out = out.replace("<!--HERO_TITLE-->", title)
    out = out.replace("<!--HERO_SUBTITLE-->", "Рассказ")
    out = out.replace("<!--CHAPTERS-->", chapters_html)
    out = out.replace("<!--NAV-->", nav_html)
    out = out.replace("<!--FOOTER-->", title)
    out = out.replace("<!--UPDATED-->", updated)

    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT} ({len(out)} bytes), {len(chapters)} chapters")


if __name__ == "__main__":
    main()

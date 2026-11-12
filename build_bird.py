#!/usr/bin/env python3
"""
Builds bird.html / bird.en.html from bird.md / bird.en.md — the bonus story,
reusing the treatise site's own look, scroll choreography, TTS reader and
text-size controls (css/style.css, js/main.js, js/ink.js) via bird_template.html.

Deliberately NOT routed through tools/manifesto.py: that parser's grammar
(Книга/§N-with-title/Аксиоматика/Словарь/...) is shaped for the treatise,
and bird.md is a different kind of document - plain chapters of continuous
prose, with bare, untitled "### §N" scene markers rather than numbered,
titled sections. Only manifesto.inline() (bold/italic/§-ref markup) and
manifesto.format_updated() (the footer colophon) are borrowed from it.

The two editions share the presentation and localize their reading controls.

    python3 build_bird.py

(also run by ./rebuild.sh alongside the treatise site and PDF)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "tools"))
import manifesto  # noqa: E402  (inline() and format_updated() only)

TEMPLATE = ROOT / "bird_template.html"

CHAPTER_RE = {
    "ru": re.compile(r"Глава (\S+)\.\s*(.+)"),
    "en": re.compile(r"Chapter ([IVX]+)\.\s*(.+)"),
}

LANGS = {
    "ru": {
        "source": "bird.md", "out": "bird.html", "treatise": "index.html",
        "subtitle": "Рассказ", "menu": "Меню", "nav_aria": "Главы рассказа",
        "back": "Трактат", "back_footer": "Вернуться к трактату",
        "scroll": "прокрутите, чтобы начать",
        "sound_aria": "Переключить фоновый звук", "sound_title": "Звук",
        "tts_aria": "Слушать рассказ вслух", "tts_title": "Слушать",
        "voice_aria": "Голос и скорость чтения", "voice_title": "Голос и скорость",
        "pdf_aria": "Скачать PDF", "pdf_title": "Скачать PDF",
        "dec_aria": "Уменьшить размер текста", "dec_title": "Меньше текста",
        "inc_aria": "Увеличить размер текста", "inc_title": "Больше текста",
    },
    "en": {
        "source": "bird.en.md", "out": "bird.en.html", "treatise": "index.en.html",
        "subtitle": "A short story", "menu": "Menu", "nav_aria": "Story chapters",
        "back": "Treatise", "back_footer": "Return to the treatise",
        "scroll": "scroll to begin",
        "sound_aria": "Toggle ambient sound", "sound_title": "Sound",
        "tts_aria": "Listen to the story", "tts_title": "Listen",
        "voice_aria": "Voice and reading speed", "voice_title": "Voice & speed",
        "pdf_aria": "Download PDF in Russian", "pdf_title": "PDF (Russian)",
        "dec_aria": "Decrease text size", "dec_title": "Smaller text",
        "inc_aria": "Increase text size", "inc_title": "Larger text",
    },
}

# Scene-setting for the ink background, one mood per chapter - see
# js/ink.js for what each mood looks like. The arc runs from the ordinary
# ("flow") down into the story's murk and settles on "calm" for its quiet,
# emptied-out ending.
CHAPTER_MOODS = ["flow", "murk", "murk", "calm"]


def parse(md: str, lang="ru"):
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
            m = CHAPTER_RE[lang].match(block[3:].lstrip("🜁").strip())
            roman = str(len(chapters) + 1)
            if m:
                roman = manifesto.BOOK_NUM_WORDS.get(m.group(1), roman) if lang == "ru" else m.group(1)
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


def build(lang, meta):
    source = ROOT / meta["source"]
    title, chapters = parse(source.read_text(encoding="utf-8"), lang)
    updated = manifesto.format_updated(source, lang=lang)

    chapters_html = "\n".join(render_chapter(ch, i) for i, ch in enumerate(chapters, start=1))
    nav_html = render_nav(chapters)

    out = TEMPLATE.read_text(encoding="utf-8")
    out = out.replace("<!--TITLE-->", title)
    out = out.replace("<!--DESC-->", f'{title} — {meta["subtitle"]}.')
    out = out.replace("<!--HERO_TITLE-->", title)
    out = out.replace("<!--LANG-->", lang)
    for key, value in meta.items():
        out = out.replace(f"<!--{key.upper()}-->", value)
    out = out.replace("<!--CHAPTERS-->", chapters_html)
    out = out.replace("<!--NAV-->", nav_html)
    out = out.replace("<!--FOOTER-->", title)
    out = out.replace("<!--UPDATED-->", updated)

    target = ROOT / meta["out"]
    target.write_text(out, encoding="utf-8")
    print(f"wrote {target} ({len(out)} characters), {len(chapters)} chapters")


def main():
    for lang, meta in LANGS.items():
        build(lang, meta)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Builds index.html / index.en.html / index.th.html from README.md /
README.en.md / README.th.md via the shared parser in tools/manifesto.py.

Re-run after any edit to any of the three source files:

    python3 build.py

(or just run ./rebuild.sh, which rebuilds the site and the PDF together)
"""
import html
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "tools"))
import manifesto  # noqa: E402
from web_glossary import glossary_json  # noqa: E402
import model_annotations  # noqa: E402

TEMPLATE = ROOT / "template.html"

# Everything that differs between languages lives here: the source file,
# the output file, and every bit of UI copy that template.html doesn't get
# from parsing the manifesto itself (meta description, button labels, the
# hero banner, the footer line...).
LANGS = {
    "ru": {
        "readme": ROOT / "README.md",
        "out": ROOT / "index.html",
        "lang_attr": "ru",
        "desc": "Имперский Квадроберский Джайнизм - трактат о Свабхаве, Хридае и Пути Служения.",
        "hero_title": "Имперский<br>Квадроберский<br>Джайнизм",
        "hero_subtitle": "Трактат о Свабхаве, Хридае и Пути Служения",
        "scroll_cue": "прокрутите, чтобы войти в русло",
        "footer": "Имперский Квадроберский Джайнизм",
        "nav_aria": "Книги трактата",
        "sound_aria": "Переключить фоновый звук", "sound_title": "Звук",
        "tts_aria": "Слушать трактат вслух", "tts_title": "Слушать",
        "tts_voice_aria": "Голос и скорость чтения", "tts_voice_title": "Голос и скорость",
        "pdf_aria": "Скачать PDF", "pdf_title": "Скачать PDF",
        "dec_aria": "Уменьшить размер текста", "dec_title": "Меньше текста",
        "inc_aria": "Увеличить размер текста", "inc_title": "Больше текста",
        "font_links": "",
        # The bonus story has Russian and English editions.
        "bonus_html": '<p class="footer-bonus"><a href="bird.html">△ Бонус: «Сухая грусть на дне очей»</a></p>',
        "bonus_control_html": (
            '<a id="bonus-link" class="corner-link" href="bird.html" '
            'title="Бонус: «Сухая грусть на дне очей»">✦ Бонус</a>'
        ),
    },
    "en": {
        "readme": ROOT / "README.en.md",
        "out": ROOT / "index.en.html",
        "lang_attr": "en",
        "desc": "Imperial Quadrobic Jainism - a treatise on Svabhava, Hridaya, and the Path of Service.",
        "hero_title": "Imperial<br>Quadrobic<br>Jainism",
        "hero_subtitle": "A treatise on Svabhava, Hridaya, and the Path of Service",
        "scroll_cue": "scroll to enter the riverbed",
        "footer": "Imperial Quadrobic Jainism",
        "nav_aria": "Books of the treatise",
        "sound_aria": "Toggle ambient sound", "sound_title": "Sound",
        "tts_aria": "Listen to the treatise", "tts_title": "Listen",
        "tts_voice_aria": "Voice and reading speed", "tts_voice_title": "Voice & speed",
        "pdf_aria": "Download PDF", "pdf_title": "Download PDF",
        "dec_aria": "Decrease text size", "dec_title": "Smaller text",
        "inc_aria": "Increase text size", "inc_title": "Larger text",
        "font_links": "",
        "bonus_html": '<p class="footer-bonus"><a href="bird.en.html">△ Bonus: “Dry Sorrow in the Depths of the Eyes”</a></p>',
        "bonus_control_html": (
            '<a id="bonus-link" class="corner-link" href="bird.en.html" '
            'title="Bonus: Dry Sorrow in the Depths of the Eyes">✦ Bonus</a>'
        ),
    },
    "th": {
        "readme": ROOT / "README.th.md",
        "out": ROOT / "index.th.html",
        "lang_attr": "th",
        "desc": "ไจนนิยมสี่เท้าแห่งจักรวรรดิ - คัมภีร์ว่าด้วยสวภาวะ หฤทัย และวิถีแห่งการรับใช้",
        "hero_title": "ไจนนิยม<br>สี่เท้า<br>แห่งจักรวรรดิ",
        "hero_subtitle": "คัมภีร์ว่าด้วยสวภาวะ หฤทัย และวิถีแห่งการรับใช้",
        "scroll_cue": "เลื่อนลงเพื่อเข้าสู่สายน้ำ",
        "footer": "ไจนนิยมสี่เท้าแห่งจักรวรรดิ",
        "nav_aria": "บรรดาเล่มของคัมภีร์",
        "sound_aria": "เปิด/ปิดเสียงพื้นหลัง", "sound_title": "เสียง",
        "tts_aria": "ฟังคัมภีร์", "tts_title": "ฟัง",
        "tts_voice_aria": "เลือกเสียงผู้อ่าน", "tts_voice_title": "เสียง",
        "pdf_aria": "ดาวน์โหลด PDF", "pdf_title": "ดาวน์โหลด PDF",
        "dec_aria": "ลดขนาดตัวอักษร", "dec_title": "ตัวอักษรเล็กลง",
        "inc_aria": "เพิ่มขนาดตัวอักษร", "inc_title": "ตัวอักษรใหญ่ขึ้น",
        "font_links": (
            '\n<link href="https://fonts.googleapis.com/css2?'
            'family=Noto+Serif+Thai:ital,wght@0,400;0,500;0,600;0,700;1,500'
            '&display=swap" rel="stylesheet">'
        ),
        "bonus_html": "",
        "bonus_control_html": "",
    },
}


def render_blocks(blocks):
    out = []
    for kind, payload in blocks:
        if kind == "p":
            out.append(f'<p class="reveal">{payload}</p>')
        elif kind == "h4":
            out.append(f'<h4 class="flow-heading reveal">{payload}</h4>')
        elif kind == "ol":
            items = "".join(f'<li class="reveal">{it}</li>' for it in payload)
            out.append(f'<ol class="passage-list">{items}</ol>')
        elif kind == "axiom":
            out.append(f'<li class="axiom reveal"><span class="axiom-glyph">△</span>{payload}</li>')
        elif kind == "invocation":
            out.append(f'<p class="invocation reveal">{payload}</p>')
    return "\n".join(out)


BOOK_MOODS = {
    1: "source",
    2: "flow",
    3: "flow",
    4: "murk",
    5: "flow",
    6: "murk",
    7: "network",
    8: "flow",
    9: "murk",
}


def render_star_blocks(blocks, lang):
    """Stage markers are web presentation; the prose and PDF stay intact."""
    phase_order = ("gather", "collapse", "choice", "after")
    has_headings = any(kind == "h4" for kind, _ in blocks)
    # Older translations have the same scene without the four subheadings.
    anchors = {
        "en": {"But the circle has a center": "collapse",
               "The Death Star is born from the other outcome": "choice",
               "The circle on four supports": "after"},
        "th": {"แต่วงมีศูนย์กลาง": "collapse", "ดาวมรณะเกิดจากทางออกอีกอย่าง": "choice",
               "วงบนสี่ฐาน": "after"},
    }.get(lang, {})
    parts = ['<div class="star-phase" data-star-phase="gather">']
    line = 0
    heading_index = 0
    for kind, payload in blocks:
        phase = None
        if kind == "h4":
            # Renaming a scene heading doesn't change its role in the story.
            phase = phase_order[min(heading_index, len(phase_order) - 1)]
            heading_index += 1
        elif kind == "p" and not has_headings:
            phase = next((value for prefix, value in anchors.items() if payload.startswith(prefix)), None)
        if phase:
            parts.append(f'</div><div class="star-phase" data-star-phase="{phase}">')
        if kind == "p":
            offset = (-5, 3, -2, 5)[line % 4]
            lean = -1 if line % 2 else 1
            parts.append(
                f'<p class="reveal star-line" style="--star-offset:{offset}px;--star-lean:{lean}">'
                f'<span class="star-voice">{payload}</span></p>'
            )
            line += 1
        else:
            parts.append(render_blocks([(kind, payload)]))
    parts.append('</div><div class="star-return-wrap">')
    label = {"ru": "Вернуться", "en": "Return", "th": "กลับ"}[lang]
    parts.append(f'<button class="star-return" type="button">{label}</button></div>')
    return "\n".join(parts)


def render_sections(sections, lang="ru", snapshot=None):
    """Shared by "book" and "practices": a list of .passage articles, each
    with an optional heading (numbered "§N. Title" or, for a titled-but-
    unnumbered subsection, just "Title") and its blocks."""
    sections_html = []
    for sec in sections:
        if sec["num"] is None and sec["title"] is None and not sec["blocks"]:
            continue
        if sec["num"]:
            header = f'<h3 class="reveal"><span class="sec-num">§{sec["num"]}</span> {sec["title"]}</h3>'
        elif sec["title"]:
            header = f'<h3 class="reveal">{sec["title"]}</h3>'
        else:
            header = ""
        id_attr = f' id="p{sec["num"]}"' if sec["num"] else ""
        star = sec["num"] == "38"
        mode_attr = ' data-star-reading="true"' if star else ""
        body = render_star_blocks(sec["blocks"], lang) if star else render_blocks(sec["blocks"])
        note = model_annotations.marker(snapshot, int(sec['num']), lang) if snapshot and sec['num'] and lang in ('ru', 'en') else ''
        note_class = ' model-annotated' if note else ''
        sections_html.append(
            f'<article class="passage{note_class}"{id_attr}{mode_attr}>{header}{note}{body}</article>'
        )
    return "".join(sections_html)


def render_book(book, book_index, lang, snapshot=None):
    if book["kind"] == "book":
        roman = manifesto.book_roman(book, book_index, lang)
        book_title = manifesto.book_name(book, lang)
        mood = BOOK_MOODS.get(book_index, "flow")
        return f"""
<section class="book" id="book-{book_index}" data-book="{book_index}" data-mood="{mood}">
  <div class="book-divider">
    <span class="book-roman">{roman}</span>
    <h2 class="book-title reveal-title">{book_title}</h2>
    <span class="glyph-line" aria-hidden="true">△</span>
  </div>
  <div class="book-body">
    {render_sections(book["sections"], lang, snapshot)}
  </div>
</section>
"""
    elif book["kind"] == "practices":
        book_title = manifesto.book_name(book, lang)
        return f"""
<section class="book practices-book" id="practices" data-mood="still">
  <div class="book-divider">
    <span class="glyph-line" aria-hidden="true">△</span>
    <h2 class="book-title reveal-title">{book_title}</h2>
  </div>
  <div class="book-body">
    {render_sections(book["sections"], lang, snapshot)}
  </div>
</section>
"""
    elif book["kind"] == "axioms":
        # Not a numbered "Книга" (it's a crystallization of the preceding
        # books, not a narrated one) - no roman-numeral badge, same as
        # conclusion/practices.
        book_title = manifesto.book_name(book, lang)
        axioms = []
        for sec in book["sections"]:
            for kind, payload in sec["blocks"]:
                if kind == "axiom":
                    axioms.append(payload)
        items = "".join(
            f'<li class="axiom reveal"><span class="axiom-glyph">△</span>{a}</li>' for a in axioms
        )
        return f"""
<section class="book axioms-book" id="axioms" data-mood="crystal">
  <div class="book-divider">
    <span class="glyph-line" aria-hidden="true">△</span>
    <h2 class="book-title reveal-title">{book_title}</h2>
  </div>
  <ul class="axioms-list">{items}</ul>
</section>
"""
    elif book["kind"] == "conclusion":
        book_title = manifesto.book_name(book, lang)
        blocks = []
        for sec in book["sections"]:
            blocks.append(render_blocks(sec["blocks"]))
        return f"""
<section class="conclusion" id="conclusion" data-mood="calm">
  <div class="book-divider">
    <span class="glyph-line" aria-hidden="true">△</span>
    <h2 class="book-title reveal-title">{book_title}</h2>
  </div>
  <div class="book-body">{''.join(blocks)}</div>
</section>
"""
    return ""


#  kind         id            glyph  (conclusion/practices aren't
#                                      numbered "books", so each gets a
#                                      fixed glyph instead of a roman numeral)
TRAILING_NAV = {
    "conclusion": ("conclusion", "◆"),
    "practices": ("practices", "✦"),
}


def render_nav(doc, lang):
    items = []
    bi = 0
    trailing = {}
    for book in doc["books"]:
        if book["kind"] in TRAILING_NAV:
            trailing[book["kind"]] = manifesto.book_name(book, lang)
            continue
        if book["kind"] != "book":
            continue
        bi += 1
        roman = manifesto.book_roman(book, bi, lang)
        name = manifesto.book_name(book, lang)
        items.append(
            f'<a href="#book-{bi}" class="nav-dot" data-target="book-{bi}" title="{html.escape(name)}">'
            f'<span class="nav-glyph">{roman}</span><span class="nav-label">{html.escape(name)}</span></a>'
        )
    for kind, (target, glyph) in TRAILING_NAV.items():
        title = trailing.get(kind, target)
        items.append(
            f'<a href="#{target}" class="nav-dot" data-target="{target}" title="{html.escape(title)}">'
            f'<span class="nav-glyph">{glyph}</span><span class="nav-label">{html.escape(title)}</span></a>'
        )
    return "\n".join(items)


def build(lang: str, tpl: str, snapshot):
    meta = LANGS[lang]
    doc = manifesto.load(meta["readme"], lang=lang)
    updated = manifesto.format_updated(meta["readme"], lang)

    preamble_html = "\n".join(f'<p class="reveal">{p}</p>' for p in doc["preamble"])

    books_html = []
    bi = 0
    for book in doc["books"]:
        if book["kind"] == "book":
            bi += 1
        books_html.append(render_book(book, bi, lang, snapshot))

    nav_html = render_nav(doc, lang)

    model_ui = model_annotations.reading_ui(snapshot, doc, lang)
    if lang in ('ru', 'en'):
        map_target = ROOT / ('model-map.html' if lang == 'ru' else 'model-map.en.html')
        map_target.write_text(model_annotations.render_map(snapshot, doc, lang), encoding='utf-8')
        print(f'wrote {map_target.name}')
    out = tpl.replace("<!--TITLE-->", html.escape(doc["title"]))
    out = out.replace("<!--PREAMBLE-->", preamble_html)
    out = out.replace("<!--BOOKS-->", "\n".join(books_html))
    out = out.replace("<!--NAV-->", nav_html)
    for key, value in model_ui.items():
        out = out.replace(f'<!--MODEL_{key.upper()}-->', value)
    out = out.replace("<!--GLOSSARY_DATA-->", glossary_json(doc, lang))
    out = out.replace("<!--LANG_ATTR-->", meta["lang_attr"])
    out = out.replace("<!--DESC-->", html.escape(meta["desc"]))
    out = out.replace("<!--HERO_TITLE-->", meta["hero_title"])
    out = out.replace("<!--HERO_SUBTITLE-->", html.escape(meta["hero_subtitle"]))
    out = out.replace("<!--SCROLL_CUE-->", html.escape(meta["scroll_cue"]))
    out = out.replace("<!--FOOTER-->", html.escape(meta["footer"]))
    out = out.replace("<!--UPDATED-->", html.escape(updated))
    out = out.replace("<!--BONUS-->", meta["bonus_html"])
    out = out.replace("<!--BONUS_BADGE-->", meta["bonus_control_html"])
    formal_path = "formalization.html" if lang == "ru" else "formalization.en.html"
    formal_label = {"ru": "Формализация", "en": "Formalization", "th": "Formalization · EN"}[lang]
    out = out.replace("<!--FORMAL_BADGE-->",
                      f'<a id="formalization-link" class="corner-link" href="{formal_path}">⊢ {formal_label}</a>')
    out = out.replace("<!--FORMAL_LINK-->",
                      f'<p class="footer-bonus"><a href="{formal_path}">⊢ {formal_label}</a></p>')
    out = out.replace("<!--NAV_ARIA-->", html.escape(meta["nav_aria"]))
    out = out.replace("<!--SOUND_ARIA-->", html.escape(meta["sound_aria"]))
    out = out.replace("<!--SOUND_TITLE-->", html.escape(meta["sound_title"]))
    out = out.replace("<!--TTS_ARIA-->", html.escape(meta["tts_aria"]))
    out = out.replace("<!--TTS_TITLE-->", html.escape(meta["tts_title"]))
    out = out.replace("<!--TTS_VOICE_ARIA-->", html.escape(meta["tts_voice_aria"]))
    out = out.replace("<!--TTS_VOICE_TITLE-->", html.escape(meta["tts_voice_title"]))
    out = out.replace("<!--PDF_ARIA-->", html.escape(meta["pdf_aria"]))
    out = out.replace("<!--PDF_TITLE-->", html.escape(meta["pdf_title"]))
    out = out.replace("<!--DEC_ARIA-->", html.escape(meta["dec_aria"]))
    out = out.replace("<!--DEC_TITLE-->", html.escape(meta["dec_title"]))
    out = out.replace("<!--INC_ARIA-->", html.escape(meta["inc_aria"]))
    out = out.replace("<!--INC_TITLE-->", html.escape(meta["inc_title"]))
    out = out.replace("<!--FONT_LINKS-->", meta["font_links"])

    meta["out"].write_text(out, encoding="utf-8")
    print(f"wrote {meta['out']} ({len(out)} bytes), {bi} books")


def main():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    snapshot = model_annotations.load_snapshot()
    for lang in LANGS:
        build(lang, tpl, snapshot)


if __name__ == "__main__":
    main()

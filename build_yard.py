#!/usr/bin/env python3
"""Build both editions of the bonus-only story continuation.

yard.md and yard.en.md are an independent story, not an input to the canonical
treatise, translations, PDF or Agda. Artwork and §38 effects share the main reader.
"""
import html
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
import manifesto
import reading_art
from build import render_star_blocks
from build_io import write_text_if_changed


LANGS = {
    'ru': {
        'source': 'yard.md', 'output': 'yard.html', 'treatise': 'index.html',
        'description': 'Михаил, Поликарпыч и птица. Продолжение рассказа «Сухая грусть на дне очей».',
        'kicker': 'После «Сухой грусти на дне очей»',
        'subtitle': 'История Михаила и Поликарпыча.',
        'chapters': 'Главы', 'nav_label': 'Главы рассказа', 'language_label': 'Язык',
        'sound_label': 'Переключить звук', 'sound_title': 'Звук',
        'back_label': 'К трактату ↗', 'answer': 'Да', 'return_label': 'Вернуться',
    },
    'en': {
        'source': 'yard.en.md', 'output': 'yard.en.html', 'treatise': 'index.en.html',
        'description': 'Misha, Polikarpich and the bird. A continuation of Dry Sorrow in the Depths of the Eyes.',
        'kicker': 'After “Dry Sorrow in the Depths of the Eyes”',
        'subtitle': 'The story of Misha and Polikarpich.',
        'chapters': 'Chapters', 'nav_label': 'Story chapters', 'language_label': 'Language',
        'sound_label': 'Toggle sound', 'sound_title': 'Sound',
        'back_label': 'To the treatise ↗', 'answer': 'Yes', 'return_label': 'Return',
    },
}


def blocks(items):
    out = []
    for kind, value in items:
        if kind == 'p':
            out.append(f'<p>{value}</p>')
        elif kind == 'h4':
            out.append(f'<h4>{value}</h4>')
        elif kind == 'ol':
            out.append('<ol>' + ''.join(f'<li>{item}</li>' for item in value) + '</ol>')
        elif kind == 'dt':
            term, definition = value
            if definition:
                out.append(f'<div class="yard-term"><dt>{term}</dt><dd>{definition}</dd></div>')
            else:
                # The shared parser treats dash-led dialogue as a bare list term.
                out.append(f'<p>- {term}</p>')
        elif kind in ('axiom', 'invocation'):
            out.append(f'<p class="yard-axiom">{value}</p>')
        else:
            raise ValueError(f'Unsupported story block: {kind}')
    return '\n'.join(out)


def build(lang, meta):
    doc = manifesto.load(ROOT / meta['source'], lang=lang)
    numbers = lambda d: [s['num'] for b in d['books'] for s in b['sections'] if s['num']]
    navigation, books = [], []
    index = 0
    after_star = False
    for book in doc['books']:
        if book['kind'] == 'book':
            index += 1
            anchor = f'book-{index}'
        else:
            anchor = book['kind']
        if book['kind'] == 'conclusion':
            after_star = True
        sealed = ' data-yard-after-star' if after_star else ''
        title = html.escape(book['title'])
        navigation.append(f'<a href="#{anchor}"{sealed}>{title}</a>')
        sections = []
        for section in book['sections']:
            if not section['blocks'] and not section['title']:
                continue
            number, heading = section['num'], section['title']
            ident = f' id="p{number}"' if number else ''
            label = ''
            header = f'<h3>{label}{html.escape(heading)}</h3>' if heading else ''
            star = number == '38'
            if star:
                # The treatise's scene renderer handles paragraphs, not the
                # dash-led dialogue entries produced by the shared parser.
                scene = [('p', f'- {value[0]}') if kind == 'dt' and not value[1]
                         else (kind, value) for kind, value in section['blocks']]
                body = render_star_blocks(scene, lang).replace(
                    f'>{meta["return_label"]}</button>', f'>{meta["answer"]}</button>')
            else:
                body = blocks(section['blocks'])
            if book['kind'] == 'glossary':
                body = f'<dl>{body}</dl>'
            mode = ' data-star-reading="true"' if star else ''
            sections.append(reading_art.render(number, 'before')
                            + f'<article class="passage"{ident}{mode}>{header}{body}</article>'
                            + reading_art.render(number, 'after'))
        books.append(f'<section class="yard-book" id="{anchor}"{sealed}><h2>{title}</h2>{"".join(sections)}</section>')
    preamble = ''.join(f'<p>{p}</p>' for p in doc['preamble'])
    intro = f'<article class="passage yard-intro" id="intro">{preamble}</article>' if preamble else ''
    values = {'TITLE': html.escape(doc['title']), 'INTRO': intro,
              'NAV': '\n'.join(navigation), 'BOOKS': '\n'.join(books),
              'RETURN_ART': reading_art.render('38', 'return'), 'LANG': lang,
              'LANGUAGES': ''.join(
                  f'<a href="{item["output"]}" lang="{code}" hreflang="{code}"'
                  + (' aria-current="page"' if code == lang else ' data-yard-language')
                  + f'>{code.upper()}</a>' for code, item in LANGS.items())}
    values.update({key.upper(): html.escape(value) for key, value in meta.items()})
    page = (ROOT / 'yard_template.html').read_text()
    for key, value in values.items():
        page = page.replace(f'<!--{key}-->', value)
    if re.search(r'<!--[A-Z_]+-->', page):
        raise ValueError('Unresolved story template token')
    changed = write_text_if_changed(ROOT / meta['output'], page)
    print(f'{"wrote" if changed else "unchanged"} {meta["output"]}; {index} books, {len(numbers(doc))} numbered sections')


if __name__ == '__main__':
    for lang, meta in LANGS.items():
        build(lang, meta)

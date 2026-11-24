#!/usr/bin/env python3
"""Build the unlisted continuation of the bird story. Never add an inbound navigation link.

yard.md is an independent story, not an input to the canonical
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
            raise ValueError(f'Unsupported satire block: {kind}')
    return '\n'.join(out)


def build():
    doc = manifesto.load(ROOT / 'yard.md', lang='ru')
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
            body = render_star_blocks(section['blocks'], 'ru').replace('>Вернуться</button>', '>Нарисовать</button>') if star else blocks(section['blocks'])
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
              'NAV': '\n'.join(navigation), 'BOOKS': '\n'.join(books)}
    page = (ROOT / 'yard_template.html').read_text()
    for key, value in values.items():
        page = page.replace(f'<!--{key}-->', value)
    if re.search(r'<!--[A-Z_]+-->', page):
        raise ValueError('Unresolved satire template token')
    changed = write_text_if_changed(ROOT / 'yard.html', page)
    print(f'{"wrote" if changed else "unchanged"} yard.html; {index} books, {len(numbers(doc))} numbered sections')


if __name__ == '__main__':
    build()

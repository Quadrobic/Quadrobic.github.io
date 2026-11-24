#!/usr/bin/env python3
"""Fast, offline validation of published web assets; never rebuilds or downloads."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from model_annotations import json_script, load_snapshot
from runtime_libraries import offline_scripts, offline_sources

ROOT = Path(__file__).resolve().parent.parent


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.scripts = path, set(), [], []
        self.markers, self.notes_source, self.notes_text = set(), None, ''
        self.in_notes = False
        source = path.read_text(encoding='utf-8')
        if re.search(r'<!--[A-Z_]+-->', source):
            raise ValueError(f'Unresolved template token: {path.name}')
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                raise ValueError(f'Duplicate id in {self.path.name}: {a["id"]}')
            self.ids.add(a['id'])
        self.links.extend(a[k] for k in ('href', 'src', 'data-src') if a.get(k))
        if tag == 'script' and a.get('src'):
            self.scripts.append(a['src'])
        if a.get('data-model-section'):
            self.markers.add(a['data-model-section'])
        if tag == 'script' and a.get('id') == 'model-notes-data':
            self.in_notes = True
            self.notes_source = a.get('data-src')

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_notes = False

    def handle_data(self, data):
        if self.in_notes:
            self.notes_text += data


def check():
    load_snapshot()  # Includes checked Agda source hashes and native anchors.
    lock = json.loads((ROOT / 'android/vendor-lock.json').read_text())
    sources = {item['file']: item['url'] for item in lock['assets']}
    for name, url in offline_sources().items():
        if sources.get(name) != url:
            raise ValueError(f'Runtime/Android dependency mismatch: {name}')
    paths = [ROOT / n for n in ('index.html', 'index.en.html', 'index.th.html',
             'bird.html', 'bird.en.html', 'formalization.html', 'formalization.en.html',
             'model-map.html', 'model-map.en.html', '404.html', 'yard.html')]
    paths += sorted((ROOT / 'formalization/code').glob('*.html'))
    pages = {p: Page(p) for p in paths}
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            decoded = unquote(url.path)
            base = ROOT if decoded.startswith('/') else path.parent
            target = (base / decoded.lstrip('/')).resolve() if decoded else path
            if ROOT not in target.parents or not target.is_file():
                raise ValueError(f'Missing or escaping asset: {path.name}: {link}')
            if target == ROOT / 'yard.html' and path.name not in ('yard.html', 'bird.html', 'bird.en.html'):
                raise ValueError(f'Unlisted satire has an inbound link: {path.name}: {link}')
            if target in pages and url.fragment and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f'Broken anchor: {path.name}: {link}')
        if path.name == 'yard.html' and 'name="robots" content="noindex, nofollow, noarchive"' not in path.read_text():
            raise ValueError('Unlisted satire must retain its noindex metadata')
        if path.name == 'yard.html' and page.scripts != ['js/reader-controls.js', 'js/yard.js', 'js/death-star.js']:
            raise ValueError('Yard reader scripts are missing or out of order')
        if page.notes_text:
            config = json.loads(page.notes_text)
            if 'sections' in config or not page.notes_source:
                raise ValueError(f'Notes must be external and lazy: {path.name}')
            payload_path = ROOT / urlsplit(page.notes_source).path
            source = payload_path.read_text()
            prefix = 'window.iqjModelNotes = '
            if not source.startswith(prefix) or not source.endswith(';\n'):
                raise ValueError(f'Invalid generated notes wrapper: {payload_path.name}')
            payload = json.loads(source[len(prefix):-2])
            version = hashlib.sha256(json_script(payload['sections']).encode()).hexdigest()[:16]
            if payload['version'] != config['version'] or version != config['version']:
                raise ValueError(f'Stale notes payload: {path.name}')
            if set(payload['sections']) != page.markers:
                raise ValueError(f'Notes do not cover all markers: {path.name}')
            if urlsplit(page.notes_source).query != 'v=' + version:
                raise ValueError(f'Notes URL lacks its content version: {path.name}')
        if path.name.startswith(('index', 'bird')):
            actual = [url for url in page.scripts if url.startswith('https://')]
            if actual != list(offline_scripts()):
                raise ValueError(f'Outdated or reordered runtime libraries: {path.name}')
            expected = ['js/main.js', 'js/reader-controls.js', 'js/speech.js']
            if sorted(expected, key=page.scripts.index) != expected:
                raise ValueError(f'Reader scripts in wrong order: {path.name}')
    print(f'PASS: {len(pages)} pages; local assets and anchors, deferred notes snapshots, '
          'reader script order, Agda snapshot integrity.')


if __name__ == '__main__':
    try:
        check()
    except (ValueError, OSError, KeyError) as error:
        sys.exit(str(error))

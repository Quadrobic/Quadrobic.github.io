"""Render claim-level model notes and a graph of actual section cross-references.

Consumes only the annotations snapshot exported after Agda verification. The graph
shows textual references, not logical implication or proof dependencies.
"""
import hashlib
import html
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent


def esc(value):
    return html.escape(str(value), quote=True)


def json_script(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c')


def load_snapshot():
    path = ROOT / 'formalization/annotations.json'
    if not path.exists():
        raise ValueError('Run python3 agda/build_web.py before building model annotations')
    data = json.loads(path.read_text())
    manifest = json.loads((ROOT / 'formalization/verification.json').read_text())
    if data['source_sha256'] != manifest['source_sha256']:
        raise ValueError('Annotations and verification manifest describe different snapshots')
    for name, digest in manifest['files'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Stale model snapshot: {name}; run python3 agda/build_web.py')
    anchors = {}
    for claims in data['claims'].values():
        for claim in claims:
            if not claim.get('source'):
                continue
            name, fragment = claim['source'].split('#', 1)
            if name not in anchors:
                anchors[name] = set(re.findall(r'\bid="([^"]+)"', (ROOT / name).read_text()))
            if fragment not in anchors[name]:
                raise ValueError(f'Annotation links to a missing native Agda anchor: {claim["source"]}')
    return data


UI = {
 'ru': {
    'map': 'Карта связей', 'status': 'Связь с моделью', 'close': 'Закрыть',
    'scope': 'Статусы относятся к утверждениям, не к параграфу целиком.',
    'entry': 'У текста есть проверяемый слой. Метки на полях показывают его границы.',
    'code': 'Проверенный фрагмент Agda', 'source': 'Определение в коде', 'more': 'Пояснение модели',
    'nocode': 'Для этого утверждения нет фрагмента Agda.',
    'uncovered': 'Утверждения этого параграфа пока не представлены отдельными определениями или теоремами. Это не означает ни их доказанности, ни намеренного запрета формализации.',
    'uncovered_title': 'Пока за пределами покрытия',
    'title': 'Связи, не тождества.', 'eyebrow': 'КАРТА ТЕКСТА / AGDA',
    'intro': '38 параграфов. Рёбра — явные ссылки §N в тексте, а не логическое следование. Выберите узел: рядом появятся точные утверждения и их статус.',
    'legend': 'Цвет каждого сегмента — статус отдельного утверждения. У одного параграфа их бывает несколько.',
    'out': 'Ссылается на', 'in': 'На него ссылаются', 'none': 'Нет ссылок',
    'read': 'Читать параграф', 'back': 'Трактат', 'formal': 'Формализация',
    'edges': 'ссылок', 'nodes': 'параграфов', 'list': 'Все параграфы',
    'graph': 'Граф перекрёстных ссылок. Выберите параграф или используйте список ниже.',
    'verified': 'Снимок проверенной модели', 'arrow': 'направление ссылки',
 },
 'en': {
    'map': 'Map of connections', 'status': 'Connection to the model', 'close': 'Close',
    'scope': 'Statuses describe individual claims, not the entire section.',
    'entry': 'The text has a checkable layer. Margin markers show its boundaries.',
    'code': 'Checked Agda excerpt', 'source': 'Definition in the code', 'more': 'Model explanation',
    'nocode': 'There is no Agda excerpt for this claim.',
    'uncovered': 'This section’s claims do not yet have dedicated definitions or theorems. This implies neither proof nor a deliberate exclusion from formalization.',
    'uncovered_title': 'Not yet covered',
    'title': 'Connections, not identities.', 'eyebrow': 'TEXT MAP / AGDA',
    'intro': '38 sections. Edges are explicit §N cross-references in the text, not logical implications. Select a node to see the precise claims and their status alongside it.',
    'legend': 'Each colored segment marks one claim status. A section may have several.',
    'out': 'Refers to', 'in': 'Referred to by', 'none': 'No references',
    'read': 'Read this section', 'back': 'Treatise', 'formal': 'Formalization',
    'edges': 'references', 'nodes': 'sections', 'list': 'All sections',
    'graph': 'Graph of textual cross-references. Select a section or use the list below.',
    'verified': 'Verified model snapshot', 'arrow': 'reference direction',
 },
}


def section_claims(snapshot, number, lang):
    return snapshot['claims'].get(str(number), [{
        'status': 'uncovered', lang: [UI[lang]['uncovered_title'], UI[lang]['uncovered']],
        'stage': None,
    }])


def status_names(snapshot, claims, lang):
    return list(dict.fromkeys(snapshot['statuses'][c['status']][1 if lang == 'ru' else 2] for c in claims))


def badges(snapshot, claims, lang):
    return ''.join(f'<span class="model-status" data-status="{status}"><b aria-hidden="true">{esc(snapshot["statuses"][status][0])}</b>{esc(snapshot["statuses"][status][1 if lang == "ru" else 2])}</span>'
                   for status in dict.fromkeys(c['status'] for c in claims))


def cards(snapshot, claims, lang):
    ui = UI[lang]
    formal = 'formalization.html' if lang == 'ru' else 'formalization.en.html'
    result = []
    for c in claims:
        title, text = c[lang]
        code = f'<details class="model-code"><summary>{ui["code"]}</summary><pre class="Agda" tabindex="0">{c["snippet"]}</pre></details>' if c.get('snippet') else f'<div class="model-no-code">{ui["nocode"]}</div>'
        links = f'<a href="{esc(c["source"])}">{ui["source"]} ↗</a>' if c.get('source') else ''
        if c.get('stage'):
            links += f'<a href="{formal}#{esc(c["stage"])}">{ui["more"]} ↗</a>'
        result.append(f'<section class="model-claim" data-status="{c["status"]}">{badges(snapshot, [c], lang)}<h4>{esc(title)}</h4><div class="model-claim-text">{esc(text)}</div>{code}<div class="model-claim-links">{links}</div></section>')
    return ''.join(result)


def marker(snapshot, number, lang):
    if lang not in UI:
        return ''
    claims = section_claims(snapshot, number, lang)
    statuses = list(dict.fromkeys(c['status'] for c in claims))
    label = f'{UI[lang]["status"]}, §{number}: ' + ', '.join(status_names(snapshot, claims, lang))
    dots = ''.join(f'<i data-status="{s}"></i>' for s in statuses)
    return f'<button class="model-marker" type="button" data-model-section="{number}" aria-label="{esc(label)}" aria-controls="model-panel" aria-expanded="false"><span class="model-hex" aria-hidden="true">{esc(snapshot["statuses"][statuses[0]][0])}</span><span class="model-dots" aria-hidden="true">{dots}</span></button><div class="model-note-slot" id="model-slot-{number}"></div>'


def entries(doc):
    result = []
    for book in doc['books']:
        if book['kind'] != 'book':
            continue
        for sec in book['sections']:
            if not sec['num']:
                continue
            chunks = [str(payload) for _, payload in sec['blocks']]
            refs = sorted({int(n) for n in re.findall(r'§(\d+)', ' '.join(chunks)) if int(n) != int(sec['num'])})
            result.append({'number': int(sec['num']), 'title': html.unescape(re.sub('<[^>]+>', '', sec['title'])), 'refs': refs})
    valid = {s['number'] for s in result}
    for sec in result:
        sec['refs'] = [n for n in sec['refs'] if n in valid]
    return result


def reading_ui(snapshot, doc, lang):
    if lang not in UI:
        return {'head': '', 'entry': '', 'tail': ''}
    ui = UI[lang]
    map_path = 'model-map.html' if lang == 'ru' else 'model-map.en.html'
    sections = {}
    actual = entries(doc)
    if set(snapshot['claims']) - {str(sec['number']) for sec in actual}:
        raise ValueError('Model annotations refer to missing treatise sections')
    for sec in actual:
        claims = section_claims(snapshot, sec['number'], lang)
        sections[str(sec['number'])] = {
            'title': f'§{sec["number"]}. {sec["title"]}',
            'html': cards(snapshot, claims, lang),
        }
    data = {'sections': sections, 'ui': ui, 'map': map_path}
    entry = f'<aside class="model-entry"><span class="model-entry-signal" aria-hidden="true">⊢</span><div>{ui["entry"]}<small>{ui["scope"]}</small></div><a href="{map_path}">{ui["map"]} ↗</a></aside>'
    panel = f'<aside id="model-panel" class="model-panel" data-model-panel data-lenis-prevent hidden aria-labelledby="model-panel-title"><header><span class="model-panel-label">{ui["status"]}</span><button type="button" data-model-close aria-label="{ui["close"]}">×</button></header><h3 id="model-panel-title"></h3><div class="model-panel-scope">{ui["scope"]}</div><div class="model-panel-content"></div><footer><a href="{map_path}" data-model-map>{ui["map"]} ↗</a></footer></aside>'
    tail = panel + f'<script type="application/json" id="model-notes-data">{json_script(data)}</script><script src="js/model-notes.js"></script>'
    return {'head': '\n<link rel="stylesheet" href="css/model-notes.css"><noscript><style>.model-marker { display: none; }</style></noscript>', 'entry': '  ' + entry + '\n\n', 'tail': '\n' + tail}


def graph_svg(sections, snapshot, lang):
    ui = UI[lang]
    positions = {}
    for i, sec in enumerate(sections):
        angle = -math.pi / 2 + i * 2 * math.pi / len(sections)
        positions[sec['number']] = (450 + 357 * math.cos(angle), 410 + 345 * math.sin(angle))
    edges = []
    for sec in sections:
        x, y = positions[sec['number']]
        for ref in sec['refs']:
            tx, ty = positions[ref]
            # A mild inward bend keeps directionality visible at the endpoints.
            cx, cy = (x + tx + 450) / 3, (y + ty + 410) / 3
            # Stop outside the target ring so the arrowhead remains visible.
            length = math.hypot(tx - cx, ty - cy)
            ex, ey = tx - 25 * (tx - cx) / length, ty - 25 * (ty - cy) / length
            edges.append(f'<path data-from="{sec["number"]}" data-to="{ref}" d="M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}" marker-end="url(#reference-arrow)"/>')
    nodes = []
    for sec in sections:
        n = sec['number']; x, y = positions[n]
        statuses = list(dict.fromkeys(c['status'] for c in section_claims(snapshot, n, lang)))
        circumference = 2 * math.pi * 23
        rings = ''.join(f'<circle class="map-status-ring" data-status="{status}" r="23" stroke-dasharray="{circumference / len(statuses) - 2:.2f} {circumference:.2f}" stroke-dashoffset="{-i * circumference / len(statuses):.2f}" transform="rotate(-90)"/>' for i, status in enumerate(statuses))
        label = f'§{n}. {sec["title"]}. ' + ', '.join(status_names(snapshot, section_claims(snapshot, n, lang), lang))
        nodes.append(f'<a href="#map-p{n}" data-map-node="{n}" aria-label="{esc(label)}" transform="translate({x:.1f},{y:.1f})"><title>{esc(label)}</title><circle class="map-node-base" r="21"/>{rings}<text text-anchor="middle" dy=".36em">{n}</text></a>')
    return f'''<svg class="model-graph" viewBox="0 0 900 820" role="group" aria-label="{esc(ui['graph'])}">
<defs><marker id="reference-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z"/></marker></defs>
<g class="map-grid" aria-hidden="true"><circle cx="450" cy="410" r="300"/><circle cx="450" cy="410" r="200"/><circle cx="450" cy="410" r="90"/><path d="M450 30V790M45 410H855"/></g>
<g class="map-edges">{''.join(edges)}</g><g class="map-nodes">{''.join(nodes)}</g></svg>'''


def render_map(snapshot, doc, lang):
    ui = UI[lang]; sections = entries(doc)
    index = 'index.html' if lang == 'ru' else 'index.en.html'
    formal = 'formalization.html' if lang == 'ru' else 'formalization.en.html'
    legend = ''.join(f'<span class="model-status" data-status="{s}"><b aria-hidden="true">{esc(d[0])}</b>{esc(d[1 if lang == "ru" else 2])}</span>' for s, d in snapshot['statuses'].items())
    details, navigation = [], []
    for sec in sections:
        n = sec['number']; claims = section_claims(snapshot, n, lang)
        incoming = [s['number'] for s in sections if n in s['refs']]
        def refs(nums):
            return ' '.join(f'<a href="#map-p{v}" data-map-select="{v}">§{v}</a>' for v in nums) or ui['none']
        details.append(f'<section class="map-detail" id="map-p{n}" data-map-detail="{n}"><div class="map-detail-number">§{n:02d}</div><h2 tabindex="-1">{esc(sec["title"])}</h2><a class="map-read" href="{index}#p{n}">{ui["read"]} ↗</a><div class="map-references"><div><b>{ui["out"]}</b>{refs(sec["refs"])}</div><div><b>{ui["in"]}</b>{refs(incoming)}</div></div>{cards(snapshot, claims, lang)}</section>')
        navigation.append(f'<a href="#map-p{n}" data-map-select="{n}"><span>§{n:02d}</span>{esc(sec["title"])}</a>')
    edges = sum(len(s['refs']) for s in sections)
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{ui['map']} · Agda</title><link rel="icon" href="logo/favicon.svg"><link rel="stylesheet" href="css/style.css"><link rel="stylesheet" href="css/model-notes.css"><link rel="stylesheet" href="css/model-map.css"></head>
<body class="model-map-page"><header class="map-nav"><a href="{index}">△ {ui['back']}</a><a href="{formal}">⊢ {ui['formal']}</a><nav aria-label="Language"><a href="model-map.html" lang="ru" data-map-lang="ru" {'aria-current="page"' if lang == 'ru' else ''}>RU</a><a href="model-map.en.html" lang="en" data-map-lang="en" {'aria-current="page"' if lang == 'en' else ''}>EN</a></nav></header>
<main class="model-map-main"><div class="map-warning"><span>{ui['eyebrow']}</span><span>{len(sections)} {ui['nodes']} / {edges} {ui['edges']}</span></div><h1>{ui['title']}</h1><p class="map-intro">{ui['intro']}</p><div class="map-legend">{legend}</div><p class="map-scope">{ui['legend']} {ui['scope']}</p>
<div class="map-workspace"><div class="map-circuit">{graph_svg(sections, snapshot, lang)}<div class="map-circuit-caption"><span>§ → §</span> {ui['arrow']}</div></div><aside class="map-inspector" aria-label="{ui['status']}">{''.join(details)}</aside></div>
<details class="map-directory" open><summary>{ui['list']}</summary><nav>{''.join(navigation)}</nav></details><footer class="map-snapshot">{ui['verified']} · {esc(snapshot['agda'])} · <a href="formalization/verification.json">SHA-256 {snapshot['source_sha256'][:16]}</a></footer></main><script src="js/model-map.js"></script></body></html>'''

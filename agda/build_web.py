#!/usr/bin/env python3
"""Verify, export genuine Agda highlighting, then build the public reading pages."""
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

from web_content import REJECTIONS, STAGES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PUBLIC = ROOT / "formalization"
RAW = HERE / "_build/html"
MODULES = {"All": HERE / "All.agda"} | {
    f"Imperium.{p.stem}": p for p in sorted((HERE / "Imperium").glob("*.agda"))
}
PRE = re.compile(r'<pre class="Agda">(.*?)</pre>', re.S)
TOKEN = re.compile(r'<a\b[^>]*>.*?</a>|[^<]+', re.S)
LINK = re.compile(r'\s+href="([^"]*)"')
ID = re.compile(r'\s+id="[^"]*"')


def escape(value):
    return html.escape(str(value), quote=True)


def pre_text(markup):
    return html.unescape(re.sub(r'<[^>]+>', '', markup))


def links(markup, prefix="", strip_ids=False):
    def rewrite(tag):
        def target(match):
            href = html.unescape(match.group(1))
            module = href.split('#', 1)[0].removesuffix('.html')
            if module in MODULES:
                return f' href="{escape(prefix + href)}"'
            # Do not publish a copy of the entire standard library, or leave
            # broken links to it. Its semantic token classes remain intact.
            return f' title="{escape(module)}"'
        tag = LINK.sub(target, tag.group(0))
        return ID.sub('', tag) if strip_ids else tag
    return re.sub(r'<a\b[^>]*>', rewrite, markup)


def excerpt(module, start, end, raw):
    source = MODULES[module].read_text(encoding="utf-8")
    begin = source.index(start)
    finish = source.index(end, begin + len(start)) if end else len(source)
    fragments, offset = [], 0
    for token in TOKEN.findall(raw):
        text = pre_text(token)
        stop = offset + len(text)
        if text and stop > begin and offset < finish:
            left, right = max(0, begin - offset), min(len(text), finish - offset)
            content = html.escape(text[left:right], quote=False)
            if token.startswith('<a'):
                opening = token[:token.index('>') + 1]
                content = opening + content + '</a>'
            fragments.append(content)
        offset = stop
    fragment = ''.join(fragments)
    if pre_text(fragment) != source[begin:finish]:
        raise ValueError(f"Agda highlight/source mismatch: {module}: {start}")
    return links(fragment.rstrip(), "formalization/code/", strip_ids=True)


def code_panel(module, start, end, folded, raw, lang):
    module = f"Imperium.{module}"
    code = excerpt(module, start, end, raw[module])
    full = "Весь модуль" if lang == "ru" else "Full module"
    copy = "Копировать" if lang == "ru" else "Copy"
    label = "Развернуть проверенный код" if lang == "ru" else "Expand checked code"
    line = MODULES[module].read_text().index(start) + 1
    panel = f'''<figure class="code-panel">
<figcaption><span>{escape(module)}</span><span class="code-actions">
<a href="formalization/code/{module}.html#{line}">{full} ↗</a>
<button type="button" data-copy>{copy}</button></span></figcaption>
<pre class="Agda" tabindex="0" aria-label="Agda · {escape(module)}">{code}</pre></figure>'''
    return f'<details class="proof-details"><summary>{label}</summary>{panel}</details>' if folded else panel


def flow(lang):
    if lang == 'ru':
        return '''<div class="proof-flow" aria-label="Два общих исхода">
<div class="flow-origin">Край обрушения <span>личные выборы и вклады → общий ответ круга</span></div>
<div class="flow-branches"><div class="flow-return"><code>explosion</code><strong>Взрыв для всех</strong><p>Действенная Шакти одной Дживы способна освободить всех оставшихся.</p></div>
<div class="flow-capture"><code>enclosure</code><strong>Заточение всего круга</strong><p>Кашая одной способна закрыть выход всем, не только ей самой.</p></div></div>
<p class="flow-note">Кто стал катализатором, задаёт отдельный контракт. Общие последствия не отнимают у Джив собственного выбора. Единодушие не требуется.</p></div>'''
    return '''<div class="proof-flow" aria-label="Two shared outcomes">
<div class="flow-origin">The brink of collapse <span>individual choices and contributions → the circle’s shared response</span></div>
<div class="flow-branches"><div class="flow-return"><code>explosion</code><strong>An explosion for everyone</strong><p>One jiva’s effective Shakti can free everyone still participating.</p></div>
<div class="flow-capture"><code>enclosure</code><strong>Captivity of the whole circle</strong><p>One jiva’s grasping-force can close every exit, not just their own.</p></div></div>
<p class="flow-note">A separate contract identifies the effective catalyst. Shared consequences do not take away each jiva’s own choice. Unanimity is not required.</p></div>'''


def render(lang, raw, version, manifest):
    ru = lang == 'ru'
    title = "Формализация" if ru else "Formalization"
    treatise = "index.html" if ru else "index.en.html"
    story = "bird.html" if ru else "bird.en.html"
    result_title = "Проверить ещё раз" if ru else "Verify it again"
    stages, nav = [], []
    for stage in STAGES:
        heading, tag, body, limit = stage[lang]
        nav.append(f'<a href="#{stage["id"]}"><span>{stage["roman"]}</span>{heading}</a>')
        blocks = ''.join(code_panel(*block, raw, lang) for block in stage['blocks'])
        stages.append(f'''<section class="proof-stage" id="{stage['id']}">
<div class="stage-meta"><span>{stage['roman']}</span><span>{stage['refs']}</span><span>{tag}</span></div>
<h2>{heading}</h2><p class="stage-lead">{body}</p>
{flow(lang) if stage['id'] == 'death-star' else ''}{blocks}
<aside class="model-assumption"><span>{'Граница утверждения' if ru else 'Scope of the claim'}</span><p>{limit}</p></aside>
</section>''')
    nav.append(f'<a href="#verify"><span>VIII</span>{result_title}</a>')
    names = sorted(REJECTIONS)
    rows = ''.join(f'''<li><span class="test-check" aria-hidden="true">✓</span>
<div><span>{REJECTIONS[name][0 if ru else 1]}</span><a href="agda/tests/reject/{name}.agda">{name}.agda ↗</a></div>
<span class="test-outcome">{'отвергнуто' if ru else 'rejected'}</span></li>''' for name in names)
    module_list = ''.join(f'<a href="formalization/code/{name}.html">{name}</a>' for name in MODULES)
    verify = f'''<section class="proof-stage" id="verify"><div class="stage-meta"><span>VIII</span><span>{'Воспроизводимость' if ru else 'Reproducibility'}</span></div>
<h2>{result_title}</h2><p class="stage-lead">{('Проверка принимает корректные модули и обязана отвергнуть намеренно неверные утверждения. Здесь показан результат сборки именно этих исходников.' if ru else 'The check accepts the correct modules and must reject deliberately false claims. This is the build result for these exact sources.')}</p>
<div class="verification-summary"><span class="verified-dot" aria-hidden="true"></span><strong>{escape(version)}</strong><span>--safe --without-K</span><span>{len(names)} {'ожидаемых отказов' if ru else 'expected rejections'}</span></div>
<details class="proof-details rejection-details"><summary>{'Какие утверждения отвергнуты' if ru else 'Which claims were rejected'}</summary><ul class="rejection-list">{rows}</ul></details>
<figure class="code-panel command-panel"><figcaption><span>{'Из корня репозитория' if ru else 'From the repository root'}</span><button type="button" data-copy>{'Копировать' if ru else 'Copy'}</button></figcaption><pre tabindex="0">python3 agda/check.py</pre></figure>
<p>{('Нужны Agda и её standard library. Все модули, отрицательные проверки и инструменты остаются в каталоге agda/.' if ru else 'Requires Agda and its standard library. All modules, negative tests, and verification tools remain in agda/.')}</p>
<div class="proof-downloads"><a href="formalization/imperium-source.zip" download>{'Скачать исходники и проверки' if ru else 'Download sources and checks'} ↓</a><a href="formalization/verification.json">{'Манифест проверки' if ru else 'Verification manifest'} ↗</a></div>
<div class="source-index"><h3>{'Все подсвеченные модули' if ru else 'All highlighted modules'}</h3>{module_list}</div>
<p class="snapshot-note">SHA-256 · <code>{manifest['source_sha256'][:20]}</code> · {'Подсветка сгенерирована Agda; ссылки в коде ведут к определениям модулей модели.' if ru else 'Highlighting is generated by Agda; links in the code lead to definitions in the model’s modules.'}</p></section>'''
    context = {
        'LANG': lang, 'TITLE': title,
        'DESC': 'Проверяемая структура трактата: контракты, доказательства и границы формальной модели на Agda.' if ru else 'The treatise’s checkable structure: contracts, proofs, and limits of the formal Agda model.',
        'TREATISE': treatise, 'STORY': story,
        'BACK': 'Трактат' if ru else 'Treatise', 'BONUS': 'Бонус' if ru else 'Bonus',
        'EYEBROW': 'На границе слова и доказательства' if ru else 'At the boundary of word and proof',
        'HERO_TITLE': 'То, что можно<br>проверить.' if ru else 'What can<br>be checked.',
        'INTRO': 'У трактата есть проверяемая структура. Здесь она записана на Agda: от конечного прошлого до выбора на краю Звезды Смерти. По этапам — определения, доказательства и то, чего они не утверждают.' if ru else 'The treatise has a checkable structure. Here it is written in Agda: from a finite past to the choice at the brink of the Death Star. Step by step: definitions, proofs, and what they do not claim.',
        'BOUNDARY': 'Исток здесь не становится типом, голос Хридаи не превращается в данные, а опыт Звезды Смерти — в алгоритм. Формализуется структура, а не откровение.' if ru else 'The Source does not become a type here. Hridaya’s voice does not become data. The Death Star’s experience does not become an algorithm. What is formalized is structure, not revelation.',
        'VERSION': escape(version), 'MODULE_COUNT': str(len(MODULES) - 1),
        'MODULE_LABEL': 'модулей модели' if ru else 'model modules',
        'TEST_COUNT': str(len(names)), 'TEST_LABEL': 'отрицательных проверок' if ru else 'negative checks',
        'CONTENTS': 'Этапы формализации' if ru else 'Stages of formalization',
        'NAV': ''.join(nav), 'STAGES': ''.join(stages) + verify,
        'COPY_DONE': 'Скопировано' if ru else 'Copied',
        'COPY_SELECT': 'Код выделен' if ru else 'Code selected',
        'FOOTER': 'Модель открыта для продолжения. Каждое новое утверждение должно назвать свои предпосылки и предъявить доказательство.' if ru else 'The model remains open to further work. Every new claim must state its premises and supply its proof.',
    }
    output = (HERE / 'web_template.html').read_text()
    for key, value in context.items():
        output = output.replace(f'<!--{key}-->', value)
    if re.search(r'<!--[A-Z_]+-->', output):
        raise ValueError('Unresolved page placeholder')
    return output


def source_files():
    return sorted(p for p in HERE.rglob('*') if p.is_file()
                  and not any(part in {'_build', '__pycache__'} for part in p.relative_to(HERE).parts)
                  and p.suffix not in {'.agdai', '.pyc'})


def main():
    print('Verifying the formalization before publishing highlighted code...', flush=True)
    result = subprocess.run([sys.executable, str(HERE / 'check.py')], cwd=ROOT,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout, end='', flush=True)
    result.check_returncode()
    for name in REJECTIONS:
        if f'PASS: rejected {name}\n' not in result.stdout:
            raise RuntimeError(f'Missing verified rejection: {name}')
    version = next(line for line in result.stdout.splitlines() if line.startswith('Agda version '))
    agda = shutil.which('agda')
    subprocess.run([agda, '--no-libraries', '--safe', '--without-K', '-Werror',
                    '-WnoUnsupportedIndexedMatch', '-i', str(HERE), '-i', str(HERE / '_build/stdlib'),
                    '--html', '--highlight-occurrences', f'--html-dir={RAW}', str(HERE / 'All.agda')],
                   cwd=ROOT, check=True)
    raw = {}
    for module, path in MODULES.items():
        raw[module] = PRE.search((RAW / f'{module}.html').read_text()).group(1)
        if pre_text(raw[module]) != path.read_text():
            raise ValueError(f'Agda output differs from source: {module}')
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files()}
    manifest = {
        'agda': version, 'flags': ['--safe', '--without-K'],
        'model_modules': sorted(set(MODULES) - {'All'}),
        'accepted_entrypoint': 'agda/All.agda', 'rejected_tests': sorted(REJECTIONS),
        'files': hashes,
        'source_sha256': hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
    }
    # Build all narrative excerpts before replacing any published page.
    pages = {lang: render(lang, raw, version, manifest) for lang in ('ru', 'en')}
    code_dir = PUBLIC / 'code'
    code_dir.mkdir(parents=True, exist_ok=True)
    for module in MODULES:
        body = links(raw[module])
        source = str(MODULES[module].relative_to(ROOT))
        page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{module} · Agda</title><link rel="icon" href="../../logo/favicon.svg"><link rel="stylesheet" href="../../css/style.css"><link rel="stylesheet" href="../../css/formalization.css"></head>
<body class="proof-source-page"><header class="source-header"><a href="../../formalization.html">⊢ Формализация</a><a href="../../formalization.en.html">Formalization · EN</a><strong>{module}</strong><a href="../../{source}" download>Исходник / Source ↓</a></header>
<main class="source-document"><pre class="Agda" tabindex="0" aria-label="Agda · {module}">{body}</pre></main><script src="../../js/formalization.js"></script></body></html>'''
        (code_dir / f'{module}.html').write_text(page, encoding='utf-8')
    with zipfile.ZipFile(PUBLIC / 'imperium-source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in source_files():
            info = zipfile.ZipInfo(str(p.relative_to(ROOT)))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, p.read_bytes())
    (PUBLIC / 'verification.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for lang, body in pages.items():
        target = ROOT / ('formalization.html' if lang == 'ru' else 'formalization.en.html')
        target.write_text(body, encoding='utf-8')
        print(f'wrote {target.name}')
    print(f'Exported {len(MODULES)} linked Agda modules and the source archive.')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Explicit offline Android snapshot/build; never invoked by the site's rebuild."""
import argparse
import fcntl
from datetime import datetime, timezone
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import posixpath
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
API = 35
MIN_API = 26
PACKAGE = 'org.quadrobic.iqj'
sys.path.insert(0, str(ROOT / 'tools'))
from runtime_libraries import VERSIONS, offline_resources

RUNTIME_URLS = offline_resources()

PUBLIC_FILES = ('index.html', 'index.en.html', 'index.th.html', 'bird.html', 'bird.en.html',
                'formalization.html', 'formalization.en.html', 'model-map.html', 'model-map.en.html')
INPUT_FILES = ('README.md', 'README.en.md', 'README.th.md', 'bird.md', 'bird.en.md',
               'build.py', 'build_bird.py', 'template.html', 'bird_template.html')
PUBLIC_DIRS = ('css', 'js', 'audio', 'logo', 'formalization')
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
       "style-src 'self' 'unsafe-inline'; font-src 'self' data:; img-src 'self' data: blob:; "
       "media-src 'self' blob:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-src 'none'")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def outside(path, name):
    path = path.expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError(f'{name} must be outside the repository: {path}')
    return path


def run(args, cwd=None, env=None):
    print('→', Path(str(args[0])).name, flush=True)
    subprocess.run([str(a) for a in args], cwd=cwd, env=env, check=True)


def sdk_tools(sdk):
    platforms = sorted((p for p in (sdk / 'platforms').glob('android-*')
                        if re.fullmatch(r'android-\d+', p.name) and int(p.name[8:]) >= API
                        and (p / 'android.jar').is_file()), key=lambda p: int(p.name[8:]))
    builds = sorted((p for p in (sdk / 'build-tools').glob('*')
                     if re.fullmatch(r'\d+\.\d+\.\d+', p.name) and int(p.name.split('.')[0]) >= 35),
                    key=lambda p: tuple(map(int, p.name.split('.'))))
    tools = {}
    missing = []
    for name in ('java', 'javac', 'keytool'):
        found = shutil.which(name)
        if found: tools[name] = Path(found)
        else: missing.append(name)
    if platforms: tools['android.jar'] = platforms[-1] / 'android.jar'
    else: missing.append(f'platforms;android-{API} (android.jar)')
    usable = next((p for p in reversed(builds)
                   if all((p / t).is_file() for t in ('aapt2', 'd8', 'zipalign', 'apksigner'))), None)
    if usable:
        tools.update({name: usable / name for name in ('aapt2', 'd8', 'zipalign', 'apksigner')})
    else: missing.append('build-tools;35.0.0 (aapt2, d8, zipalign, apksigner)')
    if missing:
        manager = sdk / 'cmdline-tools/latest/bin/sdkmanager'
        print('Missing tools:\n  ' + '\n  '.join(missing), file=sys.stderr)
        print(f'Install SDK packages separately:\n  {manager} --sdk_root={sdk} '
              f'"platforms;android-{API}" "build-tools;35.0.0"', file=sys.stderr)
        return None
    return tools


def vendor(cache, offline):
    lock = json.loads((HERE / 'vendor-lock.json').read_text())
    for item in lock['assets']:
        name = Path(item['file'])
        if name.is_absolute() or '..' in name.parts:
            raise ValueError(f'Unsafe vendor path: {name}')
        target = cache / name
        if target.is_file() and sha(target) == item['sha256']:
            continue
        if offline:
            raise ValueError(f'Missing or changed cached dependency: {name}; run once without --offline')
        if not item['url'].startswith('https://'):
            raise ValueError('Vendor downloads must use HTTPS')
        print('Fetching', name, flush=True)
        request = urllib.request.Request(item['url'], headers={'User-Agent': 'IQJ-offline-builder/1'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read(20_000_001)
        if len(data) > 20_000_000 or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f'Dependency checksum mismatch: {name}; no files were accepted')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return lock['assets']


def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def source_snapshot(work):
    """Render current Markdown in isolation, without modifying published pages."""
    manifest = json.loads((ROOT / 'formalization/verification.json').read_text())
    for name, digest in manifest['files'].items():
        source = (ROOT / name).resolve()
        if ROOT not in source.parents or not source.is_file() or sha(source) != digest:
            raise ValueError(f'Stale Agda publication: {name}; run python3 agda/build_web.py first')
        copy_file(source, work / name)
    for name in INPUT_FILES:
        copy_file(ROOT / name, work / name)
    for name in PUBLIC_FILES:
        copy_file(ROOT / name, work / name)
    for name in PUBLIC_DIRS:
        shutil.copytree(ROOT / name, work / name)
    shutil.copytree(ROOT / 'tools', work / 'tools', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    run([sys.executable, work / 'build.py'], cwd=work)
    run([sys.executable, work / 'build_bird.py'], cwd=work)
    return manifest


def about_page(lang, version):
    strings = {
        'ru': ('О приложении', 'Чтение без интернета', 'Трактат, бонус, словарь и формализация находятся внутри приложения. '
               'Внешние источники открываются в браузере. Место чтения и выбранный язык сохраняются на устройстве. '
               'При наличии интернета приложение проверяет новые версии на GitHub; скачивание предлагается отдельно.',
               'Трактат', 'Бонус', 'Формализация', 'Библиотеки и лицензии'),
        'en': ('About this app', 'Reading offline', 'The treatise, bonus, glossary, and formalization are included in the app. '
               'External sources open in your browser. Reading position and language are kept on this device. '
               'When online, the app checks GitHub for new versions and asks before opening a download.',
               'Treatise', 'Bonus', 'Formalization', 'Libraries and licenses'),
        'th': ('เกี่ยวกับแอป', 'อ่านโดยไม่ใช้อินเทอร์เน็ต', 'คัมภีร์ เรื่องเสริม อภิธานศัพท์ และแบบจำลองรวมอยู่ในแอป '
               'แหล่งข้อมูลภายนอกเปิดในเบราว์เซอร์ ตำแหน่งอ่านและภาษาจะเก็บไว้ในอุปกรณ์นี้ '
               'เมื่อเชื่อมต่ออินเทอร์เน็ต แอปจะตรวจสอบเวอร์ชันใหม่บน GitHub และถามก่อนเปิดการดาวน์โหลด',
               'คัมภีร์', 'เรื่องเสริม', 'แบบจำลอง', 'ไลบรารีและใบอนุญาต'),
    }
    title, heading, body, treatise, bonus, formal, licenses = strings[lang]
    suffix = '.en' if lang == 'en' else '.th' if lang == 'th' else ''
    other = '.en' if lang in ('en', 'th') else ''
    license_links = ''.join(f'<li><a href="licenses/{name}">{label}</a></li>' for name, label in (
        ('p5.txt', f'p5.js {VERSIONS["p5"]} · LGPL-2.1'), ('GSAP.txt', f'GSAP {VERSIONS["gsap"]} · upstream notice'),
        ('GSAP-license.html.txt', 'GSAP · Standard License'), ('Lenis.txt', f'Lenis {VERSIONS["lenis"]} · MIT'),
        ('CormorantGaramond.txt', 'Cormorant Garamond · OFL'), ('EBGaramond.txt', 'EB Garamond · OFL'),
        ('NotoSerifThai.txt', 'Noto Serif Thai · OFL')))
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="../css/style.css"><style>main{{max-width:680px;margin:3rem auto;padding:24px;color:#e7dfd0;font:18px/1.8 var(--serif-body)}}a{{color:#d4b17a}}nav{{display:flex;gap:20px;flex-wrap:wrap}}h1{{font-size:32px}}small{{opacity:.7}}</style></head>
<body><main><h1>{heading}</h1><p>{body}</p><small>Quadrobic · {html.escape(version)}</small>
<nav><a href="../index{suffix}.html">{treatise}</a><a href="../bird{other}.html">{bonus}</a><a href="../formalization{other}.html">{formal}</a></nav>
<details><summary>{licenses}</summary><ul>{license_links}</ul><p><a href="vendor/p5.js">p5.js source</a> · <a href="vendor/gsap.js">GSAP source</a> · <a href="vendor/ScrollTrigger.js">ScrollTrigger source</a></p></details>
</main></body></html>'''


def rewrite_page(path, site, version):
    original = path.read_text()
    prefix = posixpath.relpath('app', path.relative_to(site).parent.as_posix())
    text = original
    if path.name in ('index.html', 'index.en.html', 'index.th.html'):
        pattern = r'<script>.*?</script>'
        match = re.search(pattern, text, re.S)
        if not match or 'ipapi.co/json/' not in match.group():
            raise ValueError(f'Unknown language bootstrap: {path.name}; review offline adaptation')
        text = text[:match.start()] + text[match.end():]
    text = re.sub(r'<link\b[^>]*\bhref=["\']https://fonts\.(?:googleapis|gstatic)\.com[^>]*>', '', text)
    for url, local in RUNTIME_URLS.items():
        text = text.replace(url, prefix + '/' + local)
    # PDF exports are a separate published artifact, not part of this HTML reader.
    text = re.sub(r'<a\b[^>]*\bid="pdf-download"[^>]*>.*?</a>', '', text, flags=re.S)
    inject = (f'<meta http-equiv="Content-Security-Policy" content="{html.escape(CSP, quote=True)}">'
              f'<link rel="stylesheet" href="{prefix}/fonts.css">'
              f'<link rel="stylesheet" href="{prefix}/offline.css">'
              f'<script src="{prefix}/bootstrap.js"></script>')
    text = text.replace('<head>', '<head>' + inject, 1)
    lang = re.search(r'<html lang="([^"]+)"', text).group(1)
    # The bundled runtime starts afresh on each WebView navigation. Paint the
    # selected language immediately, rather than animate it in after JS loads.
    text = re.sub(
        r'<a\b([^>]*\bdata-lang="' + re.escape(lang) + r'"[^>]*)>',
        r'<a class="active" aria-current="page"\1>', text)
    label = {'ru': 'Об этом приложении', 'en': 'About this app', 'th': 'เกี่ยวกับแอป'}[lang]
    note = f'<p class="offline-version"><a class="offline-about" href="{prefix}/about.{lang}.html">{label}</a> · {html.escape(version)}</p>'
    text = text.replace('</footer>', note + '</footer>')
    path.write_text(text)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.resources = set(), [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids: raise ValueError(f'Duplicate HTML id: {attrs["id"]}')
            self.ids.add(attrs['id'])
        self.links += [attrs[k] for k in ('href', 'src', 'data-src') if k in attrs]
        if tag in ('script', 'img', 'audio', 'source', 'iframe') and attrs.get('src'):
            self.resources.append(attrs['src'])
        if tag == 'script' and attrs.get('data-src'):
            self.resources.append(attrs['data-src'])
        if tag == 'link' and attrs.get('href'):
            self.resources.append(attrs['href'])


def verify_site(site):
    pages = {p: Page(p) for p in site.rglob('*.html') if p.relative_to(site).parts[0] != 'agda'}
    def local(origin, link):
        uri = urllib.parse.urlsplit(html.unescape(link))
        if uri.scheme or uri.netloc: return None, uri
        target = (origin.parent / urllib.parse.unquote(uri.path)).resolve() if uri.path else origin
        if site not in target.parents or not target.is_file():
            raise ValueError(f'Broken or escaping local asset: {origin.relative_to(site)}: {link}')
        return target, uri
    for path, page in pages.items():
        for resource in page.resources:
            if urllib.parse.urlsplit(resource).scheme in ('http', 'https') or resource.startswith('//'):
                raise ValueError(f'Online runtime resource left in {path.name}: {resource}')
        for link in page.links:
            target, uri = local(path, link)
            if target in pages and uri.fragment and urllib.parse.unquote(uri.fragment) not in pages[target].ids:
                raise ValueError(f'Broken anchor: {path.name}: {link}')
    css_urls = re.compile(r'''url\(\s*(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|([^)]*))\s*\)''')
    for path in site.rglob('*.css'):
        for groups in css_urls.findall(path.read_text()):
            link = next((part for part in groups if part), '').strip()
            if link.startswith('data:'): continue
            if urllib.parse.urlsplit(link).scheme or link.startswith('//'):
                raise ValueError(f'Online CSS resource: {path}: {link}')
            local(path, link)
    return len(pages)


def prepare_site(destination, cache, offline, version):
    dependencies = vendor(cache, offline)
    with tempfile.TemporaryDirectory(prefix='iqj-web-snapshot-', dir='/tmp') as directory:
        work = Path(directory)
        manifest = source_snapshot(work)
        site = destination / 'site'
        site.mkdir(parents=True, exist_ok=False)
        for name in PUBLIC_FILES: copy_file(work / name, site / name)
        for name in PUBLIC_DIRS: shutil.copytree(work / name, site / name)
        for name in manifest['files']: copy_file(work / name, site / name)
        app = site / 'app'
        app.mkdir()
        for item in dependencies: copy_file(cache / item['file'], app / item['file'])
        copy_file(HERE / 'fonts.css', app / 'fonts.css')
        for name in ('bootstrap.js', 'offline.css'): copy_file(HERE / 'web' / name, app / name)
        for lang in ('ru', 'en', 'th'):
            (app / f'about.{lang}.html').write_text(about_page(lang, version))
        for path in site.rglob('*.html'):
            if path.relative_to(site).parts[0] != 'agda': rewrite_page(path, site, version)
        count = verify_site(site)
        files = {str(p.relative_to(site)): sha(p) for p in sorted(site.rglob('*')) if p.is_file()}
        snapshot = {'kind': 'iqj-offline-bundle', 'version': version, 'files': files,
                    'sha256': hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest(),
                    'agda_source_sha256': manifest['source_sha256']}
        (destination / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
        print(f'Offline snapshot: {count} HTML pages, {len(files)} files; {snapshot["sha256"][:16]}', flush=True)
        return site, snapshot


def build_apk(args, tools):
    output = outside(args.output_dir, 'APK output directory')
    state = outside(args.state_dir, 'Signing state directory')
    output.mkdir(parents=True, exist_ok=True)
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    counter_file = state / 'version.json'
    previous = json.loads(counter_file.read_text())['version_code'] if counter_file.exists() else 0
    code = previous + 1
    if not 1 <= code <= 2100000000: raise ValueError('Android version code is out of range')
    version = datetime.now(timezone.utc).strftime('%Y.%m.%d') + f'.{code}'
    apk = output / f'quadrobic-{version}.apk'
    if apk.exists(): raise ValueError(f'Output already exists; not overwriting: {apk}')
    with tempfile.TemporaryDirectory(prefix='iqj-android-build-', dir='/tmp') as directory:
        work = Path(directory)
        assets = work / 'assets'
        assets.mkdir()
        _, snapshot = prepare_site(assets, args.cache_dir, args.offline, version)
        resources = work / 'res'
        shutil.copytree(HERE / 'res', resources)
        copy_file(ROOT / 'logo/quadrobic-logo-avatar.png', resources / 'drawable/quadrobic.png')
        manifest = work / 'AndroidManifest.xml'
        manifest.write_text((HERE / 'AndroidManifest.xml').read_text()
                            .replace('@VERSION_CODE@', str(code)).replace('@VERSION_NAME@', version))
        compiled = work / 'resources.zip'
        run([tools['aapt2'], 'compile', '--dir', resources, '-o', compiled])
        unsigned = work / 'unsigned.apk'
        run([tools['aapt2'], 'link', '-o', unsigned, '-I', tools['android.jar'],
             '--manifest', manifest, '--min-sdk-version', str(MIN_API),
             '--target-sdk-version', str(API), compiled])
        classes = work / 'classes'; classes.mkdir()
        sources = sorted((HERE / 'src').rglob('*.java'))
        run([tools['javac'], '--release', '8', '-encoding', 'UTF-8', '-classpath', tools['android.jar'],
             '-d', classes, *sources])
        dex = work / 'dex'; dex.mkdir()
        run([tools['d8'], '--release', '--min-api', str(MIN_API), '--lib', tools['android.jar'],
             '--output', dex, *sorted(classes.rglob('*.class'))])
        with zipfile.ZipFile(unsigned, 'a', zipfile.ZIP_DEFLATED) as package:
            for path in dex.glob('*.dex'): package.write(path, path.name)
            # Package the explicit, audited asset set ourselves: AAPT2 silently
            # skips dotfiles, which would invalidate the checked source snapshot.
            for path in sorted(assets.rglob('*')):
                if path.is_file():
                    compression = zipfile.ZIP_STORED if path.suffix in ('.mp3', '.woff2', '.zip') else zipfile.ZIP_DEFLATED
                    package.write(path, 'assets/' + path.relative_to(assets).as_posix(), compress_type=compression)
        aligned = work / 'aligned.apk'
        run([tools['zipalign'], '-f', '4', unsigned, aligned])
        key = state / 'signing.p12'
        password_file = state / 'signing-password'
        if key.exists() != password_file.exists():
            raise ValueError('Incomplete signing state: restore both signing.p12 and signing-password')
        signing_env = os.environ.copy()
        if not key.exists():
            password = secrets.token_urlsafe(32)
            signing_env['IQJ_STORE_PASSWORD'] = password
            temporary_key = work / 'signing.p12'
            run([tools['keytool'], '-genkeypair', '-keystore', temporary_key, '-storetype', 'PKCS12',
                 '-alias', 'iqj', '-keyalg', 'RSA', '-keysize', '3072', '-validity', '10000',
                 '-dname', 'CN=Quadrobic offline reader', '-storepass:env', 'IQJ_STORE_PASSWORD',
                 '-keypass:env', 'IQJ_STORE_PASSWORD'], env=signing_env)
            shutil.copyfile(temporary_key, key); key.chmod(0o600)
            password_file.write_text(password); password_file.chmod(0o600)
        else:
            signing_env['IQJ_STORE_PASSWORD'] = password_file.read_text().strip()
        signed = work / 'signed.apk'
        run([tools['apksigner'], 'sign', '--ks', key, '--ks-key-alias', 'iqj',
             '--ks-pass', 'env:IQJ_STORE_PASSWORD', '--key-pass', 'env:IQJ_STORE_PASSWORD',
             '--out', signed, aligned], env=signing_env)
        run([tools['apksigner'], 'verify', '--verbose', signed])
        run([tools['zipalign'], '-c', '4', signed])
        verify_package(signed, snapshot)
        shutil.copy2(signed, apk)
        (output / (apk.name + '.sha256')).write_text(sha(apk) + '  ' + apk.name + '\n')
        result = {'package': PACKAGE, 'version_code': code, 'version_name': version,
                  'apk': str(apk), 'apk_sha256': sha(apk), 'content_sha256': snapshot['sha256']}
        temporary_counter = state / 'version.next.json'
        temporary_counter.write_text(json.dumps(result, indent=2) + '\n')
        temporary_counter.chmod(0o600)
        temporary_counter.replace(counter_file)
        (output / 'latest.json').write_text(json.dumps(result, indent=2) + '\n')
        print('APK:', apk, flush=True)
        if args.install:
            run([args.adb, 'install', '-r', apk])
    return apk


def verify_package(apk, snapshot):
    """AAPT must not silently drop any snapshotted asset, including dotfiles."""
    with zipfile.ZipFile(apk) as package:
        if 'classes.dex' not in package.namelist():
            raise ValueError('APK contains no DEX entrypoint')
        embedded = json.loads(package.read('assets/snapshot.json'))
        if embedded != snapshot:
            raise ValueError('APK snapshot metadata differs from the prepared content')
        for name, digest in snapshot['files'].items():
            entry = 'assets/site/' + name
            if entry not in package.namelist() or hashlib.sha256(package.read(entry)).hexdigest() != digest:
                raise ValueError(f'APK asset missing or changed: {name}')
    print('APK content hashes verified', flush=True)


def arguments():
    home = Path.home()
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='report toolchain availability without writing files')
    mode.add_argument('--prepare-only', action='store_true', help='render a browser-testable offline site without the SDK')
    parser.add_argument('--offline', action='store_true', help='require already cached, checksum-verified dependencies')
    parser.add_argument('--sdk-root', type=Path,
                        default=Path(os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_HOME') or '/opt/android-sdk'))
    parser.add_argument('--output-dir', type=Path,
                        default=Path(os.environ.get('XDG_DATA_HOME', str(home / '.local/share'))) / 'iqj-android')
    parser.add_argument('--state-dir', type=Path,
                        default=Path(os.environ.get('XDG_STATE_HOME', str(home / '.local/state'))) / 'iqj-android')
    parser.add_argument('--cache-dir', type=Path, default=HERE / '.cache')
    parser.add_argument('--install', action='store_true', help='explicitly install with adb -r after a successful build')
    parser.add_argument('--adb', default=shutil.which('adb'), help='adb executable for --install')
    args = parser.parse_args()
    args.sdk_root = args.sdk_root.expanduser().resolve()
    args.cache_dir = args.cache_dir.expanduser().resolve()
    if args.install and (args.check or args.prepare_only): parser.error('--install requires an APK build')
    if args.install and not args.adb: parser.error('--install requires adb (or --adb /path/to/adb)')
    return args


def main():
    args = arguments()
    # Enforce the artifact boundary even when a caller overrides XDG paths.
    outside(args.output_dir, 'Output directory')
    outside(args.state_dir, 'Signing state directory')
    if args.prepare_only:
        output = outside(args.output_dir, 'Preview directory')
        output.mkdir(parents=True, exist_ok=True)
        if (output / 'site').exists():
            raise ValueError('Preview site already exists; choose a new --output-dir')
        site, _ = prepare_site(output, args.cache_dir, args.offline, 'preview')
        print('Preview:', site)
        return 0
    tools = sdk_tools(args.sdk_root)
    if tools is None: return 2
    if args.check:
        for name, path in tools.items(): print(f'{name}: {path}')
        return 0
    state = outside(args.state_dir, 'Signing state directory')
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state / 'build.lock').open('a') as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Another Android build is using this signing state')
        build_apk(args, tools)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'Android build stopped: {error}', file=sys.stderr)
        raise SystemExit(1)

"""Pinned browser dependencies, shared by web renderers and the Android bundle.

Stable npm releases checked on 2026-11-23. Never use unversioned CDN URLs:
a dependency update must also refresh Android's source/license hashes and pass
browser checks, especially across a p5 major release.
"""
VERSIONS = {'p5': '2.4.0', 'gsap': '3.15.1', 'lenis': '1.3.27'}

# package, browser distribution, readable offline distribution, bundled path
SCRIPTS = (
    ('p5', 'lib/p5.min.js', 'lib/p5.js', 'vendor/p5.js'),
    ('gsap', 'dist/gsap.min.js', 'dist/gsap.js', 'vendor/gsap.js'),
    ('gsap', 'dist/ScrollTrigger.min.js', 'dist/ScrollTrigger.js', 'vendor/ScrollTrigger.js'),
    ('lenis', 'dist/lenis.min.js', 'dist/lenis.min.js', 'vendor/lenis.min.js'),
)


def cdn_url(package, path):
    return f'https://cdn.jsdelivr.net/npm/{package}@{VERSIONS[package]}/{path}'


def script_tags():
    return '\n'.join(f'<script defer src="{cdn_url(package, browser)}"></script>'
                     for package, browser, _, _ in SCRIPTS)


def offline_scripts():
    return {cdn_url(package, browser): local for package, browser, _, local in SCRIPTS}


def offline_sources():
    return {local: cdn_url(package, source) for package, _, source, local in SCRIPTS} | {
        'vendor/lenis.css': cdn_url('lenis', 'dist/lenis.css')}


def style_links():
    return f'<link rel="stylesheet" href="{cdn_url("lenis", "dist/lenis.css")}">'


def offline_resources():
    return offline_scripts() | {cdn_url('lenis', 'dist/lenis.css'): 'vendor/lenis.css'}


def main():
    """Explicit read-only check; importing this module never accesses a network."""
    import argparse
    import json
    import urllib.error
    import urllib.request

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--latest', action='store_true', help='compare with stable npm releases (network)')
    args = parser.parse_args()
    outdated = False
    for package, installed in VERSIONS.items():
        if not args.latest:
            print(f'{package}: {installed}')
            continue
        request = urllib.request.Request(f'https://registry.npmjs.org/{package}/latest',
                                         headers={'User-Agent': 'IQJ-dependency-check/1'})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                latest = json.load(response)['version']
        except (urllib.error.URLError, KeyError, ValueError) as error:
            raise SystemExit(f'Unable to check {package}: {error}') from error
        print(f'{package}: pinned {installed}, latest stable {latest}')
        outdated |= installed != latest
    if outdated:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

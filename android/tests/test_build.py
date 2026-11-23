"""Resource closure and artifact boundaries, runnable without the Android SDK."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import hashlib
import zipfile
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('iqj_android', Path(__file__).resolve().parents[1] / 'build.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class OfflineBuildTests(unittest.TestCase):
    def test_output_cannot_be_inside_checkout(self):
        with self.assertRaises(ValueError):
            builder.outside(builder.ROOT / 'android' / 'output', 'APK output')

    def test_symlink_cannot_bypass_output_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            alias = Path(temp) / 'checkout'
            alias.symlink_to(builder.ROOT, target_is_directory=True)
            with self.assertRaises(ValueError): builder.outside(alias / 'output', 'APK output')

    def test_unknown_online_runtime_resource_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / 'index.html').write_text('<script src="https://cdn.example/script.js"></script>')
            with self.assertRaisesRegex(ValueError, 'Online runtime resource'):
                builder.verify_site(site)

    def test_nested_data_svg_is_not_a_filesystem_url(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / 'index.html').write_text('<link rel="stylesheet" href="style.css">')
            (site / 'style.css').write_text('body{background:url("data:image/svg+xml,<svg filter=\'url(%23n)\'></svg>")}')
            self.assertEqual(builder.verify_site(site), 1)

    def test_local_css_font_must_exist(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / 'index.html').write_text('<link rel="stylesheet" href="style.css">')
            (site / 'style.css').write_text('@font-face{src:url(missing.woff2)}')
            with self.assertRaisesRegex(ValueError, 'Broken or escaping local asset'):
                builder.verify_site(site)

    def test_link_cannot_escape_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp) / 'site'; site.mkdir()
            (Path(temp) / 'private.txt').write_text('not an app asset')
            (site / 'index.html').write_text('<a href="../private.txt">outside</a>')
            with self.assertRaisesRegex(ValueError, 'escaping local asset'):
                builder.verify_site(site)

    def test_rewrite_preserves_relative_source_links(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp); page = site / 'formalization/code/Test.html'
            page.parent.mkdir(parents=True)
            gsap_url = next(url for url, name in builder.RUNTIME_URLS.items() if name == 'vendor/gsap.js')
            page.write_text('<html lang="en"><head></head><body><a href="../../agda/Test.agda">source</a>'
                            f'<script src="{gsap_url}"></script></body></html>')
            builder.rewrite_page(page, site, 'test')
            result = page.read_text()
            self.assertIn('src="../../app/vendor/gsap.js"', result)
            self.assertIn('href="../../agda/Test.agda"', result)
            self.assertIn('Content-Security-Policy', result)

    def test_offline_mode_rejects_modified_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); cache = root / 'cache'; cache.mkdir()
            (cache / 'dependency.js').write_text('tampered')
            (root / 'vendor-lock.json').write_text(json.dumps({'assets':[
                {'file':'dependency.js', 'sha256':'0'*64, 'url':'https://example.invalid/file'}]}))
            with patch.object(builder, 'HERE', root):
                with self.assertRaisesRegex(ValueError, 'Missing or changed cached dependency'):
                    builder.vendor(cache, offline=True)

    def test_package_cannot_drop_hidden_source_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            apk = Path(temp) / 'test.apk'
            content = b'ignored source metadata'
            snapshot = {'files': {'agda/.gitignore': hashlib.sha256(content).hexdigest()}}
            with zipfile.ZipFile(apk, 'w') as package:
                package.writestr('classes.dex', b'entrypoint')
                package.writestr('assets/snapshot.json', json.dumps(snapshot))
            with self.assertRaisesRegex(ValueError, 'APK asset missing or changed'):
                builder.verify_package(apk, snapshot)
            with zipfile.ZipFile(apk, 'a') as package:
                package.writestr('assets/site/agda/.gitignore', content)
            builder.verify_package(apk, snapshot)


if __name__ == '__main__': unittest.main()

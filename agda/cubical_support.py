"""Use a pinned external Cubical checkout without modifying its installation."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
LOCK = json.loads((HERE / 'cubical-lock.json').read_text())


def prepare_cubical(source=None):
    source = Path(source or os.environ.get('AGDA_CUBICAL',
                  Path.home() / '.local/share/agda/cubical')).expanduser().resolve()
    if source == HERE.parent or HERE.parent in source.parents:
        raise SystemExit('Cubical must be installed outside this checkout')
    if not (source / 'Cubical/Foundations/Prelude.agda').is_file():
        raise SystemExit(f'Cubical not found: {source}. Install {LOCK["repository"]} '
                         f'at {LOCK["tag"]} outside this repository; see agda/README.md.')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()
    try:
        commit = git('rev-parse', 'HEAD')
        if commit != LOCK['commit']:
            raise SystemExit(f'Cubical revision mismatch: expected {LOCK["commit"]}, got {commit}')
        if git('diff', 'HEAD', '--', 'Cubical', 'cubical.agda-lib'):
            raise SystemExit('Cubical has local source changes; use the clean pinned checkout')
        names = git('ls-files', 'Cubical', 'cubical.agda-lib').splitlines()
    except subprocess.CalledProcessError as error:
        raise SystemExit('Cubical must be a Git checkout at the pinned revision') from error
    files = [Path(n) for n in names if n.endswith(('.agda', '.agda-lib'))]
    hashes = {str(p): hashlib.sha256((source / p).read_bytes()).hexdigest() for p in files}
    fingerprint = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    # Interfaces belong in a writable external cache, never in the installed library.
    base = Path(tempfile.gettempdir()) / f'iqj-agda-{os.getuid()}'
    if base.is_symlink() or (base.exists() and base.stat().st_uid != os.getuid()):
        raise SystemExit(f'Unsafe Cubical cache directory: {base}')
    base.mkdir(mode=0o700, exist_ok=True)
    cache = base / fingerprint
    cache.mkdir(exist_ok=True)
    for p in files:
        target = cache / p
        if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != hashes[str(p)]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / p, target)
    return cache, dict(LOCK, source_sha256=fingerprint)

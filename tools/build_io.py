"""Small output helper shared by web builders; generated files stay deterministic."""
from pathlib import Path


def write_text_if_changed(path: Path, text: str) -> bool:
    """Preserve mtime when bytes are identical (watchers and incremental builds)."""
    content = text.encode('utf-8')
    if path.is_file() and path.read_bytes() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return True

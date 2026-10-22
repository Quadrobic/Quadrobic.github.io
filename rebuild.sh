#!/usr/bin/env bash
# Rebuilds the web page (all three languages) and the PDF in one command.
# Run this after any edit to README.md / README.en.md / README.th.md — or
# use tools/watch.py to do it automatically on every save.
set -euo pipefail
cd "$(dirname "$0")"

# The PDFs are only worth regenerating when something that actually feeds
# into them changed - the source .md, the PDF build script, its template,
# or the shared parser. A pure web-side edit (css/js/template.html) must
# not touch the PDF file or its embedded "Обновлено" timestamp (that
# timestamp is read from the .md's own mtime, so it only moves when the
# .md itself does - but the PDF file was still being rewritten on every
# run regardless, which is the noise this check removes).
needs_rebuild() {
  local target="$1"; shift
  [ -f "$target" ] || return 0
  local dep
  for dep in "$@"; do
    [ "$dep" -nt "$target" ] && return 0
  done
  return 1
}

echo "→ index.html"
python3 build.py

if needs_rebuild IQJ-manifest.pdf README.md pdf/build.py pdf/template.html tools/manifesto.py; then
  echo "→ IQJ-manifest.pdf"
  python3 pdf/build.py
else
  echo "→ IQJ-manifest.pdf (up to date, skipped)"
fi

echo "→ bird.html"
python3 build_bird.py

if needs_rebuild bird.pdf bird.md bird_build.py tools/manifesto.py; then
  echo "→ bird.pdf"
  python3 bird_build.py
else
  echo "→ bird.pdf (up to date, skipped)"
fi

echo "done."

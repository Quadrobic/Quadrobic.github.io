#!/usr/bin/env bash
# Rebuilds the web page (all three languages) and the PDF in one command.
# Run this after any edit to README.md / README.en.md / README.th.md — or
# use tools/watch.py to do it automatically on every save.
set -euo pipefail
cd "$(dirname "$0")"

# Every output is only regenerated when something that actually feeds into
# it changed - the source .md, its build script, its template, or the shared
# parser. A pure web-side edit (css/js) must not touch anything, and an
# unrelated edit must not touch the PDFs: Chrome's PDF output is not
# byte-identical between runs, so an unneeded rebuild always shows up as a
# diff. Skipping the HTML too keeps its "Обновлено" date stable after a
# commit (an uncommitted .md is dated by mtime, a committed one by its
# commit - so re-rendering right after committing would move the date).
#
# Decided by git rather than mtimes, since a checkout/pull on another
# machine resets every mtime:
#   - output already rebuilt but not yet committed: rebuild only if a dep was
#     edited again since (mtime is meaningful within this working copy);
#   - output committed: rebuild if a dep has uncommitted edits, or a dep was
#     committed after the output last was (e.g. text edited and committed
#     elsewhere without rebuilding).
# The "Обновлено" date itself comes from git too (tools/manifesto.py).
dirty() { [ -n "$(git status --porcelain -- "$1")" ]; }

needs_rebuild() {
  local target="$1"; shift
  [ -f "$target" ] || return 0
  local dep
  if dirty "$target"; then
    for dep in "$@"; do
      [ "$dep" -nt "$target" ] && return 0
    done
    return 1
  fi
  for dep in "$@"; do
    dirty "$dep" && return 0
  done
  local built
  built="$(git log -1 --format=%H -- "$target")"
  [ -n "$built" ] || return 0
  [ -n "$(git rev-list -1 "$built..HEAD" -- "$@")" ]
}

SITE_DEPS=(README.md README.en.md README.th.md build.py template.html tools/manifesto.py)
if needs_rebuild index.html "${SITE_DEPS[@]}" \
  || needs_rebuild index.en.html "${SITE_DEPS[@]}" \
  || needs_rebuild index.th.html "${SITE_DEPS[@]}"; then
  echo "→ index.html"
  python3 build.py
else
  echo "→ index.html (up to date, skipped)"
fi

if needs_rebuild IQJ-manifest.pdf README.md pdf/build.py pdf/template.html tools/manifesto.py; then
  echo "→ IQJ-manifest.pdf"
  python3 pdf/build.py
else
  echo "→ IQJ-manifest.pdf (up to date, skipped)"
fi

if needs_rebuild bird.html bird.md build_bird.py bird_template.html tools/manifesto.py; then
  echo "→ bird.html"
  python3 build_bird.py
else
  echo "→ bird.html (up to date, skipped)"
fi

if needs_rebuild bird.pdf bird.md bird_build.py tools/manifesto.py; then
  echo "→ bird.pdf"
  python3 bird_build.py
else
  echo "→ bird.pdf (up to date, skipped)"
fi

echo "done."

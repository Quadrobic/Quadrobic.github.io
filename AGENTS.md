# Working on Quadrobic

Start here. Read only the sources relevant to the request; generated pages can
contain hundreds of kilobytes of embedded or exported proofs.

## Source map

| Change | Edit | Build / check |
| --- | --- | --- |
| Treatise | `README.md`, `README.en.md` | `python3 build.py --lang ru --lang en` |
| Thai translation | `README.th.md`, only when explicitly requested | `python3 build.py --lang th` |
| Bonus story | `bird.md`, `bird.en.md` | `python3 build_bird.py` |
| Missing-page introduction | `404.html` (maintained directly, RU/EN) | `python3 tools/check_web.py`; no build |
| Page markup / translations of controls | `template.html`, `build.py`; bonus: `bird_template.html`, `build_bird.py` | Web builders above |
| Layout | `css/style.css`; proof/map/note CSS have separate files | No build for CSS/JS |
| Reading artwork | `tools/reading_art.py` selection, `.reading-plate` in `css/style.css`; originals in `pics/` | Web build; Android bundles selected files on its next explicit build |
| Browser library versions | `tools/runtime_libraries.py`; Android hashes: `android/vendor-lock.json` | Web build, offline preview and browser checks |
| Scroll, reveals, navigation | `js/main.js` | Browser check |
| Audio and font size / speech | `js/reader-controls.js` / `js/speech.js` | Browser check |
| Ink / frost / Death Star | `js/ink.js` / `js/frost.js` / `js/death-star.js` | Browser check, including Return |
| Definitions | Markdown glossary; matching forms: `tools/web_glossary.py`; behavior: `js/glossary.js` | Web build; Russian PDF when text changed |
| Claim status / bibliography | `agda/web_annotations.py` / `agda/web_readings.py` | `python3 agda/build_web.py`, then web build |
| Formalization presentation | `agda/web_content.py`, `agda/web_template.html` | Same formalization build |
| Agda proofs | `agda/Imperium/*.agda`; see `agda/README.md` | `python3 agda/check.py` |
| Android | `android/`; see `android/README.md` | Only build APK when explicitly requested |

## Editing boundaries

- Markdown is the text source. Do not edit `index*.html`, `bird*.html`,
  `formalization*.html`, `model-map*.html`, `formalization/code/`,
  `formalization/notes.*.js`, verification snapshots, ZIPs or PDFs by hand.
- Use `rg -n '^### §' README.md` then a focused `sed` range. Do not dump generated
  HTML, source archives, all of Agda, or the entire treatise to orient yourself.
- Preserve the author's ideas and voice. Use `-` instead of long dashes. Keep
  Hridaya as the mystical heart. A model theorem proves only its stated scope;
  distinguish definitions, assumptions, consequences and uncovered claims.
- Normally keep RU/EN aligned for prose edits; do not update Thai without a
  specific request. Bibliographic UI remains RU/EN. Technical Agda comments
  and documentation are English; preserve Sanskrit/Jain terminology.
- The web glossary is interactive; the PDF keeps the complete glossary.
  The Death Star seals the conclusion/practices until Return, which starts audio.
- Cubical is pinned and installed outside the repository. Do not vendor it,
  weaken `--safe`, introduce postulates, or relax negative checks to pass a build.
- Never run an APK build as part of an ordinary rebuild. APKs and signing keys
  stay outside the repository; never print the signing password.
- Respect existing working changes. Do not commit, publish or send messages
  unless requested. Do not introduce bundlers or minify maintained sources.

## Validation and efficient iteration

1. Inspect `git status --short` and focused diffs first.
2. Change source files, not generated copies. Script order is explicit in the two
   page templates; shared controls run after `main.js`.
3. `python3 tools/check_web.py` checks generated pages, assets, lazy notes and
   proof snapshot integrity without a network or browser. It does not build.
4. `python3 build.py --lang ru` renders only Russian; repeat `--lang` to select
   more. No-change builds preserve output mtimes. `./rebuild.sh` selects stale
   outputs, including PDFs; `python3 tools/watch.py` watches source dependencies.
5. Browser-check behavioral changes at desktop and mobile sizes. Test keyboard
   access and reduced motion; for notes, test first load, close-before-load and
   retry. For reading effects, verify Return and text-size/speech controls.
6. Inspect `git diff --check` and the final file list. Do not rerun heavy proof,
   PDF or Android builds for unrelated CSS/JS edits. See `TOOLING.md` for details.

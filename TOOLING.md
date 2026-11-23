# Building and maintaining the site

Read `AGENTS.md` first for a compact task-to-source map. This is a static site
with readable Python, JavaScript and CSS sources: no npm install, bundler,
minification step or server-side application is required.

## Sources and outputs

- `README.md`, `README.en.md`, `README.th.md`: treatise and complete glossary.
  They are authored Markdown, not project documentation. Thai is updated only
  on explicit request. RU/EN prose changes normally stay aligned.
- `tools/manifesto.py`: shared Markdown parser for the web and Russian PDF.
  Extend this parser when adding a new prose structure, rather than inventing
  another parser in a renderer.
- `template.html` and `build.py`: main page markup and localized control labels.
- `bird.md`, `bird.en.md`, `bird_template.html`, `build_bird.py`: bonus story.
  It has its own chapter grammar, while sharing the inline renderer and controls.
- `pdf/template.html`, `pdf/build.py`: Russian treatise PDF, with the full glossary.
  `bird_build.py` builds the Russian story PDF.
- `agda/`: proofs, model contracts, negative checks, bilingual explanations,
  claim annotations and reading catalog. See `agda/README.md` for proof work.

Generated files are published at the repository root for GitHub Pages. Never
hand-edit `index*.html`, `bird*.html`, `formalization*.html`, `model-map*.html`,
`formalization/code/`, `formalization/notes.*.js`, PDFs or the source ZIP.

## Select the smallest relevant build

```sh
python3 build.py --lang ru             # Russian page, notes and map only
python3 build.py --lang ru --lang en   # RU/EN, without touching Thai
python3 build.py                       # All three web editions
python3 build_bird.py                  # Both bonus editions
python3 pdf/build.py                   # Russian treatise PDF
python3 bird_build.py                  # Russian bonus PDF
./rebuild.sh                           # Rebuild stale outputs, including PDFs
python3 tools/watch.py                 # Source watcher; Ctrl+C to stop
./serve.sh                            # Local HTTP preview
```

Python web builds use the standard library. PDF builds also require an installed
Chrome/Chromium; candidates are listed in `pdf/build.py`. Repeated web builds
preserve the bytes and modification times of unchanged outputs. `rebuild.sh`
checks each language against its own Markdown source plus shared dependencies.
It does not rebuild a PDF for a CSS/JS edit, and never builds an APK.

Changing CSS or JS needs a browser reload, not an HTML build. Changing a shared
page template requires the corresponding web builder. Changing model claims,
readings, explanations or proofs requires the verified export first:

```sh
python3 agda/build_web.py
python3 build.py
```

The web builder rejects a stale Agda snapshot. Do not edit its hashes to bypass
that check. A bibliography change is a source change in the verified export,
even though it does not change a mathematical theorem.

## Runtime responsibilities

| File | Responsibility |
| --- | --- |
| `js/main.js` | Lenis/GSAP scroll, reveals, navigation, progress and initial hashes |
| `js/reader-controls.js` | Ambient/return audio and persistent text size |
| `js/speech.js` | Speech synthesis, voice selection and reading highlight |
| `js/ink.js` | p5 flow field, mood transitions and visibility/motion preferences |
| `js/frost.js` | Scroll-speed frost; no changes to text geometry |
| `js/death-star.js` | §38 phases, collective collapse, Return, explosion and unlock |
| `js/glossary.js` | Accessible definitions from the Markdown glossary |
| `js/model-notes.js` | Margin inspector, lazy proof/literature data, retry and focus |
| `js/model-map.js` | Actual § cross-reference graph and selected detail |
| `js/formalization.js` | Proof-page navigation, symbol highlighting and copying |
| `js/downloads.js` | PDF/APK disclosure and latest-release lookup |

The two page templates declare script order. Scripts are deferred while keeping
that order: p5, GSAP, ScrollTrigger, Lenis, then site behavior. Shared controls
and speech run after `main.js`; their scroll integration uses `window.__lenis`.
Frost and Death Star communicate through `reading:jump` and `reading:star-mode`;
Return dispatches `reading:return` and starts `audio/alquadro.mp3` from the click.

`template.html` keeps its small language bootstrap in the head: explicit language
choices win; geolocation is a narrow first-visit fallback. Android replaces this
bootstrap in its isolated bundle. Do not casually change the bootstrap's shape
without checking `android/build.py`.

The source order, hash links, text-size controls, speech, Return and reduced-motion
behavior must work on both the treatise and bonus pages where applicable. The
conclusion/practices stay sealed until Return on the web, not in the PDF.

## Definitions, notes and model status

Glossary definitions remain in Markdown. `tools/web_glossary.py` supplies matching
forms and web data; `js/glossary.js` annotates prose without changing its words.
There is no duplicate glossary to maintain at the bottom of the web page.

`tools/model_annotations.py` combines the checked claims/reading catalog with
current section titles. `build.py` generates `formalization/notes.ru.js` and
`formalization/notes.en.js`, separate from the primary reading HTML. These data
files load only when a marker is used. A content hash in their URL prevents a
new page from reading stale cards. A shared promise deduplicates concurrent
requests; closing or switching markers does not reopen an obsolete panel.
Failures show a localized retry message and a link to the complete map.
Script loading also works under `file://` and the Android asset origin.

All paragraph cards remain available on the separate map without lazy loading. It displays actual textual links, not proof implication. Model statuses
apply to individual claims: theorem, contract, open parameter, deliberately
excluded, or uncovered. Neither bibliography nor type checking certifies the
whole treatise. Keep that distinction in explanations and new annotations.

## Checks

```sh
python3 tools/check_web.py            # Offline, read-only asset/snapshot checks
node --check js/main.js               # Repeat for JavaScript files changed
python3 -m unittest discover -s android/tests -v  # When bundle behavior changes
python3 agda/check.py                 # When formal sources/export metadata change
```

The fast web check validates local assets and native anchors, unique IDs,
resolved placeholders, marker coverage, note hashes, reader script order and
Agda snapshot integrity. It does not download anything or prove browser behavior.

For interaction changes, browser-check desktop and mobile, mouse and keyboard,
reduced motion, first note load, early dismissal, failure/retry and the source
links. For animation changes also check frost thawing and Death Star Return.
Keep performance comparisons reproducible: separate HTML bytes and deferred
asset bytes; do not present a smaller HTML file as a measured overall speedup.

## Android and downloads

See `android/README.md`. Build the offline app only when explicitly requested:

```sh
./android/update.sh --check
./android/update.sh --prepare-only --offline --output-dir /tmp/iqj-preview
./android/update.sh --offline
```

The preview command creates an isolated site, not an APK. It must include the
lazy notes and all fonts, scripts and audio. APKs and signing state remain outside
the repository; backing up the signing state is necessary to retain update
compatibility. Reading stays offline; only the native GitHub release checker uses
Internet/network-state permissions. Update downloads open in the browser after
confirmation. No storage or package-install permission is requested.

The web Android link queries GitHub's latest published release only when clicked,
selecting its versioned APK. On API failure or timeout it opens the latest-release
page. Modified clicks/copied links use that page; no token is embedded.

Cubical v0.9 is also external, pinned by `agda/cubical-lock.json`. The checker
prepares its writable interface cache outside the repository. Never vendor the
library or weaken proof checks to make an export succeed.


## Browser dependency updates

`tools/runtime_libraries.py` is the single source for pinned stable versions,
CDN URLs, script order and offline filenames. Both page builders and the Android
rewriter use it. The Lenis stylesheet is pinned alongside its JavaScript. The ink script URL also
includes the p5 version so a major library update cannot reuse a stale canvas
adapter from the browser cache.

```sh
python3 tools/runtime_libraries.py          # Display pins, offline
python3 tools/runtime_libraries.py --latest # Read-only npm stable-release check
```

The current pins, checked on 2026-11-23, are p5.js 2.4.0, GSAP/ScrollTrigger
3.15.1 and Lenis 1.3.27. Never use `@latest` or a floating major version on the
published site: the checked source must identify exactly which code is loaded.
To update, change the shared pins, review upstream changes, refresh matching
readable sources/license notices and SHA-256 digests in `android/vendor-lock.json`,
then rebuild the web pages and an offline preview. `tools/check_web.py` detects
outdated/reordered page scripts and mismatches with the offline lock. Run the
browser checks before accepting the update, especially a p5 major upgrade.


For p5 2, assign the canvas DOM id through `canvasEl.elt.id`: the renderer's
`.id()` method can overwrite renderer dimensions from a zero-size layout during
setup. The ink field draws its short segments directly on the p5 Canvas2D
context to avoid per-particle Shape/Path2D allocation, retaining p5's noise,
colors, width and pixel-density handling. Regression checks should inspect
nonzero canvas dimensions and visible pixels, not just drawing calls.

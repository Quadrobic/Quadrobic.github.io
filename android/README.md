# Quadrobic offline reader for Android

A separate, manually built Android application. The app packages the current
Russian, English, and Thai treatise, the RU/EN bonus, glossary, model notes,
formalization pages, highlighted Agda modules, source archive, and return music.
It uses the existing site's appearance in a WebView, served from packaged assets
at a stable HTTPS origin. The native update checker has Internet and network-state
permissions; the WebView still rejects remote requests. No storage permission is used.
External bibliography links open in another browser only when selected.

`rebuild.sh` does not call this builder. Building the app does not rewrite the
published site: current Markdown is rendered in a temporary directory. A changed
Agda model must first be verified/exported with `python3 agda/build_web.py`; an
outdated verification snapshot stops the Android build.

## Toolchain on Gentoo

Required: Python 3, JDK 17 or newer with `java`, `javac`, and `keytool`, an Android SDK
platform at API 35 or newer, and SDK Build Tools 35.0.0 or newer. Android Studio,
Gradle, Maven, an emulator, and the NDK are not required to build an APK.
Minimum device version: Android 8.0 (API 26), with a current Android System WebView.
The app targets API 35 and has no native ABI-specific libraries.

Inspect the toolchain without downloading or building anything:

```sh
./android/update.sh --check
```

If only Gentoo's command-line tools are installed, add these packages separately:

```sh
/opt/android-sdk/cmdline-tools/latest/bin/sdkmanager \
  --sdk_root=/opt/android-sdk \
  "platforms;android-35" "build-tools;35.0.0"
```

Run SDK Manager with permission to write that SDK directory and accept its
licenses interactively. Alternatively choose a writable SDK directory and pass
it with `--sdk-root`, `ANDROID_SDK_ROOT`, or `ANDROID_HOME`. The builder never
installs SDK packages, accepts SDK licenses, or updates the system JDK.

## Explicit app update

```sh
./android/update.sh
# For an already populated dependency cache, prohibit all build-time downloads:
./android/update.sh --offline
# Optional explicit installation on a connected device:
./android/update.sh --offline --install
```

`--install` uses `adb install -r` and does not uninstall the existing app.
Without that flag no device is accessed. Use `--adb /path/to/adb` if necessary.
Install the resulting APK manually if you do not use adb. This is a sideloaded
APK workflow, not a Play Store publication workflow.

Every successful build increases the Android version code and uses the same
signing key. Language, last document, per-page reading position, text-size
preferences, and the completed return from the Death Star survive app updates.
Reading progress stays on the device. No account or background update service
is used. Existing explicit section links take precedence over stored positions.

Page changes retain the previous viewport in memory until local fonts and the
saved reading position are ready, then wait for WebView's visual-state callback
before revealing the new page. A short crossfade hides intermediate control
states; reduced motion disables the fade. Same-page anchors remain immediate.
The temporary frame is released after navigation and is never written to disk.
This uses [WebView's visual-state callback](https://developer.android.com/reference/android/webkit/WebView#postVisualStateCallback(long,android.webkit.WebView.VisualStateCallback)),
since completion of a page load does not itself guarantee a completed paint.

## In-app release checks

While the reader is open and Android reports an Internet connection, a native
worker checks this repository's latest stable GitHub release. It checks at most
once an hour after a successful request, retries failures after 15 minutes,
and also notices a connection becoming available while the app is open. A timer
revisits the schedule every 15 minutes while the Activity is resumed; it stops
when the reader is paused. A newly installed build ignores the previous build's
cooldown, and a discovered update is retained across process restarts. Offline
use and network/API errors remain silent. There is no background service.

Only an uploaded `quadrobic-YYYY.MM.DD.counter.apk` on the exact repository's
HTTPS release path is offered. Its counter must exceed the installed version's
counter (the Android version code); dates alone cannot trigger a downgrade.
The prompt follows the current document's RU/EN/TH language and offers Download
or Later. The same release is offered at most once per day. Download opens the
APK in the browser; the reader neither downloads it automatically nor launches
the installer. The user installs it over the existing app, with Android checking
the package signature. Keep using the same signing state when publishing releases.

The About page also offers **Check for updates**. In the installed reader, this
user-initiated check bypasses both the cooldown and the daily prompt suppression,
and reports no connection, a check failure, or an up-to-date installation. In a
browser preview, the same link opens GitHub's latest release page. Only an actual
user decision (Download, Later, or cancellation) suppresses the prompt; pausing
the Activity while it is displayed does not count as declining the update.

The first app version containing this feature must be installed manually;
previous builds cannot discover updates retroactively. Nothing is sent from the
reading history: the request is only public release metadata from GitHub.

## Files outside the repository

Default outputs:

- APKs and `latest.json`: `${XDG_DATA_HOME:-$HOME/.local/share}/iqj-android/`
- Signing key, private password file, and version counter:
  `${XDG_STATE_HOME:-$HOME/.local/state}/iqj-android/`
- Temporary generation, Java classes, DEX, and unsigned APKs: `/tmp/`
- Downloaded dependency cache: ignored `android/.cache/`

Keep a backup of the **whole signing-state directory**. A different signing key
cannot update an installed copy of the same application. This key is generated
locally for this app, not the SDK's shared debug key. The build uses a state lock
to prevent concurrent builds from generating incompatible keys or version codes.
The password is passed to signing tools through an environment variable, not a
printed command argument. The builder never prints its value.

`--output-dir` and `--state-dir` override the defaults. Both must resolve outside
the checkout; the builder rejects even a symlink back into it. APK, AAB, temporary
APK, and keystore patterns are ignored in Git as a second precaution. No compiled
application or private signing material belongs in this repository.

## Offline dependencies and scope

`vendor-lock.json` pins all dependency URLs and SHA-256 digests. The first build
can fetch those exact files; later builds use the verified cache. `--offline`
rejects a missing or changed dependency instead of silently fetching it. Updating
the pins in `../tools/runtime_libraries.py` requires an explicit lock-file review.
That module supplies the same URLs and versions to the web templates, offline
rewriter and app notices. The pinned Lenis CSS is bundled as well. The GSAP license HTML is a reviewed repository snapshot in `licenses/`, verified
against the lock-file hash; builds do not hash a changing live web page.
Fonts are local
WOFF2 subsets, including Cyrillic and Thai. Original p5.js and GSAP source files,
license texts/notices, and the Lenis license ship inside the app.

The offline adaptation removes IP geolocation and remote font/CDN requests. It
also removes the separate PDF-export buttons and browser speech-synthesis UI:
this application reads current HTML and does not depend on a PDF renderer or an
online voice. Bundled MP3/Web Audio, normal reading, glossary, and model notes
remain available. Source/archive downloads use Android's document picker.

Decorative reading plates share the web selection in `../tools/reading_art.py`.
Only selected originals from `pics/` enter the offline asset snapshot; unused
art is not bundled. The pictures stay between passages and load locally.

The Russian story «Человек, которого не видно» is bundled as `yard.html`,
with the same art and final Draw button. Both bonus pages link to it in their
chapter menu and after the story; the web's floating shortcut is moved into
the menu before reading. On other pages, five quick activations of the menu button within four
seconds reveal **Человек, которого не видно · RU** inside the menu. The entry stays revealed
for the WebView session. On tablets, or with a keyboard, five activations of the
build number in the footer or About page provide the same entry. The bonus links are available without the secret gesture. Each edition keeps its own reading place and Return state;
returning from the yard's Death Star does not unlock the canonical conclusion.

`ReaderActivity` maps only the app's HTTPS asset origin to `AssetManager`; it
has no JavaScript-to-Java bridge and enables no `file://` or content-provider
access in WebView. Other runtime requests receive an offline response. A content
policy independently limits runtime scripts, styles, fonts, and media to local
assets. Runtime sources and external bibliography links are treated differently.

## Verification without an Android SDK

```sh
python3 -m unittest discover -s android/tests -v
./android/update.sh --prepare-only --offline --output-dir /tmp/iqj-reader-preview
python3 -m http.server 8080 --directory /tmp/iqj-reader-preview/site
```

Choose a new preview directory for each preparation; an existing `site/` is never
overwritten. This preview uses the same asset closure as the APK. It validates
local links, anchors, fonts, and stylesheet URLs, including nested SVG data URLs;
rejects online runtime resources; and exports `snapshot.json` with content hashes.
It leaves the repository's HTML files unchanged. Browser checks do not replace
compilation or a device/emulator test of the Java host.

Official tool references:
[AAPT2](https://developer.android.com/tools/aapt2),
[D8](https://developer.android.com/tools/d8),
[APK signing](https://developer.android.com/tools/apksigner), and
[loading in-app web content](https://developer.android.com/develop/ui/views/layout/webapps/load-local-content).
Release metadata follows the [GitHub Releases API](https://docs.github.com/en/rest/releases/releases#get-the-latest-release).
The small host implements the asset-origin mapping directly, without an AndroidX
download, so a missing Gradle installation does not block this app.

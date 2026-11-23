# Quadrobic offline reader for Android

A separate, manually built Android application. The app packages the current
Russian, English, and Thai treatise, the RU/EN bonus, glossary, model notes,
formalization pages, highlighted Agda modules, source archive, and return music.
It uses the existing site's appearance in a WebView, served from packaged assets
at a stable HTTPS origin. The manifest has no Internet or storage permission.
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
rewriter and app notices. The pinned Lenis CSS is bundled as well. Fonts are local
WOFF2 subsets, including Cyrillic and Thai. Original p5.js and GSAP source files,
license texts/notices, and the Lenis license ship inside the app.

The offline adaptation removes IP geolocation and remote font/CDN requests. It
also removes the separate PDF-export buttons and browser speech-synthesis UI:
this application reads current HTML and does not depend on a PDF renderer or an
online voice. Bundled MP3/Web Audio, normal reading, glossary, and model notes
remain available. Source/archive downloads use Android's document picker.

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
The small host implements the asset-origin mapping directly, without an AndroidX
download, so a missing Gradle installation does not block this app.

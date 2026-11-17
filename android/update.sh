#!/usr/bin/env bash
# Explicit APK refresh; intentionally never called by ../rebuild.sh.
set -euo pipefail
exec python3 "$(dirname "$(realpath "$0")")/build.py" "$@"

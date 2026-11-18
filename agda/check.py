#!/usr/bin/env python3
"""Check the model and expected rejections with a private, offline stdlib cache."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from cubical_support import prepare_cubical

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "_build"
CACHE = BUILD / "stdlib"
CUBICAL_STDLIB = BUILD / "cubical-stdlib"


def digest(path):
    return hashlib.sha256(path.read_bytes()).digest()


def prepare_stdlib(source, cache=CACHE):
    """Only Agda sources; never write interfaces into a system installation."""
    sources = [p for p in source.rglob("*.agda")
               if "_build" not in p.relative_to(source).parts]
    if not sources or not (source / "Data/Nat.agda").is_file():
        raise SystemExit(f"Not an Agda standard library source directory: {source}")
    expected = set()
    for p in sources:
        rel = p.relative_to(source)
        expected.add(rel)
        target = cache / rel
        if not target.exists() or digest(target) != digest(p):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
    # A library upgrade must not leave removed source modules available.
    for p in cache.rglob("*.agda"):
        if p.relative_to(cache) not in expected:
            p.unlink()
    # Preserve the installed library's non-Cubical compatibility warning setting.
    # No safety, termination, positivity or coverage checks are disabled.
    (cache / "standard-library.agda-lib").write_text(
        "name: imperium-private-stdlib\ninclude: .\n"
        "flags: --warning=noUnsupportedIndexedMatch\n", encoding="utf-8")


def run(agda, target, include, log, cubical=None):
    args = [agda, "--no-libraries", "--safe",
            "--cubical" if cubical else "--without-K", "-Werror",
            "-WnoUnsupportedIndexedMatch", "-i", str(ROOT), "-i", str(CUBICAL_STDLIB if cubical else CACHE)]
    if cubical:
        args.extend(["-i", str(cubical)])
    if include:
        args.extend(["-i", str(include)])
    result = subprocess.run(args + [str(target)], cwd=ROOT,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with log.open("a", encoding="utf-8") as f:
        f.write("\n$ " + " ".join(args + [str(target)]) + "\n" + result.stdout)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdlib", type=Path,
                        default=Path(os.environ.get("AGDA_STDLIB", "/usr/share/agda-stdlib")))
    parser.add_argument("--cubical", type=Path, help="external pinned Cubical checkout")
    parser.add_argument("--fresh", action="store_true",
                        help="discard generated interfaces before checking (slow)")
    args = parser.parse_args()
    agda = shutil.which("agda")
    if not agda:
        raise SystemExit("agda not found on PATH")
    source = args.stdlib.expanduser().resolve()
    if not source.is_dir() or source == BUILD.resolve() or BUILD.resolve() in source.parents:
        raise SystemExit("Choose the installed stdlib source, not the generated cache")
    BUILD.mkdir(exist_ok=True)
    if args.fresh:
        for p in ROOT.rglob("*.agdai"):
            p.unlink()
    prepare_stdlib(source)
    prepare_stdlib(source, CUBICAL_STDLIB)
    cubical, dependency = prepare_cubical(args.cubical)
    log = BUILD / "check.log"
    version = subprocess.check_output([agda, "--version"], text=True)
    if not version.startswith("Agda version " + dependency['agda_series'] + "."):
        raise SystemExit(f"Pinned Cubical requires Agda {dependency['agda_series']}.x; got {version.strip()}")
    log.write_text(version + f"stdlib source: {source}\n", encoding="utf-8")
    print(version.splitlines()[0], flush=True)
    print("Checking All.agda (--safe --without-K, warnings are errors)...", flush=True)
    positive = run(agda, ROOT / "All.agda", None, log)
    if positive.returncode:
        print(positive.stdout[-14000:])
        raise SystemExit(f"Model failed; full log: {log}")
    print("PASS: all modules, Doctrine instance and regression proofs", flush=True)
    print("Checking CubicalAll.agda (--safe --cubical)...", flush=True)
    extension = run(agda, ROOT / "CubicalAll.agda", None, log, cubical)
    if extension.returncode:
        print(extension.stdout[-14000:])
        raise SystemExit(f"Cubical extension failed; full log: {log}")
    print("PASS: CubicalAll, tail quotient and TwoLevels instance", flush=True)
    (BUILD / "cubical-dependency.json").write_text(
        json.dumps(dependency, indent=2) + "\n", encoding="utf-8")
    count = 0
    for target in sorted((ROOT / "tests/reject").glob("*.agda")):
        result = run(agda, target, target.parent, log)
        # Rejecting a typo or a missing dependency would not test the intended claim.
        expected = ("Cannot postulate" if target.stem == "UnsafePostulate" else
                    "Unsolved" if target.stem == "UnsolvedHole" else
                    "error: [UnequalTerms]")
        if result.returncode == 0 or expected not in result.stdout:
            print(result.stdout[-7000:])
            raise SystemExit(f"Unexpected negative-test result: {target.name}; see {log}")
        print(f"PASS: rejected {target.stem}", flush=True)
        count += 1
    if count != 28:
        raise SystemExit(f"Expected 28 negative tests, found {count}")
    cubical_count = 0
    for target in sorted((ROOT / "tests/cubical-reject").glob("*.agda")):
        result = run(agda, target, target.parent, log, cubical)
        if result.returncode == 0 or "error: [UnequalTerms]" not in result.stdout:
            print(result.stdout[-7000:])
            raise SystemExit(f"Unexpected Cubical negative-test result: {target.name}")
        print(f"PASS: rejected {target.stem}", flush=True)
        cubical_count += 1
    if cubical_count != 3:
        raise SystemExit(f"Expected 3 Cubical negative tests, found {cubical_count}")
    print(f"OK: model + Cubical extension + {count + cubical_count} expected rejections. Log: {log}", flush=True)


if __name__ == "__main__":
    main()

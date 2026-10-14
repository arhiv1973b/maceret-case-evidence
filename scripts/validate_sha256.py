#!/usr/bin/env python3
"""
A©tor Evidence Integrity Validator
CASE-MACHERET-1997-2026 | TI-ULA

Scans files listed in proofs/manifest.json and verifies:
  - SHA-256 checksums
  - presence of required udhr_articles field (list of integers)
Exit code 0 = all OK, 1 = mismatch, missing file or structural error.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

MANIFEST_PATH = Path("proofs/manifest.json")
REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_UDHR = {5, 6, 7, 8, 17}


def sha256_of_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_udhr_articles(entry: dict, file_id: str) -> list:
    """Return list of structural error messages (empty = OK)."""
    errors = []
    articles = entry.get("udhr_articles")
    if articles is None:
        errors.append(f"{file_id}: missing required field 'udhr_articles'")
        return errors
    if not isinstance(articles, list):
        errors.append(f"{file_id}: 'udhr_articles' must be a list")
        return errors
    if len(articles) == 0:
        errors.append(f"{file_id}: 'udhr_articles' must not be empty")
    for a in articles:
        if not isinstance(a, int) or a not in ALLOWED_UDHR:
            errors.append(f"{file_id}: invalid UDHR article {a!r} (allowed: {sorted(ALLOWED_UDHR)})")
    return errors


def main() -> int:
    os.chdir(REPO_ROOT)

    if not MANIFEST_PATH.exists():
        print(f"[FAIL] Manifest not found: {MANIFEST_PATH}")
        return 1

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("=" * 70)
    print(f"CASE: {manifest.get('case_id', 'N/A')}")
    print(f"Actor: {manifest.get('actor_key', 'N/A')}")
    print(f"Generated: {manifest.get('generated_at', 'N/A')}")
    print(f"Legal framework: UDHR 1948 + ICCPR + UN Special Procedures only")
    print("=" * 70)

    files = manifest.get("files", [])
    if not files:
        print("[WARN] No files listed in manifest.")
        return 0

    ok_count = 0
    fail_count = 0
    missing_count = 0
    structural_errors = 0

    for entry in files:
        rel_path = entry.get("path")
        expected = entry.get("sha256", "").lower()
        size_expected = entry.get("size_bytes")
        file_id = entry.get("id", rel_path)

        # Structural check for udhr_articles
        udhr_errs = validate_udhr_articles(entry, file_id)
        if udhr_errs:
            for e in udhr_errs:
                print(f"[STRUCT]  {e}")
            structural_errors += len(udhr_errs)
            fail_count += 1
            continue

        full_path = REPO_ROOT / rel_path

        if not full_path.exists():
            print(f"[MISSING] {file_id}")
            print(f"          Expected path: {rel_path}")
            print(f"          UDHR articles: {entry.get('udhr_articles')}")
            missing_count += 1
            fail_count += 1
            continue

        actual = sha256_of_file(full_path)
        actual_size = full_path.stat().st_size

        if actual == expected and (size_expected is None or actual_size == size_expected):
            print(f"[OK]      {file_id}")
            print(f"          {rel_path}")
            print(f"          SHA-256: {actual}")
            print(f"          UDHR articles: {entry.get('udhr_articles')}")
            ok_count += 1
        else:
            print(f"[FAIL]    {file_id}")
            print(f"          Path: {rel_path}")
            print(f"          Expected SHA-256: {expected}")
            print(f"          Actual   SHA-256: {actual}")
            if size_expected is not None and actual_size != size_expected:
                print(f"          Size mismatch: expected {size_expected}, got {actual_size}")
            fail_count += 1

    print("=" * 70)
    print(f"Result: {ok_count} OK | {fail_count} FAIL | {missing_count} MISSING | {structural_errors} STRUCT")
    print("=" * 70)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

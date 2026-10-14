#!/usr/bin/env python3
"""
A©tor: integrate compressed evidence manifest v1.3.2
CASE-MACHERET-1997-2026
"""

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_SRC = REPO_ROOT.parent / "legal_submission_fincombank_20260903.pdf"
PDF_DEST = REPO_ROOT / "docs" / "soprovoditelnoe-pismo-10-10-2026.pdf"
MANIFEST_PATH = REPO_ROOT / "proofs" / "manifest.json"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def run_git(cmd: list[str]) -> None:
    print(f"[GIT] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr.strip()}")
        raise SystemExit(1)
    if result.stdout.strip():
        print(result.stdout.strip())


def main() -> None:
    if not PDF_SRC.exists():
        print(f"[ERROR] Исходный файл не найден: {PDF_SRC}")
        raise SystemExit(1)

    # Копирование файла в docs/
    PDF_DEST.parent.mkdir(parents=True, exist_ok=True)
    import shutil

    shutil.copy2(PDF_SRC, PDF_DEST)
    print(f"[INFO] Скопировано: {PDF_SRC} -> {PDF_DEST}")

    # 1. Расчёт SHA-256 и размера
    file_sha = sha256_of_file(PDF_DEST)
    file_size = PDF_DEST.stat().st_size
    print(f"[INFO] SHA-256 : {file_sha}")
    print(f"[INFO] Size    : {file_size} bytes")

    # 2. Обновление manifest.json
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["manifest_version"] = "1.3.2"
    manifest["generated_at"] = datetime.now(timezone(timedelta(hours=3))).strftime(
        "%Y-%m-%dT%H:%M:%S+03:00"
    )

    updated = False
    for entry in manifest.get("files", []):
        if entry.get("id") == "COVER-LETTER-2026-10-10":
            entry["sha256"] = file_sha
            entry["size_bytes"] = file_size
            entry["path"] = "docs/soprovoditelnoe-pismo-10-10-2026.pdf"
            entry["original_filename"] = "legal_submission_fincombank_20260903.pdf"
            entry["description"] = (
                "Сопроводительное письмо к Меморандуму правового статуса + полный комплект "
                "доказательств (жалобы IP Centru/GP, ответ FinComBank №6647/Out, Aviz №269, "
                "Identity Chain, акт усыновления 1977 и др.)"
            )
            updated = True
            break

    if not updated:
        print("[WARN] Запись COVER-LETTER-2026-10-10 не найдена — добавляю новую")
        manifest.setdefault("files", []).insert(
            0,
            {
                "id": "COVER-LETTER-2026-10-10",
                "path": "docs/soprovoditelnoe-pismo-10-10-2026.pdf",
                "original_filename": "legal_submission_fincombank_20260903.pdf",
                "description": "Сопроводительное письмо + полный комплект доказательств",
                "sha256": file_sha,
                "size_bytes": file_size,
                "mime_type": "application/pdf",
                "date": "2026-10-10",
                "google_drive_view_link": None,
                "google_drive_file_id": None,
                "udhr_articles": [6, 7, 17],
                "tags": [
                    "cover-letter",
                    "fincombank",
                    "6647-Out",
                    "identity-recognition",
                ],
            },
        )

    notes = manifest.get("notes", [])
    note_v = (
        "v1.3.2: Integrated cover letter (legal_submission_fincombank_20260903.pdf)"
    )
    if note_v not in notes:
        notes.append(note_v)
    manifest["notes"] = notes

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("[INFO] proofs/manifest.json обновлён → v1.3.2")

    # 3. Валидация
    print("\n[VALIDATE]")
    val = subprocess.run(
        ["python", "scripts/validate_sha256.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    print(val.stdout)
    if val.returncode != 0:
        print(f"[ERROR] Валидация не прошла:\n{val.stderr}")
        raise SystemExit(1)

    # 4. Git add / commit / push
    run_git(
        [
            "git",
            "add",
            "docs/soprovoditelnoe-pismo-10-10-2026.pdf",
            "proofs/manifest.json",
        ]
    )
    run_git(
        ["git", "commit", "-m", "A©tor: integrate compressed evidence manifest v1.3.2"]
    )
    run_git(["git", "push", "origin", "main"])

    print("\n[DONE] Интеграция и push выполнены успешно.")


if __name__ == "__main__":
    main()

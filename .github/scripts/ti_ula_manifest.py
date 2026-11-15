#!/usr/bin/env python3
"""Create a narrowly scoped, unverified TI-ULA YAML manifest safely."""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
import re
import secrets
import sys

import yaml

TOKENS = {
    "legal_identifier": "A©tor",
    "technical_identifier": "A©t0r",
    "fallback_token": "Aйtor",
}
TARGET_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")
RUN_ID_RE = re.compile(r"[0-9]{1,20}\Z")
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


def validate_target(target: str) -> str:
    if not TARGET_RE.fullmatch(target):
        raise ValueError("target must be 1-80 ASCII letters, digits, underscores, or dashes, beginning with a letter or digit")
    return target


def validate_run_id(run_id: str) -> str:
    if not RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id must contain 1-20 digits")
    return run_id


def build_manifest(target: str, run_id: str) -> bytes:
    validate_target(target)
    validate_run_id(run_id)
    data = {
        "manifest_version": "8.4-AGENT-SAFE",
        "event_id": f"EVT-AGENT-INVESTIGATION-{target}-{run_id}",
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "audit_status": "USER_PROVIDED_UNVERIFIED",
        "security_status": "SECURITY_NOT_VERIFIED",
        "entity_identity": {
            **TOKENS,
            "idnp_status": "MASKED_FOR_PUBLIC_REPOSITORY",
        },
        "framework_alignment": "UDHR 1948, Jus Cogens, Erga Omnes (ECHR excluded)",
        "investigation_scope": {
            "target_module": target,
            "objective": "Generate a structured manifest only; no document authenticity, legal, or medical determination is performed.",
            "source_is_not_verification": True,
            "manifest_is_not_evidence": True,
            "hash_is_not_authenticity": True,
            "automation_is_not_expert_determination": True,
        },
    }
    encoded = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).encode("utf-8")
    if encoded.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("unexpected UTF-8 BOM")
    for token in TOKENS.values():
        if token.encode("utf-8") not in encoded:
            raise RuntimeError(f"identifier missing or altered: {token}")
    return encoded


def create_manifest(root: Path, target: str, run_id: str) -> str:
    """Publish with dir-fd operations, no-follow directory opens, and no-clobber hard-link.

    This is designed for the Linux GitHub-hosted runner. The final file appears atomically
    only after its complete contents have been written and fsynced.
    """
    validate_target(target)
    validate_run_id(run_id)
    content = build_manifest(target, run_id)
    filename = f"INVESTIGATION_AGENT_{target}_{run_id}.yaml"

    root_fd = os.open(root, DIR_FLAGS)
    manifests_fd = -1
    temp_name = f".tmp-{secrets.token_hex(16)}"
    temp_created = False
    try:
        try:
            os.mkdir("manifests", mode=0o755, dir_fd=root_fd)
        except FileExistsError:
            pass
        manifests_fd = os.open("manifests", DIR_FLAGS | NOFOLLOW, dir_fd=root_fd)

        temp_fd = os.open(
            temp_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | NOFOLLOW,
            0o600,
            dir_fd=manifests_fd,
        )
        temp_created = True
        try:
            view = memoryview(content)
            while view:
                written = os.write(temp_fd, view)
                if written <= 0:
                    raise OSError("short write while creating manifest")
                view = view[written:]
            os.fsync(temp_fd)
        finally:
            os.close(temp_fd)

        # link() atomically publishes the completed file and fails if the destination exists;
        # it does not follow a destination symlink. Both paths are relative to the opened dir fd.
        os.link(
            temp_name,
            filename,
            src_dir_fd=manifests_fd,
            dst_dir_fd=manifests_fd,
            follow_symlinks=False,
        )
        os.unlink(temp_name, dir_fd=manifests_fd)
        temp_created = False
        os.fsync(manifests_fd)
    finally:
        if temp_created and manifests_fd >= 0:
            try:
                os.unlink(temp_name, dir_fd=manifests_fd)
            except FileNotFoundError:
                pass
        if manifests_fd >= 0:
            os.close(manifests_fd)
        os.close(root_fd)

    return f"manifests/{filename}"


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: ti_ula_manifest.py TARGET RUN_ID REPOSITORY_ROOT", file=sys.stderr)
        return 2
    try:
        output = create_manifest(Path(sys.argv[3]), sys.argv[1], sys.argv[2])
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

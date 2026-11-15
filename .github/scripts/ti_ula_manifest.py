#!/usr/bin/env python3
"""Create a narrowly scoped, explicitly unverified TI-ULA YAML manifest."""

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


class PublicationError(RuntimeError):
    """Publication failed; status describes whether the final file may exist."""

    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


def _required_flags() -> tuple[int, int]:
    required = ("O_DIRECTORY", "O_NOFOLLOW", "O_CLOEXEC")
    if any(not hasattr(os, flag) for flag in required):
        raise RuntimeError("REQUIRED_FILESYSTEM_FLAGS_UNAVAILABLE")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    file_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    return directory_flags, file_flags


def validate_target(target: str) -> str:
    if not isinstance(target, str) or not TARGET_RE.fullmatch(target):
        raise ValueError("target must be 1-80 ASCII letters, digits, underscores, or dashes, beginning with a letter or digit")
    return target


def validate_run_id(run_id: str) -> str:
    if not isinstance(run_id, str) or not RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id must contain 1-20 digits")
    return run_id


def build_manifest(target: str, run_id: str) -> bytes:
    validate_target(target)
    validate_run_id(run_id)
    data = {
        "manifest_version": "9.2-SAFE",
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
        raise RuntimeError("UNEXPECTED_UTF8_BOM")
    for token in TOKENS.values():
        if token.encode("utf-8") not in encoded:
            raise RuntimeError(f"IDENTIFIER_BYTE_MISMATCH: {token}")
    return encoded


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while view:
        written = os.write(fd, view)
        if written <= 0:
            raise OSError("SHORT_WRITE")
        view = view[written:]


def create_manifest(root: Path, target: str, run_id: str) -> str:
    """Atomically create one manifest, refusing symlinks and existing destinations.

    Operations inside manifests/ are relative to its opened directory descriptor.
    If an error happens after the no-clobber link succeeds, publication is reported
    as uncertain rather than falsely claiming rollback.
    """
    validate_target(target)
    validate_run_id(run_id)
    content = build_manifest(target, run_id)
    directory_flags, file_flags = _required_flags()
    filename = f"INVESTIGATION_AGENT_{target}_{run_id}.yaml"
    root_fd = -1
    manifests_fd = -1
    temp_name = f".tmp-{secrets.token_hex(16)}"
    temp_exists = False
    published = False

    try:
        # Fail closed if the supplied repository root itself is a symlink.
        root_fd = os.open(os.fspath(root), directory_flags)
        try:
            os.mkdir("manifests", mode=0o755, dir_fd=root_fd)
            os.fsync(root_fd)
        except FileExistsError:
            pass
        manifests_fd = os.open("manifests", directory_flags, dir_fd=root_fd)

        temp_fd = os.open(temp_name, file_flags, 0o644, dir_fd=manifests_fd)
        temp_exists = True
        try:
            _write_all(temp_fd, content)
            os.fsync(temp_fd)
        finally:
            os.close(temp_fd)

        # link is atomic and no-clobber; a destination symlink/file is not followed or replaced.
        os.link(
            temp_name,
            filename,
            src_dir_fd=manifests_fd,
            dst_dir_fd=manifests_fd,
            follow_symlinks=False,
        )
        published = True
        os.unlink(temp_name, dir_fd=manifests_fd)
        temp_exists = False
        os.fsync(manifests_fd)

    except Exception as exc:
        cleanup_error = None
        if temp_exists and manifests_fd >= 0:
            try:
                os.unlink(temp_name, dir_fd=manifests_fd)
                temp_exists = False
            except FileNotFoundError:
                temp_exists = False
            except OSError as cleanup_exc:
                cleanup_error = cleanup_exc
        if published:
            detail = f"publication may have occurred: {exc}"
            if cleanup_error:
                detail += f"; temporary cleanup failed: {cleanup_error}"
            raise PublicationError("PUBLICATION_STATUS_UNKNOWN", detail) from exc
        if cleanup_error:
            raise PublicationError("ROLLBACK_INCOMPLETE", f"{exc}; temporary cleanup failed: {cleanup_error}") from exc
        raise
    finally:
        if manifests_fd >= 0:
            os.close(manifests_fd)
        if root_fd >= 0:
            os.close(root_fd)

    return f"manifests/{filename}"


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: ti_ula_manifest.py TARGET RUN_ID REPOSITORY_ROOT", file=sys.stderr)
        return 2
    try:
        print(create_manifest(Path(sys.argv[3]), sys.argv[1], sys.argv[2]))
    except PublicationError as exc:
        print(f"{exc.status}: {exc}", file=sys.stderr)
        return 1
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"NOT_PUBLISHED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

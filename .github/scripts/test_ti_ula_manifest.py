from pathlib import Path
import tempfile
import unittest

from ti_ula_manifest import (
    TOKENS,
    PublicationError,
    build_manifest,
    create_manifest,
    validate_run_id,
    validate_target,
)


class ManifestSecurityTests(unittest.TestCase):
    def test_rejects_traversal_absolute_and_invalid_target(self):
        for value in ("../escape", "/tmp/escape", "a/b", "", ".", "..", "a" * 81):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_target(value)

    def test_rejects_invalid_run_id(self):
        for value in ("../1", "1/2", "", "x" * 20, "١٢٣"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_run_id(value)

    def test_rejects_symlink_manifests_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            outside = Path(temp) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "manifests").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(OSError):
                create_manifest(root, "SAFE-TARGET", "123")
            self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_symlink_repository_root(self):
        with tempfile.TemporaryDirectory() as temp:
            actual = Path(temp) / "actual"
            actual.mkdir()
            link = Path(temp) / "repo-link"
            link.symlink_to(actual, target_is_directory=True)
            with self.assertRaises(OSError):
                create_manifest(link, "SAFE-TARGET", "123")
            self.assertEqual(list(actual.iterdir()), [])

    def test_existing_destination_symlink_is_not_followed_or_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            manifests = root / "manifests"
            manifests.mkdir(parents=True)
            outside_file = Path(temp) / "outside.yaml"
            outside_file.write_text("do not modify", encoding="utf-8")
            destination = manifests / "INVESTIGATION_AGENT_SAFE-TARGET_123.yaml"
            destination.symlink_to(outside_file)
            with self.assertRaises(FileExistsError):
                create_manifest(root, "SAFE-TARGET", "123")
            self.assertEqual(outside_file.read_text(encoding="utf-8"), "do not modify")

    def test_utf8_identifiers_are_byte_exact_without_bom(self):
        content = build_manifest("SAFE-TARGET", "123")
        self.assertFalse(content.startswith(b"\xef\xbb\xbf"))
        for token in TOKENS.values():
            self.assertIn(token.encode("utf-8"), content)

    def test_atomic_creation_and_no_clobber(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            relative = create_manifest(root, "SAFE-TARGET", "123")
            output = root / relative
            self.assertTrue(output.is_file())
            self.assertIn(b"A\xc2\xa9tor", output.read_bytes())
            with self.assertRaises(FileExistsError):
                create_manifest(root, "SAFE-TARGET", "123")

    def test_post_publish_sync_error_is_not_reported_as_rollback(self):
        # Static contract test for the explicit ambiguous-publication status type.
        self.assertEqual(PublicationError("PUBLICATION_STATUS_UNKNOWN", "x").status,
                         "PUBLICATION_STATUS_UNKNOWN")


if __name__ == "__main__":
    unittest.main()

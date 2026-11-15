import os
from pathlib import Path
import tempfile
import unittest

from ti_ula_manifest import TOKENS, build_manifest, create_manifest, validate_target


class ManifestSecurityTests(unittest.TestCase):
    def test_rejects_traversal_absolute_and_invalid_names(self):
        for value in ("../escape", "/tmp/escape", "a/b", "", ".", "..", "a" * 81):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_target(value)

    def test_rejects_manifests_directory_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            outside = Path(temp) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "manifests").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(OSError):
                create_manifest(root, "SAFE-TARGET", "123")
            self.assertEqual(list(outside.iterdir()), [])

    def test_existing_destination_symlink_is_not_followed_or_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            manifests = root / "manifests"
            manifests.mkdir()
            outside_file = Path(temp) / "outside.yaml"
            outside_file.write_text("do not modify", encoding="utf-8")
            destination = manifests / "INVESTIGATION_AGENT_SAFE-TARGET_123.yaml"
            destination.symlink_to(outside_file)
            with self.assertRaises(FileExistsError):
                create_manifest(root, "SAFE-TARGET", "123")
            self.assertEqual(outside_file.read_text(encoding="utf-8"), "do not modify")

    def test_utf8_identifiers_are_byte_exact_and_without_bom(self):
        content = build_manifest("SAFE-TARGET", "123")
        self.assertFalse(content.startswith(b"\xef\xbb\xbf"))
        for token in TOKENS.values():
            self.assertIn(token.encode("utf-8"), content)

    def test_complete_file_is_published_and_existing_file_is_not_clobbered(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            relative = create_manifest(root, "SAFE-TARGET", "123")
            path = root / relative
            self.assertTrue(path.is_file())
            self.assertIn(b"A\xc2\xa9tor", path.read_bytes())
            with self.assertRaises(FileExistsError):
                create_manifest(root, "SAFE-TARGET", "123")


if __name__ == "__main__":
    unittest.main()

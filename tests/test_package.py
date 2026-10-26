import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts.validate_package import validate_repository, validate_skill


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_repository_is_ready_for_distribution(self):
        self.assertEqual([], validate_repository(ROOT))

    def test_each_skill_works_as_an_independent_copy(self):
        with tempfile.TemporaryDirectory(prefix="skill package ") as temporary:
            for name in ("design", "qa"):
                with self.subTest(skill=name):
                    target = Path(temporary) / "日本語 path" / name
                    shutil.copytree(ROOT / "skills" / name, target)
                    self.assertEqual([], validate_skill(target))

    def test_cli_can_run_outside_the_repository_without_optional_commands(self):
        with tempfile.TemporaryDirectory(prefix="skill cli ") as temporary:
            result = subprocess.run(
                [sys.executable, "-I", str(ROOT / "scripts" / "validate_package.py"), str(ROOT)],
                cwd=temporary,
                env={**os.environ, "PATH": ""},
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


class InvalidPackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill validation ")
        self.addCleanup(self.temporary.cleanup)
        self.skill = Path(self.temporary.name) / "example"
        self.skill.mkdir()
        self.entrypoint = self.skill / "SKILL.md"
        self.write_skill()

    def write_skill(self, name="example", description="Verify software changes.", body="# Example\n"):
        self.entrypoint.write_text(
            f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n{body}",
            encoding="utf-8",
            newline="\n",
        )

    def test_valid_utf8_and_crlf_are_accepted(self):
        self.write_skill(description="日本語の説明。")
        self.entrypoint.write_bytes(self.entrypoint.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual([], validate_skill(self.skill))

    def test_missing_entrypoint_is_rejected(self):
        self.entrypoint.unlink()
        self.assertTrue(validate_skill(self.skill))

    def test_invalid_or_mismatched_names_are_rejected(self):
        for name in ("Other", "-example", "example--name", "other", "x" * 65):
            with self.subTest(name=name):
                self.write_skill(name=name)
                self.assertTrue(validate_skill(self.skill))

    def test_empty_or_unfinished_description_is_rejected(self):
        for description in ("", "   ", "[TODO: describe this skill]", "x" * 1025):
            with self.subTest(description=description[:30]):
                self.write_skill(description=description)
                self.assertTrue(validate_skill(self.skill))

    def test_invalid_frontmatter_is_rejected(self):
        for content in ("# No metadata\n", "---\nname: example\n---\n", "---\nname: example\ndescription: [broken\n---\n"):
            with self.subTest(content=content):
                self.entrypoint.write_text(content, encoding="utf-8")
                self.assertTrue(validate_skill(self.skill))

    def test_broken_links_and_links_outside_the_skill_are_rejected(self):
        outside = self.skill.parent / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        for link in ("missing.md", "<missing with spaces.md>", "../outside.md", "https-not-a-scheme:missing"):
            with self.subTest(link=link):
                self.write_skill(body=f"[reference]({link})\n")
                self.assertTrue(validate_skill(self.skill))

    def test_reference_links_are_checked_recursively(self):
        references = self.skill / "references"
        references.mkdir()
        self.write_skill(body="[details](references/details.md)\n")
        (references / "details.md").write_text("[missing](missing.md)\n", encoding="utf-8")
        self.assertTrue(validate_skill(self.skill))

    def test_existing_relative_and_web_links_are_accepted(self):
        reference = self.skill / "extra notes.md"
        reference.write_text("# Details\n", encoding="utf-8")
        self.write_skill(body="[local](extra%20notes.md#details)\n[web](https://example.com/docs)\n")
        self.assertEqual([], validate_skill(self.skill))

    def test_encoded_delimiters_and_angle_bracket_paths_resolve(self):
        for filename, link in (("guide#details.md", "guide%23details.md"), ("extra notes.md", "<extra notes.md>")):
            with self.subTest(link=link):
                (self.skill / filename).write_text("# Details\n", encoding="utf-8")
                self.write_skill(body=f"[details]({link})\n")
                self.assertEqual([], validate_skill(self.skill))

    def test_malformed_urls_return_validation_errors(self):
        self.write_skill(body="[broken](https://[invalid)\n")
        self.assertTrue(validate_skill(self.skill))

    def test_backslash_links_are_rejected_even_on_windows(self):
        folder = self.skill / "references"
        folder.mkdir()
        (folder / "details.md").write_text("# Details\n", encoding="utf-8")
        self.write_skill(body="[details](references\\details.md)\n")
        self.assertTrue(validate_skill(self.skill))

    def test_local_absolute_paths_are_rejected(self):
        for path in ("C:\\Users\\someone\\secret.txt", "/Users/someone/file", "/home/someone/file", "\\\\server\\share\\file"):
            with self.subTest(path=path):
                self.write_skill(body=f"Use `{path}`.\n")
                self.assertTrue(validate_skill(self.skill))

    def test_non_utf8_and_bom_are_rejected_for_new_packages(self):
        for content in (b"\xff\xfeinvalid", b"\xef\xbb\xbf---\nname: example\n---\n"):
            with self.subTest(content=content):
                self.entrypoint.write_bytes(content)
                self.assertTrue(validate_skill(self.skill))


if __name__ == "__main__":
    unittest.main()

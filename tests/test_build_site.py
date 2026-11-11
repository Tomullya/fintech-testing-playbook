"""Site source generator (scripts/build_site.py): pages per language and rewritten links."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_site import EN_URL, REPO_URL, RU_URL, build, rewrite  # noqa: E402


class Rewrite(unittest.TestCase):
    def test_link_between_areas(self):
        self.assertEqual(
            rewrite("see [x](../02-accounting/en.md#rounding)", "areas/01-card-payment/en.md", "en"),
            "see [x](02-accounting.md#rounding)",
        )

    def test_readme_area_link(self):
        self.assertEqual(rewrite("[a](areas/03-money/ru.md)", "README.ru.md", "ru"), "[a](03-money.md)")

    def test_language_switch_goes_to_other_site(self):
        self.assertEqual(rewrite("[ru](README.ru.md)", "README.md", "en"), f"[ru]({RU_URL})")
        self.assertEqual(rewrite("[en](glossary.md)", "glossary.ru.md", "ru"), f"[en]({EN_URL}glossary/)")

    def test_same_language_glossary(self):
        self.assertEqual(rewrite("[g](glossary.ru.md)", "README.ru.md", "ru"), "[g](glossary.md)")

    def test_terminology_report(self):
        self.assertEqual(
            rewrite("[r](docs/ru-terminology-check.md)", "README.md", "en"), "[r](ru-terminology-check.md)"
        )

    def test_other_repo_file_goes_to_github(self):
        self.assertEqual(
            rewrite("[s](scripts/check_playbook.py)", "README.md", "en"),
            f"[s]({REPO_URL}/blob/main/scripts/check_playbook.py)",
        )

    def test_web_links_and_code_untouched(self):
        text = "[w](https://example.org/a.md) `[c](../02-accounting/en.md)`\n```\n[d](README.md)\n```"
        self.assertEqual(rewrite(text, "areas/01-card-payment/en.md", "en"), text)


class Build(unittest.TestCase):
    def test_build_creates_pages_per_language(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build(root, out)
            for lang in ("en", "ru"):
                names = {p.name for p in (out / lang).glob("*.md")}
                self.assertIn("index.md", names)
                self.assertIn("glossary.md", names)
                self.assertIn("01-card-payment.md", names)
                self.assertIn("10-interview-questions.md", names)
            self.assertNotIn("](../", (out / "en" / "03-money.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

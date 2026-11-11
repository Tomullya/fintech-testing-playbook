"""Website builder (scripts/build_site.py): pages per language, rewritten links, anchors that exist."""

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_site import REPO_URL, build, rewrite_link  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class Links(unittest.TestCase):
    def test_area_link_becomes_route(self):
        self.assertEqual(rewrite_link("../02-accounting/en.md#rounding", "areas/03-money/en.md"), "#/02-accounting/rounding")

    def test_readme_area_link(self):
        self.assertEqual(rewrite_link("areas/03-money/ru.md", "README.ru.md"), "#/03-money")

    def test_glossary_and_readme_links(self):
        self.assertEqual(rewrite_link("glossary.ru.md", "README.ru.md"), "#/glossary")
        self.assertEqual(rewrite_link("README.md", "glossary.md"), "#/")

    def test_other_repo_file_goes_to_github(self):
        self.assertEqual(
            rewrite_link("docs/ru-terminology-check.md", "README.md"), f"{REPO_URL}/blob/main/docs/ru-terminology-check.md"
        )

    def test_web_and_anchor_links_untouched(self):
        self.assertEqual(rewrite_link("https://example.org/x.md", "README.md"), "https://example.org/x.md")


class Build(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        build(ROOT, cls.out)
        cls.index = json.loads((cls.out / "data" / "pages.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_ten_areas_and_glossary_in_both_languages(self):
        ids = [p["id"] for p in self.index["pages"]]
        self.assertEqual(len([i for i in ids if re.match(r"\d\d-", i)]), 10)
        self.assertIn("glossary", ids)
        self.assertNotIn("ru-terminology-check", ids)
        for page in self.index["pages"]:
            for lang in ("en", "ru"):
                self.assertTrue(page["title"][lang])
                self.assertTrue((self.out / "data" / lang / f"{page['id']}.html").exists())

    def test_home_has_cards_and_no_badges(self):
        for lang in ("en", "ru"):
            home = (self.out / "data" / lang / "home.html").read_text(encoding="utf-8")
            self.assertNotIn("badge.svg", home)
            self.assertEqual(home.count('class="card"'), 10)

    def test_every_internal_link_points_to_an_existing_page_and_anchor(self):
        ids = {}
        for lang in ("en", "ru"):
            for f in (self.out / "data" / lang).glob("*.html"):
                ids[(lang, f.stem)] = set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8")))
        for lang in ("en", "ru"):
            for f in (self.out / "data" / lang).glob("*.html"):
                html = f.read_text(encoding="utf-8")
                self.assertNotRegex(html, r'href="[^"#:]+\.md', f"{lang}/{f.name}: .md link left")
                for page, anchor in re.findall(r'href="#/([^"/]*)/?([^"]*)"', html):
                    page = page or "home"
                    self.assertIn((lang, page), ids, f"{lang}/{f.name}: no page {page}")
                    if anchor:
                        from urllib.parse import unquote

                        self.assertIn(unquote(anchor), ids[(lang, page)], f"{lang}/{f.name}: no anchor {anchor} in {page}")

    def test_mermaid_kept_for_the_browser(self):
        html = (self.out / "data" / "en" / "01-card-payment.html").read_text(encoding="utf-8")
        self.assertIn('class="mermaid"', html)

    def test_static_files_copied(self):
        for name in ("index.html", "css/site.css", "js/app.js", "js/routes.js"):
            self.assertTrue((self.out / name).exists(), name)
        self.assertFalse((self.out / "tests").exists())


if __name__ == "__main__":
    unittest.main()

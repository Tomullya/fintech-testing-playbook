"""Structure checks of the playbook (scripts/check_playbook.py)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_playbook import EN_HEADINGS, RU_HEADINGS, check  # noqa: E402

LINKS = "\n".join(f"- [Source {i}](https://example.org/{i})" for i in range(3))


def page(headings, mermaid=True, extra=""):
    parts = ["# Title", "", "Intro."]
    for h in headings:
        parts += ["", f"## {h}", "", "Text."]
        if h in ("How it works", "Как это работает") and mermaid:
            parts += ["", "```mermaid", "graph LR; A-->B", "```"]
    parts += ["", LINKS, extra]
    return "\n".join(parts)


class PlaybookCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.areas = []

    def tearDown(self):
        self.tmp.cleanup()

    def area(self, slug, en=None, ru=None):
        d = self.root / "areas" / slug
        d.mkdir(parents=True)
        if en is not False:
            (d / "en.md").write_text(en if en is not None else page(EN_HEADINGS), encoding="utf-8")
        if ru is not False:
            (d / "ru.md").write_text(ru if ru is not None else page(RU_HEADINGS), encoding="utf-8")
        self.areas.append(slug)

    def readmes(self, skip=()):
        listed = [s for s in self.areas if s not in skip]
        (self.root / "README.md").write_text(
            "\n".join(f"- [x](areas/{s}/en.md)" for s in listed), encoding="utf-8"
        )
        (self.root / "README.ru.md").write_text(
            "\n".join(f"- [x](areas/{s}/ru.md)" for s in listed), encoding="utf-8"
        )

    def test_valid_area_passes(self):
        self.area("01-card-payment")
        self.readmes()
        self.assertEqual(check(self.root), [])

    def test_missing_ru_file_fails(self):
        self.area("01-card-payment", ru=False)
        self.readmes()
        self.assertTrue(any("ru.md" in p for p in check(self.root)))

    def test_missing_heading_in_ru_fails(self):
        self.area("01-card-payment", ru=page(RU_HEADINGS[:4] + RU_HEADINGS[5:]))
        self.readmes()
        self.assertTrue(any("Типичные дефекты" in p for p in check(self.root)))

    def test_heading_order_enforced(self):
        swapped = list(EN_HEADINGS)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        self.area("01-card-payment", en=page(swapped))
        self.readmes()
        self.assertTrue(any("order" in p for p in check(self.root)))

    def test_mermaid_required_for_01_to_08(self):
        self.area("03-money", en=page(EN_HEADINGS, mermaid=False))
        self.area("09-test-data", en=page(EN_HEADINGS, mermaid=False), ru=page(RU_HEADINGS, mermaid=False))
        self.readmes()
        problems = check(self.root)
        self.assertTrue(any("03-money" in p and "mermaid" in p for p in problems))
        self.assertFalse(any("09-test-data" in p for p in problems))

    def test_area_10_uses_questions_template(self):
        self.area(
            "10-interview-questions",
            en=page(["Questions", "Sources"], mermaid=False),
            ru=page(["Вопросы", "Источники"], mermaid=False),
        )
        self.readmes()
        self.assertEqual(check(self.root), [])

    def test_three_source_links_required(self):
        text = page(EN_HEADINGS).replace(LINKS, "- [one](https://example.org/1)")
        self.area("01-card-payment", en=text)
        self.readmes()
        self.assertTrue(any("Sources" in p and "3" in p for p in check(self.root)))

    def test_broken_relative_link_fails(self):
        self.area("01-card-payment", en=page(EN_HEADINGS, extra="See [area 2](../02-accounting/en.md)."))
        self.readmes()
        self.assertTrue(any("02-accounting/en.md" in p for p in check(self.root)))

    def test_area_missing_from_readme_fails(self):
        self.area("01-card-payment")
        self.area("02-accounting")
        self.readmes(skip=("02-accounting",))
        problems = check(self.root)
        self.assertTrue(any("README.md" in p and "02-accounting" in p for p in problems))
        self.assertTrue(any("README.ru.md" in p and "02-accounting" in p for p in problems))


if __name__ == "__main__":
    unittest.main()

"""Structure check of the playbook. Standard library only.

Every area folder areas/NN-<slug>/ has en.md and ru.md with the same template headings in
order, a Mermaid diagram (areas 01-08), at least 3 web links under Sources, working relative
links, and is listed in README.md / README.ru.md.

Usage: python3 scripts/check_playbook.py   (exit code 1 if there are problems)
"""

import re
import sys
from pathlib import Path

EN_HEADINGS = [
    "How it works",
    "Participants and money flows",
    "Business risks",
    "What to test",
    "Typical defects",
    "In card-wallet",
    "Sources",
]
RU_HEADINGS = [
    "Как это работает",
    "Участники и потоки денег",
    "Бизнес-риски",
    "Что тестировать",
    "Типичные дефекты",
    "В card-wallet",
    "Источники",
]
QA_HEADINGS = {"en": ["Questions", "Sources"], "ru": ["Вопросы", "Источники"]}
MERMAID_AREAS = {f"{n:02d}" for n in range(1, 9)}
LINK = re.compile(r"\]\(([^)\s]+)\)")


def strip_code(text: str) -> str:
    """Text without fenced code blocks (their lines are not headings or links)."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def headings(text: str) -> list[str]:
    return [line[3:].strip() for line in strip_code(text).splitlines() if line.startswith("## ")]


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", strip_code(text), flags=re.M | re.S)
    return m.group(1) if m else ""


def expected(area: str, lang: str) -> list[str]:
    if area.startswith("10-"):
        return QA_HEADINGS[lang]
    return EN_HEADINGS if lang == "en" else RU_HEADINGS


def check_page(root: Path, area: str, lang: str) -> list[str]:
    path = root / "areas" / area / f"{lang}.md"
    name = f"areas/{area}/{lang}.md"
    if not path.exists():
        return [f"{name}: file missing"]
    text = path.read_text(encoding="utf-8")
    want, got = expected(area, lang), headings(text)
    problems = [f"{name}: missing section '{h}'" for h in want if h not in got]
    if not problems and [h for h in got if h in want] != want:
        problems.append(f"{name}: sections are out of order (expected {want})")
    if area[:2] in MERMAID_AREAS and "```mermaid" not in text:
        problems.append(f"{name}: needs a mermaid diagram")
    sources = want[-1]
    links = re.findall(r"https?://", section(text, sources))
    if len(links) < 3:
        problems.append(f"{name}: {sources} needs at least 3 web links (has {len(links)})")
    return problems


def check_links(root: Path) -> list[str]:
    problems = []
    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts or ".superpowers" in md.parts:
            continue
        for target in LINK.findall(strip_code(md.read_text(encoding="utf-8"))):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            file_part = target.split("#")[0]
            if file_part and not (md.parent / file_part).resolve().exists():
                problems.append(f"{md.relative_to(root)}: broken link {target}")
    return problems


def check(root: Path) -> list[str]:
    areas_dir = root / "areas"
    areas = sorted(p.name for p in areas_dir.iterdir() if p.is_dir()) if areas_dir.exists() else []
    problems = []
    for area in areas:
        for lang in ("en", "ru"):
            problems += check_page(root, area, lang)
    for readme, lang in (("README.md", "en"), ("README.ru.md", "ru")):
        path = root / readme
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        for area in areas:
            if f"areas/{area}/{lang}.md" not in text:
                problems.append(f"{readme}: area {area} is not listed")
    return problems + check_links(root)


def main() -> int:
    problems = check(Path(__file__).resolve().parents[1])
    print("\n".join(problems) if problems else "Playbook check: OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

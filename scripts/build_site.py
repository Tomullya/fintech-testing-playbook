"""Build the MkDocs sources of the website from the playbook files. Standard library only.

Every page gets one file per language:
  README.md / README.ru.md          -> <lang>/index.md
  glossary.md / glossary.ru.md      -> <lang>/glossary.md
  areas/NN-<slug>/<lang>.md         -> <lang>/NN-<slug>.md
  docs/ru-terminology-check.md      -> <lang>/ru-terminology-check.md
Links are rewritten for the site: links between pages of the same language stay relative,
links to the other language go to the other site, other repository files go to GitHub.

Usage: python3 scripts/build_site.py build/site_src
"""

import re
import shutil
import sys
from pathlib import Path, PurePosixPath

REPO_URL = "https://github.com/Tomullya/fintech-testing-playbook"
EN_URL = "https://tomullya.github.io/fintech-testing-playbook/"
RU_URL = EN_URL + "ru/"
SITE_URL = {"en": EN_URL, "ru": RU_URL}
LINK = re.compile(r"\]\(([^)\s]+)\)")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def page_of(path: str):
    """Repository file → (language, site page name), or None if it is not a site page."""
    p = PurePosixPath(path)
    if p.name in ("README.md", "README.ru.md") and len(p.parts) == 1:
        return ("ru" if p.name == "README.ru.md" else "en"), "index.md"
    if p.name in ("glossary.md", "glossary.ru.md") and len(p.parts) == 1:
        return ("ru" if p.name == "glossary.ru.md" else "en"), "glossary.md"
    if len(p.parts) == 3 and p.parts[0] == "areas" and p.name in ("en.md", "ru.md"):
        return p.stem, f"{p.parts[1]}.md"
    if str(p) == "docs/ru-terminology-check.md":
        return None, "ru-terminology-check.md"
    return None


def site_url(page: str) -> str:
    return "" if page == "index.md" else page[:-3] + "/"


def rewrite_link(target: str, source: str, lang: str) -> str:
    if re.match(r"^(https?:|mailto:|#)", target):
        return target
    path, _, anchor = target.partition("#")
    resolved = str(PurePosixPath(*_normalise(PurePosixPath(source).parent / path)))
    anchor = f"#{anchor}" if anchor else ""
    page = page_of(resolved)
    if page is None:
        return f"{REPO_URL}/blob/main/{resolved}{anchor}"
    page_lang, name = page
    if page_lang in (None, lang):
        return f"{name}{anchor}"
    return f"{SITE_URL[page_lang]}{site_url(name)}{anchor}"


def _normalise(p: PurePosixPath) -> list[str]:
    parts: list[str] = []
    for part in p.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part not in (".", ""):
            parts.append(part)
    return parts


def rewrite(text: str, source: str, lang: str) -> str:
    """Rewrite markdown links outside code; source is the repository path of the file."""
    out, last = [], 0
    for m in CODE.finditer(text):
        out.append(LINK.sub(lambda l: f"]({rewrite_link(l.group(1), source, lang)})", text[last : m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(LINK.sub(lambda l: f"]({rewrite_link(l.group(1), source, lang)})", text[last:]))
    return "".join(out)


def build(root: Path, out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    sources = {
        "en": {"README.md": "index.md", "glossary.md": "glossary.md"},
        "ru": {"README.ru.md": "index.md", "glossary.ru.md": "glossary.md"},
    }
    for area in sorted(p for p in (root / "areas").iterdir() if p.is_dir()):
        for lang in ("en", "ru"):
            sources[lang][f"areas/{area.name}/{lang}.md"] = f"{area.name}.md"
    for lang in ("en", "ru"):
        sources[lang]["docs/ru-terminology-check.md"] = "ru-terminology-check.md"
        (out / lang).mkdir(parents=True)
        for src, dst in sources[lang].items():
            text = (root / src).read_text(encoding="utf-8")
            (out / lang / dst).write_text(rewrite(text, src, lang), encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    build(root, Path(sys.argv[1]) if len(sys.argv) > 1 else root / "build" / "site_src")
    print("site sources written")

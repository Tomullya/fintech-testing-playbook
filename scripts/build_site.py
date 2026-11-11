"""Build the website (build/site) from the playbook Markdown.

Pages: home (README), the 10 areas, glossary — each in EN and RU. Markdown is converted to HTML
fragments in data/<lang>/<page>.html; data/pages.json holds titles, card texts and the table of
contents. The static shell (web/) is copied next to it. Links between pages become routes
(#/<page>/<anchor>); other repository files link to GitHub.

Usage: python3 scripts/build_site.py [out_dir]     (needs requirements-site.txt)
"""

import html
import json
import re
import shutil
import sys
from pathlib import Path, PurePosixPath

import markdown
from pymdownx.slugs import slugify
from pymdownx.superfences import fence_div_format

REPO_URL = "https://github.com/Tomullya/fintech-testing-playbook"
LINK = re.compile(r"\]\(([^)\s]+)\)")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
LANGS = ("en", "ru")


def _normalise(p: PurePosixPath) -> str:
    parts: list[str] = []
    for part in p.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part not in (".", ""):
            parts.append(part)
    return "/".join(parts)


def page_id(path: str):
    """Repository path → site page id, or None if it is not a page of the site."""
    p = PurePosixPath(path)
    if str(p) in ("README.md", "README.ru.md"):
        return ""
    if str(p) in ("glossary.md", "glossary.ru.md"):
        return "glossary"
    if len(p.parts) == 3 and p.parts[0] == "areas" and p.name in ("en.md", "ru.md"):
        return p.parts[1]
    return None


def rewrite_link(target: str, source: str) -> str:
    if re.match(r"^(https?:|mailto:|#)", target):
        return target
    path, _, anchor = target.partition("#")
    resolved = _normalise(PurePosixPath(source).parent / path)
    page = page_id(resolved)
    if page is None:
        return f"{REPO_URL}/blob/main/{resolved}" + (f"#{anchor}" if anchor else "")
    return f"#/{page}" + (f"/{anchor}" if anchor else "")


def rewrite(text: str, source: str) -> str:
    out, last = [], 0
    sub = lambda chunk: LINK.sub(lambda m: f"]({rewrite_link(m.group(1), source)})", chunk)  # noqa: E731
    for m in CODE.finditer(text):
        out += [sub(text[last : m.start()]), m.group(0)]
        last = m.end()
    out.append(sub(text[last:]))
    return "".join(out)


def to_html(text: str) -> str:
    md = markdown.Markdown(
        extensions=["tables", "toc", "attr_list", "admonition", "pymdownx.superfences", "pymdownx.tasklist"],
        extension_configs={
            "toc": {"slugify": slugify(case="lower")},
            "pymdownx.superfences": {
                "custom_fences": [{"name": "mermaid", "class": "mermaid", "format": fence_div_format}]
            },
            "pymdownx.tasklist": {"custom_checkbox": True},
        },
    )
    return md.convert(text)


def split_title(text: str) -> tuple[str, str]:
    """('# Title' line, rest of the page)."""
    lines = text.splitlines()
    i = next(n for n, line in enumerate(lines) if line.startswith("# "))
    return lines[i][2:].strip(), "\n".join(lines[i + 1 :])


def toc_of(fragment: str) -> list[dict]:
    return [
        {"level": int(level), "id": anchor, "text": html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()}
        for level, anchor, inner in re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', fragment)
    ]


def home(text: str, lang: str) -> tuple[str, list[dict]]:
    """Home fragment: intro, area cards from the README table, then the remaining sections."""
    _, body = split_title(text)
    body = "\n".join(line for line in body.splitlines() if "badge.svg" not in line)
    head, _, rest = body.partition("\n## ")
    table_heading, _, after = rest.partition("\n")
    rows = re.findall(r"^\| (\d\d) \| \[([^\]]+)\]\(([^)]+)\)([^|]*)\|", after, re.M)
    after = re.sub(r"^\|.*\|\s*$\n?", "", after, flags=re.M)
    cards = []
    for num, text, link, tail in rows:
        route = rewrite_link(link, "README.md" if lang == "en" else "README.ru.md")
        title, _, inner = text.partition(":")
        desc = tail.strip().lstrip(":").strip().strip("()") or inner.strip()
        cards.append({"num": num, "title": title.strip(), "desc": desc, "href": route})
    grid = "".join(
        f'<a class="card" href="{c["href"]}"><span class="card__num">{c["num"]}</span>'
        f'<span class="card__title">{html.escape(c["title"])}</span>'
        f'<span class="card__desc">{html.escape(c["desc"])}</span></a>'
        for c in cards
    )
    fragment = (
        to_html(rewrite(head, "README.md"))
        + f'<h2 id="areas">{html.escape(table_heading.strip())}</h2><div class="cards">{grid}</div>'
        + to_html(rewrite(after, "README.md"))
    )
    return fragment, cards


def build(root: Path, out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(root / "web", out, ignore=shutil.ignore_patterns("tests"))
    areas = sorted(p.name for p in (root / "areas").iterdir() if p.is_dir())
    pages = {"home": {"id": "home", "title": {}, "toc": {}}}
    for a in areas:
        pages[a] = {"id": a, "num": a[:2], "title": {}, "desc": {}, "toc": {}}
    pages["glossary"] = {"id": "glossary", "title": {}, "toc": {}}
    for lang in LANGS:
        (out / "data" / lang).mkdir(parents=True)
        readme = "README.md" if lang == "en" else "README.ru.md"
        text = (root / readme).read_text(encoding="utf-8")
        title, _ = split_title(text)
        fragment, cards = home(text, lang)
        pages["home"]["title"][lang] = re.sub(r"^\W+\s*", "", title)
        (out / "data" / lang / "home.html").write_text(fragment, encoding="utf-8")
        for c in cards:
            pid = c["href"][2:].split("/")[0]
            pages[pid]["desc"][lang] = c["desc"]
            pages[pid].setdefault("short", {})[lang] = c["title"]
        sources = {"glossary": "glossary.md" if lang == "en" else "glossary.ru.md"}
        sources.update({a: f"areas/{a}/{lang}.md" for a in areas})
        for pid, src in sources.items():
            title, body = split_title((root / src).read_text(encoding="utf-8"))
            fragment = to_html(rewrite(body, src))
            pages[pid]["title"][lang] = title
            pages[pid]["toc"][lang] = toc_of(fragment)
            (out / "data" / lang / f"{pid}.html").write_text(fragment, encoding="utf-8")
    (out / "data" / "pages.json").write_text(
        json.dumps({"pages": list(pages.values())}, ensure_ascii=False, indent=1), encoding="utf-8"
    )


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "build" / "site"
    build(root, target)
    print(f"site written to {target}")

// Fintech Testing Playbook site: menu, RU/EN switch on the same page, theme, table of contents,
// glossary search, Mermaid diagrams. Content comes from data/ (built by scripts/build_site.py).

import { href, parse } from "./routes.js";

const UI = {
  ru: {
    skip: "Перейти к тексту",
    tagline: "Как устроены финтех-процессы и как их тестировать",
    language: "Язык",
    theme: "Тема",
    menu: "Области",
    toc: "На этой странице",
    tocLabel: "На этой странице",
    home: "Главная",
    glossary: "Словарь",
    area: "Область {n}",
    repo: "Репозиторий на GitHub",
    wallet: "Проект card-wallet",
    search: "Найти термин на русском или английском",
    nothing: "Ничего не найдено. Попробуйте часть слова.",
    footer: "Справочник не является юридической консультацией. Источники указаны в конце каждой области.",
    error: "Не удалось загрузить страницу. Обновите страницу или проверьте соединение.",
  },
  en: {
    skip: "Skip to content",
    tagline: "How fintech business processes work and how to test them",
    language: "Language",
    theme: "Theme",
    menu: "Areas",
    toc: "On this page",
    tocLabel: "On this page",
    home: "Home",
    glossary: "Glossary",
    area: "Area {n}",
    repo: "Repository on GitHub",
    wallet: "The card-wallet project",
    search: "Find a term in English or Russian",
    nothing: "Nothing found. Try part of a word.",
    footer: "This playbook is not legal advice. Sources are listed at the end of every area.",
    error: "The page could not be loaded. Reload the page or check the connection.",
  },
};

const $ = (id) => document.getElementById(id);
const cache = new Map();
let pages = [];
let lang = "ru";
let renderId = 0;
let mermaid = null;

function pref(name, fallback) {
  try {
    return window.localStorage.getItem(`playbook-${name}`) ?? fallback;
  } catch {
    return fallback;
  }
}

function setPref(name, value) {
  try {
    window.localStorage.setItem(`playbook-${name}`, value);
  } catch {
    /* storage blocked: the choice lasts for this visit only */
  }
}

const t = (key, vars = {}) => UI[lang][key].replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? "");
const byId = (id) => pages.find((p) => p.id === id);

function fragment(page) {
  const key = `${lang}/${page}`;
  if (!cache.has(key)) {
    cache.set(
      key,
      fetch(`data/${lang}/${page}.html`).then((r) => {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      }),
    );
  }
  return cache.get(key);
}

function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  Object.assign(node, props);
  node.append(...children.filter((c) => c !== null && c !== undefined));
  return node;
}

function renderStatic() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-ui]").forEach((n) => (n.textContent = t(n.dataset.ui)));
  document.querySelectorAll("[data-ui-aria]").forEach((n) => n.setAttribute("aria-label", t(n.dataset.uiAria)));
  document.querySelectorAll("[data-lang]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
  $("footer").textContent = t("footer");
}

function renderMenu(current) {
  const item = (p) => {
    const a = el("a", { href: href(p.id) });
    if (p.id === current) a.setAttribute("aria-current", "page");
    a.append(el("span", { className: "menu__num", textContent: p.num ?? "" }), el("span", { textContent: menuTitle(p) }));
    return el("li", {}, a);
  };
  const areas = pages.filter((p) => p.num);
  $("menu").replaceChildren(
    item(byId("home")),
    ...areas.map(item),
    el("li", { className: "menu__sep", ariaHidden: "true" }),
    item(byId("glossary")),
  );
}

function menuTitle(p) {
  if (p.id === "home") return t("home");
  if (p.id === "glossary") return t("glossary");
  return p.short?.[lang] ?? p.title[lang];
}

function renderToc(page) {
  const items = (page.toc?.[lang] ?? []).filter((h) => h.level <= 3);
  if (items.length < 3) return $("toc").replaceChildren();
  $("toc").replaceChildren(
    el("p", { className: "toc__label", textContent: t("tocLabel") }),
    el(
      "ol",
      {},
      ...items.map((h) =>
        el("li", { className: `toc__l${h.level}` }, el("a", { href: href(page.id, h.id), textContent: h.text })),
      ),
    ),
  );
}

function enhanceGlossary(container) {
  const table = container.querySelector("table");
  if (!table) return;
  const rows = [...table.querySelectorAll("tbody tr")];
  const empty = el("p", { className: "search__empty", textContent: t("nothing"), hidden: true });
  const input = el("input", { type: "search", className: "search", placeholder: t("search") });
  input.setAttribute("aria-label", t("search"));
  input.dataset.testid = "glossary-search";
  input.addEventListener("input", () => {
    const needle = input.value.trim().toLowerCase();
    let shown = 0;
    rows.forEach((r) => {
      r.hidden = Boolean(needle) && !r.textContent.toLowerCase().includes(needle);
      if (!r.hidden) shown += 1;
    });
    empty.hidden = shown > 0;
  });
  table.before(input, empty);
}

async function drawDiagrams(container) {
  const nodes = [...container.querySelectorAll(".mermaid")];
  if (!nodes.length) return;
  try {
    mermaid ??= (await import("https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs")).default;
    mermaid.initialize({ startOnLoad: false, theme: document.documentElement.dataset.theme === "dark" ? "dark" : "default" });
    await mermaid.run({ nodes });
  } catch {
    nodes.forEach((n) => n.removeAttribute("data-processed")); // leave the source text visible
    nodes.forEach((n) => (n.style.color = "inherit"));
  }
}

async function render({ keepScroll = false } = {}) {
  const id = ++renderId;
  const { page: pid, anchor } = parse(location.hash, pages.map((p) => p.id));
  const page = byId(pid);
  renderStatic();
  renderMenu(pid);
  $("kicker").textContent = page.num ? t("area", { n: page.num }) : "";
  $("title").textContent = pid === "home" ? page.title[lang] : page.title[lang];
  document.title = pid === "home" ? "Fintech Testing Playbook" : `${page.title[lang]} — Fintech Testing Playbook`;
  let html;
  try {
    html = await fragment(pid);
  } catch {
    html = `<p>${t("error")}</p>`;
  }
  if (id !== renderId) return; // a newer render started while loading
  const content = $("content");
  content.innerHTML = html;
  renderToc(page);
  if (pid === "glossary") enhanceGlossary(content);
  await drawDiagrams(content);
  if (id !== renderId) return;
  if (anchor) document.getElementById(anchor)?.scrollIntoView();
  else if (!keepScroll) window.scrollTo(0, 0);
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelector("[data-testid=theme-toggle]").setAttribute("aria-pressed", String(theme === "dark"));
}

async function start() {
  lang = pref("lang", navigator.language?.startsWith("ru") ? "ru" : "en");
  if (!UI[lang]) lang = "ru";
  applyTheme(pref("theme", window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  pages = (await fetch("data/pages.json").then((r) => r.json())).pages;
  document.querySelectorAll("[data-lang]").forEach((b) =>
    b.addEventListener("click", () => {
      lang = b.dataset.lang;
      setPref("lang", lang);
      render({ keepScroll: true });
    }),
  );
  document.querySelector("[data-testid=theme-toggle]").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    setPref("theme", next);
    applyTheme(next);
    render({ keepScroll: true });
  });
  document.querySelector(".skip").addEventListener("click", (e) => {
    e.preventDefault();
    $("main").focus();
  });
  window.addEventListener("hashchange", () => render());
  render();
}

start();

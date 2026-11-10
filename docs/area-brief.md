# Brief for writing an area

Read this whole file before writing. The spec is `docs/design/2026-11-10-playbook-design.md`.

## Reader
A QA engineer (Russian-speaking; worked as a manual tester on bank cards) who wants to understand
fintech processes deeply before interviews, and employers who read the English version. Write
plainly, concretely, without marketing words. Explain every term at first use. Prefer short
paragraphs, tables and lists.

## Files
`areas/NN-<slug>/en.md` and `areas/NN-<slug>/ru.md` — same content, same structure. Start each
with `# <Area title>` and a 2–3 sentence intro, then exactly these level-2 headings in this order
(the CI checker enforces them; do not add other `## ` headings — use `###` for sub-topics):

| EN | RU |
|---|---|
| How it works | Как это работает |
| Participants and money flows | Участники и потоки денег |
| Business risks | Бизнес-риски |
| What to test | Что тестировать |
| Typical defects | Типичные дефекты |
| In card-wallet | В card-wallet |
| Sources | Источники |

## What each section contains
1. **How it works** — the process step by step, at least one Mermaid diagram that GitHub renders
   (`sequenceDiagram` or `flowchart LR`; keep labels short; avoid quotes, parentheses and
   semicolons inside labels), and a worked example with real-looking numbers (EUR amounts,
   dates, times).
2. **Participants and money flows** — a table: participant → role → what they send/receive and
   when; say who carries the risk at each step.
3. **Business risks** — grouped: company (money loss, fines, scheme penalties), customer,
   regulator/compliance. Concrete, not generic.
4. **What to test** — a checklist (`- [ ]` items, 10–20) and a table of 6–10 example test cases:
   `ID | Condition / steps | Expected result`. IDs like `CP-01` (area prefix). Include negative,
   boundary, timing (cut-off, time zones, expiry), concurrency/duplicates, and reconciliation cases.
5. **Typical defects** — 5–8 realistic defect patterns, each one line of "what goes wrong" + one
   line of "how to catch it". Link card-wallet bug reports where they really match.
6. **In card-wallet** — what of this area exists in https://github.com/Tomullya/card-wallet
   (read the card-wallet repo: docs/requirements, docs/qa,
   wallet-api, fraud-service, tests). Link real files as
   `https://github.com/Tomullya/card-wallet/blob/main/<path>` — every linked file must exist.
   Then 2–4 bullet ideas "could be added" (honest: card-wallet is a simplified demo).
7. **Sources** — 4–10 bullet links to official or public primary sources (see below), each with
   one short note on what it supports. At least 3 must be http(s) links.

## Sources (binding)
Use only official/public primary sources: Visa and Mastercard public rules and guides; public
docs of Stripe/Adyen/other PSPs; EUR-Lex texts (PSD2 2015/2366, RTS on SCA 2018/389, EMD2
2009/110, GDPR 2016/679, AMLD); EBA guidelines; EPC SEPA rulebooks; ISO 20022 public pages;
PCI SSC documents; FATF; IFRS Foundation; central bank / regulator pages. Use WebSearch/WebFetch
to confirm facts and get exact URLs; never invent a URL. If schemes or countries differ, say
"rules differ by scheme / country" rather than presenting one variant as universal. No numbers
you cannot source (fees, timeframes) — say "typically" only when a source says so. No long
verbatim quotes. No information about any specific employer's internal systems.

## Language
RU: natural Russian fintech language; at first use give the English term in parentheses, e.g.
«возврат платежа (refund)». Keep the same examples and numbers in both languages.

## Length
About 1500–2500 words per language. Depth over breadth.

## Glossary
At the end of your report back, list glossary rows for every key term you introduced:
`English | Русский | Meaning (EN, one line) | Значение (RU, одна строка)`. Do not edit the
glossary files yourself.

## Check
`python3 scripts/check_playbook.py` must print `Playbook check: OK` — but it also requires the
area to be listed in README.md/README.ru.md; the coordinator adds that row, so a "not listed"
message for your area is expected. Fix every other problem.

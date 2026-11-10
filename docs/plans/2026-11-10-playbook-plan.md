# Fintech Testing Playbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the empty `fintech-testing-playbook` repo into a bilingual (EN/RU) Markdown playbook of 10 fintech areas with a CI structure check.

**Architecture:** Content is Markdown: `areas/NN-<slug>/en.md` and `ru.md` with a fixed 7-section template; a stdlib-only Python checker enforces structure and links; GitHub Actions runs it. Area texts are written by author subagents from a shared brief and fact-checked by separate reviewer subagents against official public sources.

**Tech Stack:** Markdown + Mermaid (GitHub renders it), Python 3.12 standard library (`unittest`), GitHub Actions.

**Spec:** `docs/design/2026-11-10-playbook-design.md`

## Global Constraints

- Every area folder has `en.md` and `ru.md` with the same 7 level-2 headings in this order —
  EN: `How it works`, `Participants and money flows`, `Business risks`, `What to test`, `Typical defects`, `In card-wallet`, `Sources`;
  RU: `Как это работает`, `Участники и потоки денег`, `Бизнес-риски`, `Что тестировать`, `Типичные дефекты`, `В card-wallet`, `Источники`.
  Area 10 instead: `Questions` / `Вопросы` and `Sources` / `Источники`.
- Areas 01–08 contain at least one ```` ```mermaid ```` block; every page has ≥ 3 `http(s)` links under Sources.
- Sources: official/public primary sources only (spec §Sources); no employer internals; no long verbatim quotes.
- Links to card-wallet use `https://github.com/Tomullya/card-wallet/blob/main/<path>` and must point to files that exist.
- Checker uses the Python standard library only.
- Commits authored as `Tomullya <61884339+Tomullya@users.noreply.github.com>`; push only with the author's OK.

## Review Focus

1. A page whose RU and EN versions drift apart (a section missing in one language) — pinned in Task 1 (`test_missing_heading_in_ru_fails`).
2. Headings in the wrong order or renamed — pinned in Task 1 (`test_heading_order_enforced`).
3. A relative link to a file that does not exist (e.g. after renaming an area) — pinned in Task 1 (`test_broken_relative_link_fails`).
4. A new area folder not listed in README — pinned in Task 1 (`test_area_missing_from_readme_fails`).
5. A wrong fact in a money flow or a regulation — no code test; covered by the per-area fact review step in Tasks 2–7.

---

### Task 1: Repo restructure and structure checker

**Files:**
- Delete: `postman/`, `.github/workflows/newman.yml`, `docs/test-plan.md`
- Create: `scripts/check_playbook.py`, `tests/test_check_playbook.py`, `.github/workflows/check.yml`, `README.md`, `README.ru.md`, `glossary.md`, `glossary.ru.md`, `docs/area-brief.md` (writing rules for authors, from the spec)
- Modify: `.gitignore` (add `.superpowers/`, remove Postman/Newman blocks)

**Interfaces:**
- Produces: `check(root: Path) -> list[str]` (problems; empty = OK) and CLI `python3 scripts/check_playbook.py` (prints problems, exit 1 if any). README must contain a link `areas/NN-<slug>/en.md` (README.md) / `areas/NN-<slug>/ru.md` (README.ru.md) for every area folder.

- [ ] **Step 1:** write `tests/test_check_playbook.py` (unittest, temp dirs): `test_valid_area_passes`, `test_missing_ru_file_fails`, `test_missing_heading_in_ru_fails`, `test_heading_order_enforced`, `test_mermaid_required_for_01_to_08`, `test_area_10_uses_questions_template`, `test_three_source_links_required`, `test_broken_relative_link_fails`, `test_area_missing_from_readme_fails`. Run `python3 -m unittest discover -s tests` → FAIL (module missing).
- [ ] **Step 2:** implement `scripts/check_playbook.py`; run tests → PASS.
- [ ] **Step 3:** delete Postman skeleton; write READMEs (EN/RU: purpose, how to read, area map with planned areas marked, link to card-wallet, sources policy), empty glossary pages, `check.yml` (checkout, setup-python 3.12, unittest, checker), `docs/area-brief.md`. Run checker → OK (no areas yet).
- [ ] **Step 4:** commit `chore: playbook structure, checker and CI`.

### Tasks 2–3: Area 01 card payment, area 02 accounting

Per area (same steps): author subagent writes `areas/0N-<slug>/en.md` + `ru.md` from `docs/area-brief.md`; run checker → OK; fact-review subagent checks every claim against the listed primary sources and fixes; run checker → OK; commit `feat: area 0N <name>`.
- [ ] **Task 2:** `areas/01-card-payment/` — authorisation, capture/clearing, settlement, reversal, refund, chargeback, partial capture, pre-authorisation; card-wallet link: payments service, BR-PAY-02 order of checks, idempotency.
- [ ] **Task 3:** `areas/02-accounting/` — double entry, chart of accounts, GL vs subledgers, posting rules (payment with fee, refund, chargeback), suspense accounts, EOD/EOM, reconciliation types, FX revaluation, safeguarding; card-wallet link: transactions + commission, "balance = sum of transactions" DB test.
- [ ] **CHECKPOINT:** show areas 01–02 to the author; apply feedback; with OK push branch → main.

### Tasks 4–6: Areas 03–08 (two per task, same per-area steps)
- [ ] **Task 4:** 03 money (ledger, reconciliation, rounding, fees, FX), 04 card lifecycle.
- [ ] **Task 5:** 05 transfers (SEPA SCT/SCT Inst, ISO 20022 basics, idempotency, cut-off), 06 limits, fraud, AML.
- [ ] **Task 6:** 07 onboarding/KYC, 08 regulation for testers (PSD2/SCA/3DS, PCI DSS, GDPR).

### Task 7: Areas 09–10, glossary, README final
- [ ] 09 test data (public test card numbers, Luhn, BIN, IBAN check digits — worked examples), 10 interview questions (≥ 20 Q&A across areas, linking to areas); fill `glossary.md`/`.ru.md` with all terms used; README area map complete. Checker → OK; commit.

### Task 8: Final review and publish
- [ ] Whole-repo review subagent (structure, cross-links, consistency of terms between areas, privacy/NDA, copyright); fix Important findings; checker → OK; with the author's OK push and confirm the GitHub Actions run is green.

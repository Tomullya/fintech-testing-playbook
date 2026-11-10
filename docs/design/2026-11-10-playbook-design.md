# Fintech Testing Playbook — design

Date: 2026-11-10 · Status: agreed in conversation, awaiting the author's review.

## Goal
A bilingual (EN/RU) Markdown playbook that explains how fintech business processes work and how
to test them: card payments, accounting, money movement, fraud/AML, onboarding, regulation.
Two readers: the author (deep learning of fintech processes before job interviews) and
employers (proof of business-domain understanding). It complements the technical portfolio
project https://github.com/Tomullya/card-wallet and links to it for real code, tests and bugs.

Out of scope now: an interactive site (maybe later, generated from the same Markdown), code
or Postman collections (they live in card-wallet).

## Repository
Renamed `fintech-qa-portfolio` → `fintech-testing-playbook`. The empty Postman skeleton
(`postman/`, Newman workflow, old test plan) is removed.

```
README.md, README.ru.md         what it is, area map, how to read, link to card-wallet
areas/NN-<slug>/en.md, ru.md    one folder per area
glossary.md, glossary.ru.md     EN↔RU terms
scripts/check_playbook.py       structure checks (run in CI)
.github/workflows/check.yml     runs the checks on every push
```

Areas, in build order: 01 card payment (authorisation → clearing → settlement, reversal,
refund, chargeback) · 02 accounting for testers (double entry, chart of accounts, GL vs
subledgers, posting rules, EOD/EOM close, reconciliation types, FX revaluation, safeguarding) ·
03 money: ledger, reconciliation, rounding, fees, FX · 04 card lifecycle · 05 transfers:
SEPA, instant, idempotency, cut-off · 06 limits, fraud, AML · 07 onboarding and KYC ·
08 regulation for testers: PSD2/SCA/3-D Secure, PCI DSS, GDPR · 09 test data: test cards,
Luhn, BIN, IBAN · 10 fintech QA interview questions.

## Page template (both languages, same headings in this order)
1. How it works — plain words, a Mermaid diagram, a worked example with numbers.
2. Participants and money flows — who owes whom what, and when.
3. Business risks — for the company, the customer, the regulator.
4. What to test — checklist + 5–10 example test cases (id, steps/condition, expected).
5. Typical defects — with links to card-wallet bug reports where they exist.
6. In card-wallet — links to code/tests, or "could be added".
7. Sources — official/public primary sources only, with links.
Area 10 (interview questions) uses Q&A instead of sections 1–6 but keeps Sources.

## Sources and accuracy (binding)
Only official or public primary sources: Visa Core Rules and Mastercard public rules/
chargeback guide; Stripe/Adyen public docs; PSD2 (EU 2015/2366) and RTS on SCA (EU 2018/389),
EBA guidelines, EMVCo; EPC SEPA rulebooks, ISO 20022 public catalogue; PCI SSC documents;
FATF recommendations, EU AML directives; GDPR; IFRS Foundation; EMD2 and regulator
safeguarding guidance. Where rules differ between card schemes or countries, say so.
No internal details of any employer (NDA). Every area is fact-checked against its sources by a
separate reviewer before it is merged. No long verbatim quotes.

## Checks (CI)
`scripts/check_playbook.py`: every area has `en.md` and `ru.md`; both have the 7 headings
(EN and RU wording fixed in the script) in order; each has at least one Mermaid block (except
areas 09–10) and at least 3 links under Sources; relative links resolve; README lists every
area. Python standard library only; runs in GitHub Actions on every push.

## Delivery
Areas 01 and 02 first, shown to the author; then 03–10. Commits per area. Push only with the
author's OK (needs a GitHub token).

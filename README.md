# 💳 Fintech Testing Playbook

[![Playbook check](https://github.com/Tomullya/fintech-testing-playbook/actions/workflows/check.yml/badge.svg)](https://github.com/Tomullya/fintech-testing-playbook/actions/workflows/check.yml)  ·  [Русская версия](README.ru.md)

How fintech business processes work — and how to test them. Card payments, accounting,
money movement, fraud and AML, onboarding, regulation: each explained in plain words with a
diagram and a worked example, followed by the business risks, a test checklist, example test
cases and typical defects.

I am a QA engineer with a card-payments background. This playbook is the business side of my
portfolio; the technical side is **[card-wallet](https://github.com/Tomullya/card-wallet)** — a
working wallet with REST + gRPC services and 600+ automated tests. Every area here links to the
places in card-wallet where the same idea is implemented and tested.

## Areas

| # | Area | Status |
|---|---|---|
| 01 | [Card payment](areas/01-card-payment/en.md): authorisation, clearing, settlement, reversal, refund, chargeback | ✅ ready |
| 02 | [Accounting for testers](areas/02-accounting/en.md): double entry, ledgers, posting rules, reconciliation, safeguarding | ✅ ready |
| 03 | [Money: balances, rounding, fees, FX](areas/03-money/en.md) | ✅ ready |
| 04 | [Card lifecycle: card data, statuses, reissue, tokens](areas/04-card-lifecycle/en.md) | ✅ ready |
| 05 | [Transfers: SEPA, instant payments, R-transactions, cut-off times](areas/05-transfers/en.md) | ✅ ready |
| 06 | [Limits, fraud and AML](areas/06-limits-fraud-aml/en.md) | ✅ ready |
| 07 | [Onboarding and KYC](areas/07-onboarding-kyc/en.md) | ✅ ready |
| 08 | [Regulation for testers: PSD2 / SCA / 3-D Secure, PCI DSS, GDPR](areas/08-regulation/en.md) | ✅ ready |
| 09 | [Test data: test cards, Luhn, BIN, IBAN](areas/09-test-data/en.md) | ✅ ready |
| 10 | [Fintech QA interview questions (30 with model answers)](areas/10-interview-questions/en.md) | ✅ ready |

Terms: [glossary](glossary.md).

## How every area is built

1. **How it works** — plain words, a diagram, an example with numbers
2. **Participants and money flows** — who owes whom what, and when
3. **Business risks** — for the company, the customer and the regulator
4. **What to test** — checklist and example test cases
5. **Typical defects**
6. **In card-wallet** — where it is implemented and tested
7. **Sources**

## Sources and accuracy

Only official or public primary sources: card scheme public rules, EU legislation (PSD2, RTS on
SCA, GDPR), EBA guidelines, EPC SEPA rulebooks, PCI SSC documents, FATF recommendations, IFRS
Foundation, and public documentation of payment providers. Where rules differ between card
schemes or countries, the page says so. No internal information of any employer is used.
Every area is fact-checked against its sources before publishing; `scripts/check_playbook.py`
checks the structure, both languages and links in CI.

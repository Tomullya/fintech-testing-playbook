# Fintech QA interview questions

Thirty questions a QA engineer is likely to hear in a fintech interview, grouped by topic. Each
has a model answer with concrete numbers, one line on what the interviewer is really checking, and
a link to the playbook area that explains the topic in depth. The numbers and examples are the
same as in the areas, so you can practise an answer here and then read the details there.

How to use this page: answer aloud first, then compare. A good fintech answer names the
**money effect** (who is debited, when), a **boundary** and a **failure** (timeout, duplicate,
time zone). Rules that differ by scheme or country are marked as such — say so in the interview too.

## Questions

### Part 1 · Card payments and card lifecycle

### 1. What is the difference between authorisation, capture, clearing and settlement?

**Answer.**
- **Authorisation** — the issuer approves or declines and puts a **hold** on the money. No money
  moves: the ledger balance stays the same, the available balance goes down.
- **Capture** — the merchant says "charge this approved payment for the final amount".
- **Clearing** (presentment) — the acquirer sends captures to the scheme in files; the issuer
  matches each record to its authorisation, posts it and releases the hold.
- **Settlement** — the real movement of money: issuer → scheme → acquirer → merchant, net of
  interchange and fees. The number of days depends on scheme, acquirer and contract — not a fixed T+1.
- Example: hotel pre-authorises EUR 120.00, adds 30.00 (incremental), captures 135.00 at check-out
  and reverses 15.00; clearing posts 135.00 the next day and the hold drops to 0.00.

**What the interviewer is checking:** that you know an approval is not a payment and can follow
the hold and the posting separately.

**Read more:** [Card payment](../01-card-payment/en.md)

### 2. Reversal vs refund vs chargeback — what is the difference?

**Answer.**

| | Reversal | Refund | Chargeback |
|---|---|---|---|
| Who starts it | Merchant or acquirer | Merchant | Issuer, usually after a complaint |
| When | Before clearing | After clearing | After clearing, within scheme time limits |
| Effect | Cancels all or part of the authorisation, releases the hold | New credit transaction | Money taken back from the acquirer, then the merchant |

- The customer sees a reversal as the pending payment disappearing; a refund as a separate credit
  next to the original charge (−135.00 and +20.00).
- The chargeback has stages: dispute → representment (merchant's evidence) → pre-arbitration →
  arbitration. Visa groups disputes into fraud, authorisation, processing errors and consumer
  disputes; time limits differ by scheme and reason (Stripe notes networks typically allow 120 days).
- Trap: APIs blur the line — Stripe may process an early refund as a reversal, and Adyen has one
  "reversal" call that cancels or refunds depending on the state.

**What the interviewer is checking:** who starts each one, at which stage, and that a refund
never edits the original transaction.

**Read more:** [Card payment](../01-card-payment/en.md), [Accounting for testers](../02-accounting/en.md)

### 3. A customer's available balance is lower than expected after a hotel stay. What could be wrong and how do you test it?

**Answer.**
- Available balance = ledger balance − active holds. A hold that is never released is the usual cause.
- Causes: partial capture without a reversal of the unused part (captured 135.00 of 150.00 held,
  15.00 still blocked); a clearing record not matched to its authorisation; hold expiry not running.
- The opposite defect is also real: the hold is released on 14 Nov but the clearing arrives on
  15 Nov, so for a day the customer sees 1,000.00 available and can overspend.
- Tests: check available and ledger balance after **every** step (auth, incremental, capture,
  reversal, clearing, expiry); a capture lower than authorised; no capture until after the expiry
  date; a clearing record with no matching authorisation goes to an exceptions report.

**What the interviewer is checking:** that you test balances as two numbers and think about
the time between steps.

**Read more:** [Card payment](../01-card-payment/en.md), [Money](../03-money/en.md)

### 4. Freeze, block, lost — how do you test card statuses?

**Answer.**
- Statuses (names differ by issuer): Inactive, Active, Frozen (by the client, reversible),
  Blocked (by the issuer), Lost/Stolen (permanent), Expired, Closed.
- Key rule: **temporary statuses can go back to Active, permanent ones never can**. A lost card is
  replaced by a new card with a new PAN.
- Use a **state transition table** with the invalid pairs too: Lost → Active, Closed → Frozen,
  Expired → Blocked must be rejected or follow a written rule.
- A status must reach every channel: plastic, online, ATM and phone wallet tokens (freezing the
  plastic does not automatically freeze the token).
- A block stops **new** authorisations only: a hotel hold from 12 Nov is still cleared on 15 Nov
  after the card is reported lost on 14 Nov.
- Security: client B calling "block" on client A's card must get 404, like a non-existing card.

**What the interviewer is checking:** state-transition testing, including invalid transitions,
and channels beyond the main app.

**Read more:** [Card lifecycle](../04-card-lifecycle/en.md)

### 5. How would you test the card expiry date?

**Answer.**
- First get the rule: the card is commonly valid through the last day of the `MM/YY` month, but
  scheme and issuer set the exact rule — and in which time zone the day ends.
- Boundaries for a card 11/29 and a UTC rule: pay on 30 Nov 2029 at 23:59 UTC → approved;
  on 1 Dec 2029 at 00:00 UTC → declined as expired.
- Repeat in local time if the rule is local; include a customer abroad.
- Check what expiry changes: new authorisations decline, but holds and clearings of payments
  authorised before expiry still process; the expired card frees a slot in the card count limit.
- Renewal: usually the same PAN with a new expiry and CVV2 (issuer rule), so saved-card payments
  with the old expiry may fail.

**What the interviewer is checking:** boundary values on dates and awareness that "the end of
the day" needs a time zone.

**Read more:** [Card lifecycle](../04-card-lifecycle/en.md)

### Part 2 · Accounting and money

### 6. Which ledger invariants would you check?

**Answer.**
1. Every journal entry has ≥ 2 lines and **sums to zero per currency** (debits = credits).
2. **Account balance = sum of its postings**; a stored balance is only a cache.
3. **GL control account = sum of the subledger** (e.g. account 2100 = sum of all customer wallets).
4. **Original + reversal = 0** on every account and currency.
5. Posted entries are never updated or deleted; corrections are new entries.
6. Declined operations create no postings; no negative balance where it is not allowed.
7. Safeguarded funds ≥ customer liabilities; suspense is empty or explained at close.
- Example: card payment EUR 100.00 with a 1 % fee → Dr Customer 101.00, Cr Scheme payable 100.00,
  Cr Fee income 1.00; sum 0.00. Run these as nightly SQL checks, not only in test cases.

**What the interviewer is checking:** that you can find lost money without reading every
transaction, using invariants.

**Read more:** [Accounting for testers](../02-accounting/en.md)

### 7. How do you test a payment with a fee?

**Answer.**
- Get the rule exactly: e.g. 1 % of the amount, half-up to cents, minimum EUR 0.50.
- Boundaries where the minimum stops: 50.49 → 0.50, 50.50 → 0.51. A tie value: 150.50 → 1.51
  (half-even would give 1.50). If there is a cap or tiers, test their borders ± 0.01.
- Funds check must include the fee: balance 100.00, pay 99.00 → fee 0.99, total 99.99, approved;
  pay 99.50 → fee 1.00 (0.995 rounded up), total 100.50, declined.
- The fee must reach fee income in the ledger, appear on the statement and in reports with the
  same total.
- Refund: the fee rule (full, proportional, none) must be written and tested; refunded ≤ paid.
- Real example: card-wallet [BUG-01](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-01.md)
  — the minimum fee was not applied, so a EUR 10.00 payment was charged 0.10 instead of 0.50.

**What the interviewer is checking:** boundary values on money, rounding mode, and the fee in
the balance check and the ledger.

**Read more:** [Money](../03-money/en.md), [Accounting for testers](../02-accounting/en.md)

### 8. Why not use float for money, and how do you test rounding?

**Answer.**
- Binary floats cannot store 0.1 exactly: `0.1 + 0.2` is `0.30000000000000004`, `round(2.675, 2)`
  gives 2.67. Use a decimal type or integers in minor units (EUR 10.99 = `1099`).
- Know each currency's exponent (ISO 4217): EUR 2, JPY 0, BHD 3. Hard-coded "÷ 100" shows JPY 500
  as 5.00.
- Rounding mode is a business rule: half-up vs half-even differ only on exact ties (2.345 → 2.35
  vs 2.34), so test data must contain ties. Python's `Decimal` defaults to half-even.
- Round once, at a documented step: three payments of 0.55 at 1.5 % give 0.03 per line but 0.02
  on the total — reports that mix methods never match.
- Allocation: 100.00 / 3 must be 33.34 + 33.33 + 33.33; the sum of parts always equals the whole.

**What the interviewer is checking:** that you know where cents disappear and design data to
expose it.

**Read more:** [Money](../03-money/en.md)

### 9. What is a reconciliation break and how would you test a reconciliation job?

**Answer.**
- Reconciliation compares our records with another source: internal (GL control account vs
  subledger) or external (ledger vs bank statement, scheme settlement report, PSP payout report).
- A **break** is an unmatched or unequal item: missing on our side, missing on theirs, amount
  differs, duplicate. Causes: timing (23:58 lands in tomorrow's file), missing or double postings.
- Matching keys: our id or the partner reference (end-to-end ID for transfers; acquirer or
  retrieval reference for cards) plus amount, currency and a date window — **never amount alone**,
  or two EUR 850.00 transfers swap.
- Tests: remove one line from the bank file and duplicate another → exactly two breaks with
  reference, amount and age; run the job twice for the same day → same result; one-to-many
  matching (one payout line = many payments minus fees).

**What the interviewer is checking:** that you test the job by injecting each break type, not
only the happy path.

**Read more:** [Accounting for testers](../02-accounting/en.md), [Money](../03-money/en.md)

### 10. How would you test a currency conversion?

**Answer.**
- Quote: the customer sees rate, amounts, fee and an expiry (e.g. 30 s). Confirm at 31 s →
  re-quote or reject; never execute silently at a new rate. Executed rate = quoted rate (quote id).
- Rounding to the **target** exponent: EUR 100.00 → JPY 16,012; → BHD 41.234.
- Round-trip exploit: buy EUR at 162 JPY, sell at 158. JPY 1 → EUR 0.01 → JPY 2 with half-up.
  Test that a round trip never gains; use a minimum amount or round in the company's favour.
- Disclosure in the EU: card payment of PLN 430.00 from a EUR wallet; ECB rate 4.3000 → benchmark
  EUR 100.00; charged 101.50 → mark-up 1.50 %. The same figure must be in the price list, in the
  app before paying and in the message after (Regulation (EU) 2021/1230).
- Cards: the rate at authorisation and at clearing may differ, so posted ≠ held; the difference
  must be explained and reconciled.

**What the interviewer is checking:** quote expiry, exponents, and that you know rounding can be
exploited.

**Read more:** [Money](../03-money/en.md), [Card payment](../01-card-payment/en.md)

### 11. Two payments arrive at the same moment. What can go wrong and how do you test it?

**Answer.**
- A **race condition**: both requests read balance 100.00, both pass the check, both pay 60.00.
  With a 1 % fee the balance ends at 39.40 with two approved payments (lost update) — the company
  lost 60.60 — or at −21.20.
- Protections: lock the account row while checking and debiting (`SELECT … FOR UPDATE`) or one
  conditional `UPDATE … WHERE balance >= amount` and check that one row changed; DB constraints
  (balance ≥ 0, unique idempotency key) as the last line.
- Test: send two 60.00 payments in parallel with a barrier → exactly one approved, balance 39.40;
  then check balance = sum of transactions. The same applies to the last part of a daily limit.
- Repeat many times: a race test that passes once proves little.

**What the interviewer is checking:** that you test concurrency deliberately and check the
result with an invariant.

**Read more:** [Money](../03-money/en.md)

### Part 3 · Transfers

### 12. SEPA Credit Transfer vs SEPA Instant — what is different for a tester?

**Answer.**

| | SCT | SCT Inst |
|---|---|---|
| When | Banking business days (T2 days) | 24/7, every calendar day |
| Speed | Money at the payee's PSP by D+1 | Payee credited and confirmed within 10 seconds |
| Cut-off | Set by each PSP | None |
| After failure | Reject, return (3 business days), recall | Confirmed or rejected in seconds; then only recall |

- Instant: if no confirmation in 10 s, the payer's account is restored; a late confirmation must
  not create a debit. On request the customer can set a per-day or per-transaction limit.
- Instant must not cost more than standard (IPR). Verification of payee (VoP) applies to both,
  before the payer authorises.
- Test focus: SCT → calendars, cut-off, value dates; Inst → timeouts, rollback, late messages.

**What the interviewer is checking:** you know the two clocks and the 10-second rule.

**Read more:** [Transfers](../05-transfers/en.md)

### 13. How do you prevent double charging? How do you test idempotency?

**Answer.**
- The client sends an **idempotency key** with each request. Same key + same body → the stored
  response returns, nothing new is created. Same key + different body → error (e.g. `409`).
- The key check and the debit happen in **one database transaction**, or two parallel requests
  both pass.
- After a timeout, ask for the status — never send a new payment message. Cards: the acquirer
  sends a reversal for an authorisation without a response.
- A business duplicate check (same IBAN, amount, reference within minutes) usually **warns**,
  because paying rent twice can be real.
- Tests: sequential retry; five parallel requests with one key → one transaction, one debit,
  identical responses; changed amount 850.00 → 580.00 with the same key → error; key reusable after
  a `503` where nothing was saved; key scoped per user.
- Also check what the idempotency table stores: in card-wallet
  [BUG-11](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-11.md)
  the stored request hash included the CVV.

**What the interviewer is checking:** parallel testing, not just "send twice", and where the key
is stored.

**Read more:** [Transfers](../05-transfers/en.md), [Money](../03-money/en.md)

### 14. A customer in Lisbon sends rent at 15:30 on 24 December. When does it arrive?

**Answer.**
- The cut-off is in the PSP's time zone (here 16:00 CET, illustrative). 15:30 in Lisbon is 16:30
  in Frankfurt — after the cut-off.
- 25 and 26 December are TARGET closing days and 27 December is a Sunday, so the order counts as
  received on **Mon 28 Dec 2026** (day D) and must reach the payee's PSP by **Tue 29 Dec** (D+1).
- The app must show "28–29 Dec", not "tomorrow"; the amount is reserved at once.
- Tests: 15:59:59 and 16:00:01 CET; clients in other zones; CET and CEST; every TARGET closing day
  (Good Friday and Easter Monday move each year); a future-dated order for Fri 1 May 2026 runs on
  Mon 4 May.
- As SCT Inst the same order is credited in seconds on 24 Dec.

**What the interviewer is checking:** time zones, business-day calendars and honest
communication to the customer.

**Read more:** [Transfers](../05-transfers/en.md)

### 15. Reject, return, recall — what is the difference?

**Answer.**
- **Reject** — refused **before** inter-PSP settlement (bad format, invalid IBAN); goes back with
  a reason code, at the latest the next business day.
- **Return** — money was settled but the payee's PSP cannot credit (`AC04` closed account); sent
  within **3 banking business days** after settlement as pacs.004.
- **Recall** — the payer's PSP asks to cancel: duplicate (`DUPL`) or technical problem (`TECH`)
  within 10 banking business days, fraud (`FRAD`) within 13 months; the payee's PSP answers within
  15 banking business days (positive: pacs.004, negative: camt.029).
- Count business days with the calendar: a return after settlement on 29 Dec 2026 may come on
  30 Dec, 31 Dec or 4 Jan 2027 (1 Jan is closed).
- Tests: each restores the balance **once**, linked to the original, with the reason shown; the
  original status changes to "returned"; no jump from rejected to completed.

**What the interviewer is checking:** that you know money can come back days later and must be
linked to the original.

**Read more:** [Transfers](../05-transfers/en.md)

### Part 4 · Limits, fraud, AML and KYC

### 16. How do you test a daily limit around midnight and time zones?

**Answer.**
- Ask three questions: **what counts** (approved only? fees? holds? refunded?), **which window**
  (calendar day or rolling 24 h), **which time zone** (UTC, bank, customer).
- Example, limit EUR 1,000.00 per UTC day, customer in Berlin: a payment at 00:30 on 14 Mar local
  is 23:30 UTC on 13 Mar and counts to **13 March**.
- Boundaries: 600.00 + 400.00 = 1,000.00 → approved (exact limit allowed); then 0.01 → declined.
- Midnight: payments at 23:59:59 and 00:00:00 in the rule's zone.
- Daylight saving: 29 Mar 2026 has 23 local hours and 25 Oct 2026 has 25 — nothing counted twice
  or lost. Month ends for monthly limits.
- Parallel: two 300.00 payments with 400.00 left → exactly one approved.

**What the interviewer is checking:** that you ask for the definition before testing and know
the DST trap.

**Read more:** [Limits, fraud and AML](../06-limits-fraud-aml/en.md)

### 17. How would you test a fraud rules engine or a new fraud rule?

**Answer.**
- **Boundaries** of each rule: amount > 5,000.00 → 5,000.00 approved, 5,000.01 declined.
- **Order**: 6,000.00 at a gambling merchant matches two rules; the first in order gives the
  reason (`HIGH_AMOUNT`, not `BLOCKED_CATEGORY`).
- **Reachability**: a rule that an earlier check always pre-empts is a requirements defect
  (card-wallet [BUG-05](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-05.md)).
- **Decisions**: approve, decline, step-up, review — passed, failed and abandoned challenges.
- **Failure**: fraud service timeout → the specified fail-closed or fail-open behaviour.
- **Audit**: rule version, inputs, score, reason codes and request id stored for each decision.
- **Shadow mode** before go-live: e.g. 1,200 flagged of 100,000, 24 real fraud, 40 fraud in total →
  precision 2 %, recall 60 %, 1,176 good customers would be blocked.

**What the interviewer is checking:** rule logic plus the business cost of false positives.

**Read more:** [Limits, fraud and AML](../06-limits-fraud-aml/en.md)

### 18. Sanctions screening gives many false positives. How do you test it?

**Answer.**
- Screening compares names with sanctions lists using **fuzzy matching**: a similarity score and a
  threshold. Most hits are false hits that an analyst closes using date of birth, country or ID.
- Example with fictional names: payee "Ivan Petrovski Testov" scores 0.91 against list entry
  "Ivan Petrovsky Testoff", threshold 0.85 → hit, payment held; different date of birth → released
  with a recorded reason.
- Tests: a table of variants — exact, transliteration, swapped first/last name, diacritics,
  truncation, case; scores at threshold − 0.01, threshold, + 0.01.
- Re-screening of existing customers after every list update.
- For SEPA instant transfers the IPR changes the model: PSPs check their own customers against EU
  lists at least daily and on list changes, not each instant transfer.
- Use only fictional names in tests; the customer sees neutral texts (no tipping-off).

**What the interviewer is checking:** you understand fuzzy matching is a trade-off and test the
threshold, not just "a known name is caught".

**Read more:** [Limits, fraud and AML](../06-limits-fraud-aml/en.md), [Transfers](../05-transfers/en.md)

### 19. How would you test an AML monitoring scenario such as structuring?

**Answer.**
- Structuring: many payments just below a threshold. Illustrative scenario: ≥ 5 credits of
  1,900–1,999.99 in 48 hours. Rapid movement: ≥ 90 % of credits sent out within 24 hours.
- Data: five credits of 1,950.00, 1,980.00, 1,900.00, 1,990.00 and 1,960.00 from five senders
  (9,780.00), then 9,600.00 out to a new payee abroad → both scenarios fire, **one alert**.
- Boundaries: four credits → no alert; 1,899.99 → not counted; the 48-hour window edge.
- One alert per pattern, not one per payment; the alert links all payments.
- **Tipping-off**: while an alert is open or a report is filed, app, push messages, API errors and
  support texts stay neutral ("processing"); no `AML_HOLD` code visible to the customer.
- Records retained 5 years after the relationship ends.

**What the interviewer is checking:** that you test aggregate rules over time and the legal
"silence" requirement.

**Read more:** [Limits, fraud and AML](../06-limits-fraud-aml/en.md)

### 20. How would you test a KYC onboarding flow?

**Answer.**
- Statuses (names differ): Pending → Verified / Rejected; Verified → Restricted → Verified; Closed.
  While Pending, **no money moves on any channel** — app, API, card, transfer (a top-up API call
  must fail).
- Name matching: document "YULIIA" vs entered "Yulia" → manual review, not auto-reject; also
  "Müller"/"Mueller", double surnames.
- Boundaries: minimum age 18, onboarding on 12 Nov 2026 → born 12 Nov 2008 accepted, 13 Nov 2008
  rejected; document expiry at 23:59 / 00:01 in the policy's time zone.
- Vendor failures: timeout → retry with the **same session**, one vendor case, one fee; two late
  callbacks → one decision by a documented rule.
- Ongoing: document expiry restricts the account at the right moment and is lifted after a new
  document; re-screening after list updates.
- Audit trail for every manual decision; synthetic identities and vendor sandbox documents only.

**What the interviewer is checking:** status × channel coverage and vendor failure handling.

**Read more:** [Onboarding and KYC](../07-onboarding-kyc/en.md)

### Part 5 · Regulation

### 21. What is SCA? Is card number plus CVV enough?

**Answer.**
- Strong Customer Authentication (PSD2 Art. 97, RTS (EU) 2018/389): at least **two elements from
  two different categories** — knowledge (PIN), possession (bound phone), inherence (fingerprint).
- Card number + CVV is **not** SCA: the EBA says data printed on the card is neither knowledge nor
  possession. Two passwords are one category.
- Testable RTS rules: at most five failed attempts, then a block; the error must not say which
  element was wrong; online banking session ends after 5 minutes of inactivity.
- **Dynamic linking**: the code is tied to amount and payee; change EUR 120.00 to 121.00 → code rejected.
- For cards SCA usually runs through 3-D Secure 2: frictionless or challenge; outcomes Y, N, A, U,
  R, C must each lead to the specified decision. Successful 3DS usually shifts fraud liability to
  the issuer — not guaranteed, scheme rules decide.

**What the interviewer is checking:** the "two categories" rule and that you can turn the RTS
into test cases.

**Read more:** [Regulation for testers](../08-regulation/en.md)

### 22. What are SCA exemptions and how would you test one?

**Answer.**
- Exemptions are optional — the issuer may always ask for SCA. Examples: contactless ≤ EUR 50
  (cumulative ≤ 150 or ≤ 5 in a row); low-value remote ≤ EUR 30 (previous ≤ 100 or ≤ 5 in a row);
  trusted beneficiaries; recurring same amount; transaction risk analysis (TRA) by fraud-rate bands.
- Merchant-initiated payments under a mandate are **out of scope**, not exempt.
- Test low-value with the amount counter, last SCA 2 Nov: 25.00, 30.00, 28.00, 17.00 → counter
  100.00, all exempt; 12.00 → still exempt (100.00 does not exceed 100); 9.00 → previous 112.00 →
  SCA, counter resets; 30.01 → always SCA.
- The requirement must say: amount or count counter, are declined payments counted, which
  channels share the counter. Without that, dev and QA will disagree.
- TRA: fraud rate 0.05 % → exempt up to EUR 250.00, not 250.01.

**What the interviewer is checking:** boundary and counter testing on a regulatory rule.

**Read more:** [Regulation for testers](../08-regulation/en.md)

### 23. What must never be logged or stored?

**Answer.**
- PCI DSS **sensitive authentication data** — CVV2/CVC2, PIN and PIN block, full track or chip
  data — must not be kept after authorisation, **even encrypted**, in any storage: database,
  logs, caches, queues, idempotency tables, backups. (Issuers have a narrow exception.)
- Full PAN: shown at most as BIN + last four; stored only unreadable (encrypted, tokenised,
  truncated, or a **keyed** hash — a plain SHA-256 of a PAN can be brute-forced).
- Also keep out of logs: passwords, one-time codes and access tokens; personal data beyond what is
  needed (GDPR minimisation), e.g. document numbers from KYC.
- Test: pay with a test card, then search every log, export, error body and table for the full
  PAN and CVV; recompute the plain hash and assert it differs.
- card-wallet examples: [BUG-10](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-10.md)
  (unkeyed PAN hash), [BUG-11](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-11.md)
  (CVV in the idempotency hash).

**What the interviewer is checking:** PCI DSS basics and that "logs" include technical tables.

**Read more:** [Regulation for testers](../08-regulation/en.md), [Card lifecycle](../04-card-lifecycle/en.md)

### 24. A customer asks to delete all their data. What do you test?

**Answer.**
- GDPR gives a right to erasure (Art. 17), but Art. 17(3)(b) allows keeping data when the law
  requires it. AML rules require CDD and transaction records for 5 years after the relationship
  ends (Member States may extend).
- Account closed 2 years ago: marketing data deleted; KYC and transaction records kept,
  **restricted**, until 5 years after closure; the customer is told what was kept and why.
- Retention job: records reaching their date at 00:00 UTC are removed exactly then — none a day
  early, none a day late; AML-held records skipped.
- Pseudonymised data (masked PAN + customer id) is still personal data.
- Breach: notify the authority without undue delay, where feasible within 72 hours.

**What the interviewer is checking:** that you see the conflict between GDPR and AML and test
both sides of the retention date.

**Read more:** [Regulation for testers](../08-regulation/en.md), [Onboarding and KYC](../07-onboarding-kyc/en.md)

### Part 6 · Test design and test data

### 25. How do you design test data without real card numbers or real people?

**Answer.**
- PCI DSS: no live PANs in pre-production unless that environment is protected as the cardholder
  data environment; test data removed before production.
- Use **scheme or PSP test cards** (each PSP publishes its own, with numbers that trigger declines
  or 3DS challenges), or generate **Luhn-valid numbers in a fictional range** — card-wallet uses
  the prefix `400000` with a computed check digit.
- Luhn: starting from the check digit (rightmost), double every second digit to its left,
  subtract 9 from results above 9, add everything — the sum must end in 0. Test both valid and
  one-digit-off numbers.
- IBANs with correct check digits; dates and times picked for boundaries (month end, DST, holidays).
- People: synthetic identities (Yuliia Testenko), fictional sanctions names, `@example.com`
  emails, vendor sandbox documents. Never a production copy.
- Card numbers, Luhn, BIN and IBAN in detail: area 09 (test data).

**What the interviewer is checking:** that you know test data is a compliance topic, not just
convenience.

**Read more:** [Card lifecycle](../04-card-lifecycle/en.md), [Regulation for testers](../08-regulation/en.md)

### 26. Which test design techniques do you use most in fintech? Give an example of each.

**Answer.**
- **Boundary value analysis** — limits, fees, exemptions: 999.99 / 1,000.00 / 1,000.01; fee
  50.49 / 50.50; SCA 30.00 / 30.01.
- **Equivalence partitioning** — currency exponent classes 0, 2, 3 (JPY, EUR, BHD); one test per
  class instead of every currency.
- **Decision table** — decline order: blocked, expired, wrong CVV, funds incl. fee, daily limit,
  anti-fraud; combine two failing conditions and check that the first one wins.
- **State transition** — card statuses, KYC statuses, transfer statuses; include invalid pairs.
- **Concurrency and duplicates** — parallel requests with and without the same idempotency key.
- **Time-based** — cut-off, midnight, DST, holidays, expiry.
- **Error guessing** from known defects — float, half-even default, server-local time zone.

**What the interviewer is checking:** that you name techniques and tie each to a real money rule.

**Read more:** [Card payment](../01-card-payment/en.md), [Limits, fraud and AML](../06-limits-fraud-aml/en.md)

### 27. A downstream service (fraud check, issuer, instant scheme) times out. What do you test?

**Answer.**
- A timeout is **not** a decline: the other side may have approved. The system must end in a known
  state and allow a safe retry.
- card-wallet: anti-fraud over gRPC with a 2-second timeout → `503`, nothing saved, and the
  idempotency key can be reused.
- Decide and test **fail-closed vs fail-open**: decline when the control is down, or approve
  within a small risk budget — a business rule.
- Cards: the acquirer reverses an authorisation with no response, so no orphan hold stays.
- SCT Inst: at 10 s the reservation is lifted; a confirmation at 12 s must not debit.
- Tools: a stub with configurable delay (answer at 9.9 s and 10.1 s, answer twice, never answer);
  check threads are not blocked under load.
- Related in card-wallet: [BUG-16](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-16.md).

**What the interviewer is checking:** that you test the unhappy integration path and late answers.

**Read more:** [Card payment](../01-card-payment/en.md), [Transfers](../05-transfers/en.md)

### Part 7 · "How would you test …" and behavioural questions

### 28. How would you test a refund feature?

**Answer.**
- Route: before clearing it should be a reversal (hold released); after clearing a refund (new
  credit linked to the original). Check which one the API actually produced.
- Amounts: full; partial; several partials — capture 135.00, refund 100.00 then 40.00 → second
  rejected (140.00 > 135.00). Zero, negative and too many decimals rejected.
- Fee: return all, proportional or none — as written; returned fee ≤ charged fee.
- Card changes: refund to an expired or replaced card still reaches the cardholder.
- Duplicates: same idempotency key → one refund; parallel refunds cannot exceed the total.
- Ledger: refund posts Dr Scheme payable, Cr Customer; the original stays unchanged.
- Chargeback after a refund: no double credit to the cardholder.
- Permissions and audit: who may refund, reason stored; statement shows −135.00 and +20.00.

**What the interviewer is checking:** structure — types, amounts, money effect, duplicates,
edge states — rather than a random list.

**Read more:** [Card payment](../01-card-payment/en.md), [Accounting for testers](../02-accounting/en.md)

### 29. A customer says they were charged twice. How do you investigate?

**Answer.**
1. Get facts: amount, time, merchant, screenshot, statement or app view.
2. Is it really two charges? Often it is one **pending hold plus one posted** transaction, or a
   pre-authorisation and a capture with a different amount. Compare authorisation ids and
   clearing records.
3. If there are two posted debits: check idempotency records — same key or two keys? Same body?
   Timestamps a few seconds apart point to a client retry after a timeout.
4. Check the ledger and reconciliation: two journal entries, two clearing records or one?
5. Fix the customer first (reversal or refund per the rule), then reproduce in test: retry with
   the same key, parallel retry, retry after a timeout.
6. Add a regression test and a monitoring query (two debits, same card, amount and merchant within
   N seconds).

**What the interviewer is checking:** calm, evidence-first investigation that separates display
issues from real double debits.

**Read more:** [Card payment](../01-card-payment/en.md), [Money](../03-money/en.md)

### 30. Tell me about a bug you found.

**Answer.** Use a short structure: context → how you found it → expected vs actual → impact →
fix and regression test. Examples from the card-wallet portfolio project:
- [BUG-02](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-02.md) —
  card daily limit 100.00, paid 60.00, then 40.00: declined `DAILY_LIMIT_EXCEEDED`, although the
  requirement (BR-PAY-04) allows reaching the limit exactly. The check behaved like `>=` instead of
  `>`. Caught by a boundary test (`test_daily_limit_exact_allowed`); this bug is planted in the
  project's buggy mode to prove the test suite catches it.
- [BUG-05](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-05.md) —
  a requirements defect found before any code: daily limit max 5,000.00 and the limit check runs
  before anti-fraud, so the fraud rule "amount > 5,000" could never fire. Fix: max daily limit
  raised to 10,000.00; regression test added. The cheapest bug is the one found in review.
- [BUG-13](https://github.com/Tomullya/card-wallet/blob/main/docs/qa/bug-reports/BUG-13.md) —
  an expired card could still be blocked by the client (200 instead of 409). Trivial, open and
  deferred: it needs a product decision, not a code change — good for showing judgement on severity.

**What the interviewer is checking:** clear reproduction, business impact, root cause and that
you prevent repeats — and honesty about where the bug came from.

**Read more:** [Limits, fraud and AML](../06-limits-fraud-aml/en.md), [Card lifecycle](../04-card-lifecycle/en.md)

## Sources

- [Visa Core Rules and Visa Product and Service Rules, public edition (PDF)](https://www.visa.co.uk/content/dam/VCOM/download/about-visa/visa-rules-public.pdf) — authorisation types and validity, reversals, dispute categories (questions 1–3).
- [Stripe: Idempotent requests](https://docs.stripe.com/api/idempotent_requests) — same key returns the saved result; different parameters cause an error (questions 11, 13).
- [Directive (EU) 2015/2366 (PSD2)](https://eur-lex.europa.eu/eli/dir/2015/2366/oj) — blocking funds, refunds, cut-off and execution time, SCA, liability (questions 1, 14, 21).
- [Delegated Regulation (EU) 2018/389, RTS on SCA](https://eur-lex.europa.eu/eli/reg_del/2018/389/oj) — SCA elements, attempts, dynamic linking, exemptions and TRA bands (questions 21–22).
- [EPC — SEPA Credit Transfer Rulebook 2025 (PDF)](https://europeanpaymentscouncil.eu/sites/default/files/kb/file/2024-11/EPC125-05%202025%20SCT%20Rulebook%20version%201.0.pdf) — D+1, reject, return, recall and their time limits (questions 12, 14–15).
- [Regulation (EU) 2024/886 (Instant Payments Regulation)](https://eur-lex.europa.eu/eli/reg/2024/886/oj) — 10 seconds, customer limits, price parity, verification of payee, sanctions screening of customers (questions 12, 18).
- [ECB — Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) — the benchmark for showing an FX mark-up (question 10).
- [PCI SSC Document Library](https://www.pcisecuritystandards.org/document_library/) — PCI DSS v4.0.1: sensitive authentication data, masking, keyed hashes, no live PANs in test (questions 23, 25).
- [FATF Recommendations](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html) — risk-based approach, CDD, record keeping, suspicious transaction reporting, tipping-off (questions 18–20).
- [Regulation (EU) 2016/679 (GDPR)](https://eur-lex.europa.eu/eli/reg/2016/679/oj) — data minimisation, erasure and its legal-obligation exception, breach notification (questions 23–24).

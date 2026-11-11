# Glossary

[Русская версия](glossary.ru.md)

Key terms used in the areas.

| English | Русский | Meaning |
|---|---|---|
| 3-D Secure 2 (3DS2) | 3-D Secure 2 (3DS2) | EMVCo protocol for authenticating card-not-present payments |
| Account takeover (ATO) | Захват аккаунта | Criminal gains access to the customer's account and pays out |
| Account updater | Сервис обновления реквизитов (account updater) | Scheme service passing new PAN/expiry to card-on-file merchants |
| Acquirer | Эквайер | Merchant's bank or provider that accepts card payments for it |
| Activation | Активация | Client step that turns an inactive card into an active one |
| Allocation | Распределение (allocation) | Splitting a total so rounded parts add up exactly |
| AML/CFT | ПОД/ФТ | Anti-money laundering and countering the financing of terrorism |
| Anonymisation | Анонимизация | Data that can no longer identify a person; outside GDPR |
| Arbitration | Арбитраж | The scheme decides liability in a dispute |
| Asset | Актив | What the company has or is owed |
| Audit trail | Журнал аудита | Record of who changed what, when and why |
| Authorisation | Авторизация | Issuer's approval or decline; blocks funds but does not move them |
| Authorised push payment (APP) scam | Мошенничество с переводом, совершённым с согласия клиента под влиянием обмана (социальная инженерия; APP scam) | Customer is tricked into sending a payment themselves |
| Available balance | Доступный баланс | Ledger balance minus active holds |
| Banking business day | Банковский рабочий день | Day a PSP and T2 are open for execution |
| BBAN | BBAN | National part of the IBAN with a country-specific layout |
| Beneficial owner | Бенефициарный владелец | Natural person who ultimately owns or controls a customer |
| BIC | BIC | Code identifying a payment service provider |
| BIN / IIN | BIN / IIN | Leading PAN digits identifying the issuer (ISO/IEC 7812); moving from 6 to 8 digits |
| Booking date | Дата проводки | Date the entry is recorded |
| Boundary value analysis | Анализ граничных значений | Testing just below, at and above each limit |
| Breach notification | Уведомление об утечке | Report to the supervisory authority within 72 hours where feasible |
| Break | Расхождение | Unmatched or unequal item found by reconciliation |
| Capture | Списание (capture) | Merchant's instruction to charge an approved payment for the final amount |
| Card on file | Сохранённая карта (card on file) | Card details stored by a merchant for later or recurring charges |
| Card scheme | Платёжная система | Network such as Visa or Mastercard that routes messages and sets rules |
| Card-not-present (CNP) fraud | Мошенничество без присутствия карты | Stolen card details used online or by phone |
| Cardholder | Держатель карты | Person who pays with the card |
| Cardholder data environment (CDE) | Среда данных держателей карт (CDE) | Systems that store, process or transmit account data |
| CDD (customer due diligence) | Надлежащая проверка клиента (CDD) | AML duty: identify and verify, beneficial owner, purpose, ongoing monitoring |
| Challenge flow | Аутентификация с проверкой (challenge) | Issuer asks the customer to authenticate actively |
| Chargeback | Чарджбэк | Issuer-initiated return of funds under scheme dispute rules |
| Chart of accounts | План счетов | List of all ledger accounts of a company |
| Check digit | Контрольная цифра | Last PAN digit computed with the Luhn algorithm |
| Clearing (presentment) | Клиринг (presentment) | Sending final transaction records from acquirer to issuer through the scheme |
| Control account | Синтетический счёт (control account) | GL account that must equal the subledger total |
| Credit (Cr) | Кредит (Кт) | Right side of an entry; increases liabilities, equity and income |
| Credit transfer | Кредитовый перевод | Payment pushed by the payer to the payee |
| Currency exponent | Количество десятичных знаков валюты (currency exponent) | Number of minor-unit digits per ISO 4217 (EUR 2, JPY 0, BHD 3) |
| Cut-off | Отсечка (время отсечения) | Moment separating one posting day or period from the next |
| Cut-off time | Время отсечения (cut-off; в российских правилах — время окончания приёма распоряжений) | Latest time an order counts as received today |
| CVV2 / CVC2 | Код проверки карты (CVV2 / CVC2) | 3–4 digit code for card-not-present payments; never stored after authorisation |
| Data masking | Маскирование данных | Replacing real values in a production copy with fake ones |
| Data minimisation | Минимизация данных | GDPR principle: collect only data needed for the purpose |
| Debit (Dr) | Дебет (Дт) | Left side of an entry; increases assets and expenses |
| Decision table | Таблица решений | Combinations of conditions mapped to expected outcomes |
| Direct debit | Прямое дебетование | Payment pulled by the payee from the payer's account under a mandate |
| Double spending | Двойная трата | Spending the same money twice, e.g. through a race condition |
| Double-entry bookkeeping | Двойная запись | Every event is recorded as ≥ 2 entries whose debits equal credits |
| DST (daylight saving time) | Летнее время (DST) | Clock change that creates a missing hour and a repeated hour |
| Duplicate detection | Выявление дублей | Business check for same payee, amount and reference in a short window |
| Dynamic Currency Conversion (DCC) | Динамическая конвертация валюты | Merchant offers to charge in the cardholder's currency at its own rate |
| Dynamic linking | Динамическая привязка | Authentication code tied to the exact amount and payee |
| ECB reference rate | Референсный курс ЕЦБ | Daily euro rates published by the ECB for information |
| EDD (enhanced due diligence) | Усиленные меры надлежащей проверки клиента (EDD) | Extra CDD measures for higher risk, e.g. PEPs |
| eID / eIDAS | eID / eIDAS | Electronic identification; EU framework with assurance levels |
| End of day / end of month (EOD/EOM) | Закрытие дня / месяца | Scheduled close: reconciliations, snapshots, revaluation, lock |
| End-to-end ID | End-to-end ID | Payer's reference passed unchanged through the whole chain |
| Entry / posting | Проводка | One line changing one account by an amount on one side |
| Equivalence partitioning | Классы эквивалентности | One test per group of inputs that behave the same |
| Fail-closed / fail-open | Отказ при сбое / пропуск при сбое | Decline vs approve when a control service is unavailable |
| False hit (sanctions) | Ложное срабатывание (скрининг) | Screening match that is not the listed person |
| False negative | Пропуск (ложноотрицательное срабатывание) | Fraudulent payment approved |
| False positive | Ложноположительное срабатывание | Genuine payment flagged or blocked |
| Fee income | Комиссионный доход | Income account for commissions charged |
| FIU (financial intelligence unit) | Подразделение финансовой разведки (FIU) | Authority that receives suspicious transaction reports |
| Four-party model | Четырёхсторонняя модель | Cardholder, merchant, acquirer and issuer connected through a card scheme |
| Frictionless flow | Аутентификация без участия клиента (frictionless) | Issuer authenticates by risk data without asking the customer |
| Friendly fraud (first-party fraud) | «Дружественный» фрод | Genuine cardholder falsely disputes their own purchase |
| Fuzzy matching | Нечёткое сравнение | Name comparison by similarity score and threshold |
| FX quote / quote expiry | Котировка / срок действия котировки | Rate offered to the customer, valid until an expiry time |
| GDPR | GDPR | EU Regulation 2016/679 on personal data |
| General ledger (GL) | Главная книга | Ledger of all accounts with totals |
| Half-even (banker's) rounding | Банковское округление (half-even) | A tie rounds to the nearest even digit |
| Half-up rounding | Округление половины вверх (half-up) | A tie (…5) rounds away from zero |
| Hold (blocked funds) | Холд (блокировка средств) | Amount reserved on the account after an approval |
| IBAN | IBAN | International identifier of one payment account |
| IBAN Registry | Реестр IBAN | SWIFT-published list of national IBAN formats |
| Idempotency key | Ключ идемпотентности | Unique request id so a retry returns the first result |
| Immutability | Неизменяемость | Posted entries are never edited or deleted |
| Incremental authorisation | Инкрементальная авторизация | Additional authorisation linked to the original one |
| Interchange fee | Интерчейндж (межбанковское вознаграждение, МБВ) | Fee the acquirer pays the issuer per purchase |
| ISO 20022 | ISO 20022 | Standard for financial XML messages |
| ISO 4217 | ISO 4217 | Standard for currency codes and minor units |
| Issuer | Эмитент | Cardholder's bank that issued the card and holds the account |
| Journal entry | Бухгалтерская запись | A balanced group of entries describing one business event |
| Keyed hash | Ключевой хеш | Hash computed with a secret key (e.g. HMAC) |
| KYB (know your business) | KYB («знай бизнес клиента») | KYC for companies: register check, representatives, beneficial owners |
| KYC (know your customer) | KYC («знай своего клиента») | Knowing and verifying who the customer is before and during the relationship |
| Lawful basis | Законное основание | Legal ground required for each processing of personal data |
| Ledger balance | Учётный баланс | Balance of posted transactions only |
| Liability | Обязательство | What the company owes others, e.g. customer e-money |
| Liability shift | Перенос ответственности | Fraud loss moves from merchant to issuer, e.g. after 3-D Secure |
| Live PAN | Реальный PAN | Real card number; not used in pre-production unless that environment is in the CDE and protected like it (PCI DSS 6.5.5) |
| Liveness detection | Проверка живости (liveness) | Check that a live person is present, not a photo, video or mask |
| Lost update | Потерянное обновление | Two parallel writes where one overwrites the other |
| Luhn algorithm (mod 10) | Алгоритм Луна (mod 10) | Check-digit method for PANs; catches single-digit errors and most adjacent swaps |
| Mandate | Мандат | Payer's consent allowing a creditor to collect direct debits |
| Mark-up (FX) | Наценка (mark-up) | Margin added to a reference rate; in the EU shown as % over the ECB rate |
| Masking | Маскирование | Showing at most BIN and last four digits of a PAN |
| Matching key | Ключ сопоставления | Field(s) used to pair our record with the partner's in reconciliation |
| Merchant | Мерчант (торгово-сервисное предприятие, ТСП) | Business that accepts card payments |
| Merchant-initiated transaction (MIT) | Платёж по инициативе мерчанта (MIT) | Payment started by the payee under a mandate, outside SCA |
| Mid rate | Средний курс (mid rate) | Midpoint between market buy and sell rates |
| Minor unit | Разменная денежная единица (minor unit) | Smallest unit of a currency; amounts often stored as an integer of it |
| MOD 97-10 (ISO 7064) | MOD 97-10 (ISO 7064) | IBAN checksum: rearranged number mod 97 must equal 1 |
| Network token | Сетевой токен | Token issued by a scheme token service, linked to the PAN in a vault |
| Onboarding | Онбординг | The sign-up funnel from account creation to an opened, verified account |
| Ongoing monitoring | Постоянный мониторинг | Continuous review of the relationship against the customer profile |
| Overdraft | Овердрафт | Agreed credit line allowing a balance below zero up to a limit |
| PAN (Primary Account Number) | PAN (номер карты) | The card number identifying the card account |
| Partial authorisation | Частичная авторизация | Issuer approves less than the requested amount |
| Payment token | Платёжный токен | Substitute number used instead of the PAN |
| PCI DSS | PCI DSS | Card industry data security standard, current v4.0.1 |
| Pending balance | Ожидающий баланс (pending) | Incoming funds announced but not yet spendable |
| PEP (politically exposed person) | Публичное должностное лицо (ПДЛ, PEP) | Person with a prominent public function, plus family and close associates |
| Posting rule | Правило проводок | Mapping from a business event to accounts and sides |
| Pre-authorisation | Преавторизация | Authorisation of an estimated amount when the final amount is unknown |
| Precision / recall | Точность / полнота | Share of flagged that is fraud / share of fraud that is flagged |
| PSD2 | PSD2 (Вторая платёжная директива) | EU directive 2015/2366 on payment services |
| Pseudonymisation | Псевдонимизация | Data linkable back via a separate key; still personal data |
| R-transaction | R-транзакция | Any exception to normal payment processing (reject, return, recall) |
| Race condition | Состояние гонки (race condition) | Parallel requests acting on stale data |
| Recall | Отзыв (recall) | Payer's PSP request to cancel a sent transfer |
| Reconciliation | Сверка | Matching ledger with subledger, bank or scheme files |
| Refund | Возврат | New credit transaction from the merchant after clearing |
| Reissue | Перевыпуск | New card for the same account (damage etc.) |
| Renewal | Продление | New card before expiry, usually same PAN, new expiry and CVV2 |
| Representment | Повторное представление (representment) | Merchant/acquirer defends against a chargeback with evidence |
| Revaluation | Переоценка | Re-measuring foreign-currency balances at the closing rate |
| Reversal (card authorisation) | Отмена авторизации (reversal) | Cancels all or part of an authorisation before clearing |
| Reversal / storno (accounting) | Сторно | Mirror entry that cancels an earlier one |
| Right to erasure | Право на удаление | Right to deletion, limited by legal obligations such as AML |
| Risk score | Риск-скор | Number estimating how risky a payment is |
| Risk-based approach | Риск-ориентированный подход | Stronger controls where ML/TF risk is higher |
| Rolling window | Скользящее окно | Period counted back from now (e.g. last 24 h), not a calendar day |
| RTS on SCA | RTS по SCA | Delegated Regulation (EU) 2018/389 with detailed SCA rules and exemptions |
| Rules engine | Движок правил | Component that applies ordered if-then rules |
| Safeguarding | Защита средств клиентов | Keeping customer funds segregated or insured, protected in insolvency |
| Sanctions screening | Санкционный скрининг | Comparing names with sanctions lists |
| Sandbox (test mode) | Песочница (тестовый режим) | Separate PSP environment with test keys where no money moves |
| SCA exemption | Исключение из SCA | Case where the PSP may skip SCA under the RTS |
| Screening | Скрининг | Matching names against sanctions and PEP lists |
| SCT (SEPA Credit Transfer) | SCT (SEPA-перевод) | Standard euro credit transfer, executed by D+1 on business days |
| SCT Inst | SCT Inst (мгновенный SEPA-перевод) | Instant euro credit transfer, 24/7, within 10 seconds |
| SDD (simplified due diligence) | Упрощённые меры надлежащей проверки клиента (SDD) | Lighter CDD where lower risk is assessed and documented |
| Seeding | Наполнение (seeding) | Script that loads a known baseline or demo data set |
| Sensitive authentication data | Чувствительные аутентификационные данные | PCI DSS term: CVV, PIN/PIN block, full track/chip data |
| SEPA | SEPA | Area where euro payments work the same across borders as at home |
| Settlement | Расчёты (settlement) | Actual movement of money between issuer, scheme, acquirer and merchant |
| Shadow mode | Теневой режим | New rule records its decisions without affecting live ones |
| Soft decline | Мягкий отказ | Issuer decline asking the merchant to retry with SCA |
| State transition testing | Тестирование переходов состояний | Testing allowed and forbidden status changes |
| Step-up authentication | Усиленная аутентификация (step-up) | Asking for stronger authentication before approving |
| Strong Customer Authentication (SCA) | Строгая аутентификация клиента (SCA) | Authentication with two elements from different categories |
| Structuring (smurfing) | Дробление (структурирование) | Splitting money into amounts just below a threshold |
| Subledger | Аналитический учёт (subledger) | Detailed ledger, e.g. per-customer balances |
| Suspense / transit account | Счёт невыясненных / транзитных сумм (в российском плане счетов — суммы до выяснения) | Temporary account for unidentified or in-flight money; must be cleared |
| Suspicious activity report (SAR/STR) | Сообщение о подозрительной операции | Report of suspected ML/TF to the FIU |
| Synthetic data | Синтетические данные | Generated data with a valid format but fake content |
| Synthetic identity | Синтетическая личность | Fake identity from invented or mixed data; in tests, a fictional profile |
| TARGET closing day | Нерабочий день TARGET | Day T2 is closed (weekends, 1 Jan, Easter Fri/Mon, 1 May, 25–26 Dec) |
| Test card number | Тестовый номер карты | PSP-published card number that triggers a set outcome only in that PSP's sandbox |
| Test data factory / builder | Фабрика / билдер тестовых данных | Function that creates a valid test object with defaults |
| Tiered fee | Ступенчатая комиссия | Rate depends on amount tiers |
| Tipping-off prohibition | Запрет на разглашение (tipping-off) | Ban on telling the customer about a report or investigation |
| Transaction monitoring | Мониторинг транзакций | Scenarios over many payments to find suspicious patterns |
| Transaction risk analysis (TRA) | Анализ риска транзакции (TRA) | Exemption based on real-time risk scoring and the PSP's fraud rate |
| Transliteration | Транслитерация | Writing a name in another alphabet by a defined rule |
| Trial balance | Оборотно-сальдовая ведомость | List of all account balances; total debits must equal total credits |
| Unicode normalisation (NFC/NFD) | Нормализация Unicode (NFC/NFD) | Composed vs decomposed forms of the same character |
| Value date | Дата валютирования | Date the money actually counts or settles |
| Velocity limit | Лимит частоты | Maximum number of events in a time window |
| Verification of payee (VoP) | Проверка получателя (VoP) | Check that the payee's name matches the IBAN before authorisation |
| Virtual card | Виртуальная карта | Card that exists only as data in an app |

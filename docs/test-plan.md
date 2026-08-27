# 📋 Test Plan — Fintech API

## 1. Scope

API testing for a fintech platform covering authentication, account management, transactions and payments.

## 2. Test Objectives

- Verify API endpoints return correct HTTP status codes
- Validate response schemas (JSON structure & data types)
- Check business logic (balance calculations, transaction limits)
- Ensure proper error handling (4xx, 5xx responses)
- Confirm authentication & authorization rules

## 3. Test Types

| Type | Tool | Trigger |
|------|------|---------|
| Functional | Postman / Newman | Every push (CI) |
| Regression | Newman | Every push (CI) |
| Exploratory | Postman | Manual |

## 4. Coverage Matrix

### 🔐 Authentication
| Test Case | Method | Endpoint | Expected | Priority |
|-----------|--------|----------|----------|----------|
| Valid login | POST | `/auth/login` | 200 + token | High |
| Invalid password | POST | `/auth/login` | 401 | High |
| Missing credentials | POST | `/auth/login` | 400 | High |
| Token expiry | GET | `/auth/refresh` | 200 + new token | Medium |

### 💰 Accounts
| Test Case | Method | Endpoint | Expected | Priority |
|-----------|--------|----------|----------|----------|
| Get own account | GET | `/accounts/{id}` | 200 + data | High |
| Get another user's account | GET | `/accounts/{id}` | 403 | High |
| Non-existent account | GET | `/accounts/{id}` | 404 | Medium |

### 💸 Transactions
| Test Case | Method | Endpoint | Expected | Priority |
|-----------|--------|----------|----------|----------|
| List transactions | GET | `/transactions` | 200 + array | High |
| Create transaction | POST | `/transactions` | 201 | High |
| Insufficient funds | POST | `/transactions` | 422 | High |
| Invalid amount | POST | `/transactions` | 400 | Medium |

### 📤 Payments
| Test Case | Method | Endpoint | Expected | Priority |
|-----------|--------|----------|----------|----------|
| Create payment | POST | `/payments` | 201 | High |
| Duplicate payment | POST | `/payments` | 409 | Medium |
| Payment to invalid account | POST | `/payments` | 404 | High |

## 5. Entry / Exit Criteria

**Entry:** API environment is up, test data is seeded, token is valid

**Exit:** All High priority tests pass, no P1 bugs open

## 6. Risks

| Risk | Mitigation |
|------|------------|
| Real API unavailable in CI | Use mock server (Postman Mock / WireMock) |
| Token leaking via logs | Use GitHub Secrets, mask values in CI |
| Test data pollution | Cleanup scripts in collection teardown |
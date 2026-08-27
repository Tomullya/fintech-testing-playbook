# 💳 fintech-qa-portfolio

> QA portfolio project — API testing for fintech domain. Postman, Newman, GitHub Actions.

![CI](https://github.com/Tomullya/fintech-qa-portfolio/actions/workflows/newman.yml/badge.svg)

## 📋 Overview

This repository demonstrates QA engineering skills applied to a fintech API domain:
- REST API test collections (Postman)
- Automated regression runs (Newman + GitHub Actions)
- Structured test plan & coverage documentation

## 🗂 Project Structure

```
fintech-qa-portfolio/
├── postman/
│   ├── collections/          # Postman collection JSON files
│   └── environments/         # *.example.json only — no real tokens!
├── .github/
│   └── workflows/
│       └── newman.yml        # CI: auto-run tests on every push
├── docs/
│   └── test-plan.md          # Test plan & coverage matrix
└── .gitignore                # Protects secrets from accidental commit
```

## 🚀 How to Run Locally

### Prerequisites
```bash
npm install -g newman newman-reporter-htmlextra
```

### Run collection
```bash
newman run postman/collections/fintech-api.json \
  --environment postman/environments/local.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/report.html
```

> ⚠️ `local.json` is listed in `.gitignore` — create it from `local.example.json`, never commit real tokens!

## 🔐 Security Notes

| File | Status | Reason |
|------|--------|--------|
| `postman/environments/local.json` | 🚫 git-ignored | Contains real API tokens |
| `config.yaml` | 🚫 git-ignored | May contain secrets |
| `.continue/` | 🚫 git-ignored | AI assistant config with tokens |
| `postman/environments/local.example.json` | ✅ tracked | Template only, no real values |

## 🧪 Test Coverage

| Domain | Endpoint | Methods | Status |
|--------|----------|---------|--------|
| Auth | `/auth/login` | POST | 🟡 planned |
| Accounts | `/accounts/{id}` | GET | 🟡 planned |
| Transactions | `/transactions` | GET, POST | 🟡 planned |
| Payments | `/payments` | POST | 🟡 planned |

## 🛠 Tech Stack

- [Postman](https://www.postman.com/) — API test authoring
- [Newman](https://github.com/postmanlabs/newman) — CLI collection runner
- [GitHub Actions](https://github.com/features/actions) — CI/CD pipeline
- [newman-reporter-htmlextra](https://github.com/DannyDainton/newman-reporter-htmlextra) — HTML reports
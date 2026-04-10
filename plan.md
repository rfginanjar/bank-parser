# Bank Statement Processor — Technical Plan

**Project:** Professional-grade web application for OCR-based bank statement processing with human-in-the-loop validation
**Status:** Draft | Spec Ready | In Progress | Complete
**Version:** 1.0
**Date:** 2026-04-10
**Owner:** Development Team

---

## Project Summary

A web application that processes bank statements (e.g., BCA Tahapan) using OCR technology, stores transaction data relationally, and provides a validation UI for users to review and correct extracted data before final commit. The system serves individuals and businesses needing to digitize, categorize, and analyze their banking history.

### Success Criteria

- [ ] User can upload statement and see extracted transactions within 30 seconds
- [ ] Transaction extraction accuracy ≥95% after human validation
- [ ] Support for multiple bank accounts with monthly history view
- [ ] CSV export functionality working
- [ ] Zero data loss during processing pipeline

### Non-Goals

- No real-time bank integration (file upload only)
- No multi-user collaboration in MVP
- No mobile-responsive design in v1
- No AI-powered auto-categorization beyond keyword matching

---

## Architecture

### Core Philosophy

Asynchronous OCR processing with human-in-the-loop validation ensures data accuracy while maintaining responsive UX.

### Tech Stack

| Component | Technology | Rationale |
|-----------|------------|----------|
| Frontend | React.js or Next.js | Modern component-based UI for complex data tables |
| Backend | Python FastAPI | High performance async API, excellent data processing library support |
| Database | PostgreSQL | Relational data integrity for accounts, statements, transactions |
| File Storage | AWS S3 / Google Cloud Storage | Scalable, secure storage for uploaded statement images/PDFs |
| OCR Engine | AWS Textract (Pro) or Tesseract (DIY) | Textract handles tables perfectly; Tesseract for DIY approach |
| Task Queue | Celery + Redis | Handles 10-30 second OCR processing without blocking UI |
| Auth | JWT tokens | Stateless authentication suitable for distributed processing |

### Design Decisions

| ID | Decision | Chosen Option | Rationale |
|----|----------|---------------|-----------|
| D-001 | OCR service | Cloud-based Textract vs DIY Tesseract | Textract provides superior table extraction; reduces custom parser complexity |
| D-002 | Data validation | Human review before commit vs auto-commit | OCR errors inevitable; human validation ensures data integrity |
| D-003 | File storage | Cloud object storage vs local filesystem | Scalability, backup, and secure signed URL access |
| D-004 | Queue implementation | Celery+Redis vs async/await only | Decouples processing from request-response cycle; handles retries |

---

## Substrate Layer Map

Links this plan to actual files in the stratvibe substrate.

### spec/architecture/ — Intent & Constraints

| Decision | Status | File |
|----------|--------|------|
| Architecture Overview | pending | spec/architecture/overview.md |
| Tech Stack Selection | pending | spec/architecture/tech-stack.md |
| Security & Privacy | pending | spec/architecture/security.md |

### spec/api/ — Contracts

| Contract | Status | File |
|----------|--------|------|
| Upload API | pending | spec/api/upload.md |
| OCR Processing API | pending | spec/api/ocr-processing.md |
| Transaction Validation API | pending | spec/api/validation.md |
| Dashboard API | pending | spec/api/dashboard.md |

### spec/components/ — Behavioral Definitions

| Component | Status | File |
|-----------|--------|------|
| Upload Component | pending | spec/components/upload.md |
| OCR Parser | pending | spec/components/ocr-parser.md |
| Validation UI | pending | spec/components/validation-ui.md |
| Dashboard | pending | spec/components/dashboard.md |
| Transaction Table | pending | spec/components/transaction-table.md |

### tasks/ — Bounded Work Units

| Task | Sprint | Blocked By | File |
|------|--------|------------|------|
| Database Schema Setup | sprint1 | -- | tasks/sprint1/database-schema.md |
| Authentication System Implementation | sprint1 | -- | tasks/sprint1/auth.md |
| Upload Endpoint Implementation | sprint1 | -- | tasks/sprint1/upload-endpoint.md |
| Celery Task Queue Setup | sprint1 | -- | tasks/sprint1/task-queue.md |
| Basic OCR Integration (Tesseract) | sprint1 | -- | tasks/sprint1/ocr-integration.md |
| Simple Transaction Parser | sprint1 | -- | tasks/sprint1/transaction-parser.md |
| PendingReview & Validation API | sprint1 | -- | tasks/sprint1/validation-api.md |
| React Frontend Setup | sprint2 | -- | tasks/sprint2/frontend-setup.md |
| Upload UI Component | sprint2 | -- | tasks/sprint2/upload-ui.md |
| Validation UI (Data Table) | sprint2 | T-007 | tasks/sprint2/validation-ui.md |
| CSV Export Feature | sprint2 | -- | tasks/sprint2/csv-export.md |
| Dashboard with Stats | sprint2 | -- | tasks/sprint2/dashboard.md |
| End-to-End MVP Testing | sprint2 | -- | tasks/sprint2/e2e-testing.md |

### snippets/ — Reusable Patterns

| Pattern | Language | File |
|---------|----------|------|
| Multi-line buffer parser | Python | snippets/ocr/buffer-parser.py |
| Transaction deduplication | Python | snippets/db/deduplication.py |
| S3 signed URL generation | Python | snippets/storage/signed-urls.py |
| Data table component | React | snippets/ui/data-table.jsx |
| Floating action button | React | snippets/ui/fab.jsx |

### atomic/ — Lookups & Constants

| Key | Value / Range | File |
|-----|---------------|------|
| BANK_NAMES | ["BCA", "Mandiri", "BNI", "BRI"] | atomic/configs/banks.json |
| TRANSACTION_TYPES | ["Debit", "Credit"] | atomic/configs/types.json |
| SPENDING_CATEGORIES | ["Food", "Transport", "Transfer", "Shopping", "Entertainment", "Bills", "Salary", "Other"] | atomic/configs/categories.json |
| OCR_ENGINES | ["textract", "tesseract"] | atomic/configs/ocr-engines.json |
| ERR-OCR-001 | "OCR extraction failed" | atomic/errors/ocr-errors.json |
| ERR-VAL-001 | "Validation timeout" | atomic/errors/validation-errors.json |

---

## Code Organization

```text
/src-root/
    backend/
        app/
            main.py              # FastAPI app entry
            api/
                upload.py
                transactions.py
                validation.py
                dashboard.py
            core/
                config.py
                security.py
            models/
                user.py
                account.py
                statement.py
                transaction.py
            services/
                ocr_service.py
                parser_service.py
                storage_service.py
                validation_service.py
            tasks/
                ocr_task.py
            utils/
                buffer_parser.py
                deduplication.py
        celery_worker.py
    frontend/
        src/
            components/
                UploadButton.jsx
                TransactionTable.jsx
                ValidationModal.jsx
                Dashboard.jsx
                Sidebar.jsx
            pages/
                upload.jsx
                dashboard.jsx
                validation.jsx
            services/
                api.js
            utils/
                format.js
        public/
    shared/
        constants.js
        types.js
```

### Module Responsibilities

| Module | Purpose | Depends On |
|--------|---------|------------|
| backend/app/api | HTTP endpoints | models, services, tasks |
| backend/app/services | Business logic (OCR, parsing, validation) | models, utils |
| backend/app/models | Database schema | none |
| backend/app/tasks | Celery async workers | services |
| frontend/components | Reusable UI elements | services/api |
| frontend/pages | Route handlers | components |

### Key Patterns

- All OCR processing in Celery tasks with status tracking in database
- PendingReview table for transactions awaiting user validation
- Buffer parser for multi-line transaction descriptions
- S3 signed URLs with short expiration for secure file access
- Transaction deduplication using (date, amount, balance) composite check

---

## Data Model

### Core Entities

**Users** — System authentication and ownership

```yaml
id: uuid          # Primary key
email: string     # Unique, used for login
password_hash: string
created_at: timestamp
```

**Accounts** — Bank accounts owned by users

```yaml
id: uuid
user_id: uuid     # Foreign key to Users
account_number: string   # Encrypted in database
account_name: string
bank_name: string
created_at: timestamp
```

**Statements** — Uploaded bank statement files

```yaml
id: uuid
account_id: uuid  # Foreign key to Accounts
period_month: integer      # 1-12
period_year: integer       # e.g., 2026
file_url: string           # S3 path
file_hash: string          # For duplicate detection
upload_date: timestamp
status: enum              # pending, processing, extracted, validated, committed
```

**Transactions** — Extracted transaction data

```yaml
id: uuid
statement_id: uuid         # Foreign key to Statements
date: date
description: string
mutation_amount: decimal   # Negative for debit, positive for credit
type: enum                # Debit, Credit
balance: decimal          # Running balance after this transaction
category: string          # User-assigned or auto-categorized
created_at: timestamp
```

**PendingReview** — Temporary storage for OCR results needing validation

```yaml
id: uuid
statement_id: uuid
raw_transactions: jsonb    # Array of extracted but unvalidated transactions
validation_token: uuid     # For secure access to validation UI
expires_at: timestamp
```

### Relationships

```
Users 1-to-N Accounts
Accounts 1-to-N Statements
Statements 1-to-N Transactions
Statements 1-to-1 PendingReview (optional, during validation)
```

### Invariants

1. Transaction `mutation_amount` sign must match `type` (Debit negative, Credit positive)
2. Every `Statement` must have at least one `Transaction` or be marked as empty
3. `balance` must be consistent with previous transaction's balance plus current `mutation_amount`
4. Duplicate prevention: (statement_id, date, mutation_amount, balance) must be unique
5. PendingReview cannot exist after Statement status is "committed"

---

## Testing Strategy

| Type | Tool | Scope | Location |
|------|------|-------|----------|
| Unit | pytest | Backend services, utils | tests/unit/ |
| Integration | pytest | API endpoints with test database | tests/integration/ |
| E2E | Playwright or Cypress | Full upload → validation → commit flow | tests/e2e/ |
| OCR Accuracy | Custom script | Parser output vs ground truth | tests/ocr/ |

### Critical Test Cases

1. Upload valid PDF → response 202 with statement_id → OCR task queued → status becomes "processing"
2. Invalid file type → response 400 with error message
3. OCR returns malformed data → validation UI shows all fields editable → user corrections saved
4. Duplicate statement upload → detected by file_hash → response 409 with "already processed"
5. Multi-line description → buffer parser correctly concatenates continuation lines
6. Concurrent validation requests → second request rejected with "already validated"
7. Expired validation token → redirect to login or show error

---

## Operations

### Local Development

```bash
# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate (Windows) or source venv/bin/activate (Unix)
pip install -r requirements.txt
createdb bankstatements_dev

# Run API
uvicorn app.main:app --reload

# Run Celery worker
celery -A celery_worker worker --loglevel=info

# Frontend setup
cd frontend
npm install
npm run dev

# Run tests
pytest tests/
npm test
```

### Deployment / Delivery

```
1. Build Docker images for backend and frontend
2. Push to container registry
3. Deploy to AWS ECS / GCP Cloud Run with:
   - PostgreSQL RDS instance
   - Redis ElastiCache
   - S3 bucket with versioning and encryption
   - AWS Textract if using cloud OCR
4. Set up Celery beat for periodic cleanup of expired PendingReview
5. Configure monitoring (CloudWatch logs, Sentry errors)
```

---

## Constraints & Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| OCR accuracy varies by bank format | high | Implement bank-specific parsers; allow manual correction |
| S3 costs for large image storage | medium | Implement cleanup policy; compress images on upload |
| Celery worker crashes mid-processing | high | Implement idempotent tasks; retry logic with exponential backoff |
| Slow OCR processing (30s+) frustrates users | medium | Clear status indicators; WebSocket or SSE progress updates |
| PII data in database (account numbers) | high | Encrypt at rest; restrict DB access; audit logs |
| DDoS on upload endpoint | medium | Rate limiting per user; file size limits |

---

## Sprint Plan

### Sprint 1 — MVP Infrastructure & Backend (Week 1-2)

| Task | Estimate | Status |
|------|----------|--------|
| Database schema implementation | small | pending |
| User authentication (login/signup) | medium | pending |
| Upload endpoint with S3 storage | small | pending |
| Celery task queue setup | medium | pending |
| Basic OCR integration (Tesseract) | medium | pending |
| Simple transaction parser | medium | pending |
| PendingReview table & validation API | small | pending |

### Sprint 2 — MVP UI & Features (Week 3-4)

| Task | Estimate | Status |
|------|----------|--------|
| Basic React frontend setup | small | pending |
| Upload button component | small | pending |
| Validation UI (React data table) | large | pending |
| CSV export functionality | small | pending |
| Basic transaction table view | medium | pending |
| Dashboard with current month stats | medium | pending |
| End-to-end testing of upload → validation → export flow | medium | pending |

### Backlog (Post-MVP)

- Account switching sidebar for multiple accounts
- Auto-categorization (keyword matching)
- Transaction search
- Charts and visualizations
- AWS Textract integration
- Multi-bank format auto-detection
- Mobile responsive design
- Budget planning features

---

## References

- Draft plan: draft.md
- Substrate protocol: .substrate/substrate-summary.md
- AWS Textract documentation
- PostgreSQL documentation
- Celery distributed task documentation

---

This is the human-facing entry point for Bank Statement Processor.
Substrate structure managed by stratvibe. Decisions tracked in spec/.

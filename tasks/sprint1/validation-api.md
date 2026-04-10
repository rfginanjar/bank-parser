---
title: PendingReview & Validation API
acceptance_criteria:
  - Implement GET /statements?status=pending with JWT filter (user's own)
  - Implement POST /transactions/validate with token verification
  - On validate, set transaction status='committed' and link to user's ledger
  - Write tests for listing and validation flow
blocked_by:
  - Database Schema Implementation
  - Transaction Parser Implementation
sprint: sprint1
effort: small
---

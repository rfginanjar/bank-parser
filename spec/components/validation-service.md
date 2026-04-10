---
decision: Implement validation service that applies user corrections to parsed transactions, enforces deduplication, assigns categories (default or user-provided), and commits transactions to the database. Updates Statement status to 'committed' upon success.
constraints:
  - Enforce unique constraint on (statement_id, date, mutation_amount, balance) to prevent duplicates
  - Process transactions in a single database transaction
  - Allow category override and default categorization rules
  - Rollback on any validation error
rationale: Ensures data integrity and finality of approved transactions while preventing duplicates.
affects:
  - backend/services/validation
  - backend/models
  - backend/api/validation
---
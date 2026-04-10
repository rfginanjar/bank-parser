---
decision: Implement database schema with tables Users, Accounts, Statements, Transactions, PendingReview, and relationships as specified. Include encryption for account_number and unique constraint on (statement_id, date, mutation_amount, balance).
constraints:
  - Encrypt account_number at rest
  - Unique (statement_id, date, mutation_amount, balance)
  - Foreign keys: Accounts.user_id → Users.id, Statements.account_id → Accounts.id, Transactions.statement_id → Statements.id, PendingReview.statement_id → Statements.id
  - Indexes on foreign keys and frequently queried fields
rationale: Provides a robust data model ensuring data integrity, security, and supporting core business operations.
affects:
  - backend/models
  - backend/database/migrations
  - backend/services
---
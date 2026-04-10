---
decision: Implement GET /dashboard/stats endpoint returning monthly aggregated transaction totals (income, expenses, net) for authenticated user, optionally filtered by account_id, month, and year. Include count of transactions.
constraints:
  - Must authenticate user and filter by user's accounts only
  - Support optional query parameters: account_id, month (1-12), year (e.g., 2026)
  - Return JSON with totals: credit_total, debit_total, net_change, transaction_count
  - Use database aggregation queries for performance
rationale: Provides key financial metrics for dashboard overview, enabling users to quickly understand spending patterns.
affects:
  - backend/api/dashboard
  - frontend/dashboard
  - backend/models/transaction
---
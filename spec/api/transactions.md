---
decision: Implement GET /transactions endpoint with flexible filtering (account_id, date range, category, search) and pagination. Add GET /transactions/export/csv returning CSV of filtered transactions with proper headers.
constraints:
  - Require authentication and filter by user's accounts
  - Support query params: account_id, start_date, end_date, category, search (description), page, per_page
  - Return consistent date format (ISO 8601) and decimal precision (2 places)
  - CSV export includes header row with column names and same data as list response
  - Use efficient queries with indexes on account_id, date, category
rationale: Enables transaction browsing, filtering, and data export for external analysis.
affects:
  - backend/api/transactions
  - backend/models/transaction
  - frontend/transaction-table
  - frontend/csv-export
---
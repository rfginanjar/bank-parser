---
decision: Create GET /accounts endpoint listing all bank accounts owned by authenticated user with id, bank_name, masked_account_number, account_name, and created_at. Support optional query param 'bank' to filter by bank_name.
constraints:
  - Require authentication; return only accounts belonging to current user
  - Mask account numbers (show only last 4 digits) for security
  - Return sorted by bank_name then account_name
  - Include account id for filtering other endpoints
rationale: Enables account selection/switching in UI and provides necessary account context for transactions and dashboards.
affects:
  - backend/api/accounts
  - backend/models/account
  - frontend/account-switcher
---
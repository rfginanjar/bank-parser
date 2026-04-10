---
decision: Implement React AccountSwitcher component as a dropdown menu listing user's accounts (from GET /accounts) with option to select one or view "All Accounts". Show masked account number and bank icon/name.
constraints:
  - Fetch accounts on mount; cache for session
  - Highlight currently selected account; on change, update global state or callback
  - Include "All Accounts" option to aggregate data across all accounts
  - Search/filter within dropdown if more than 10 accounts
  - Accessible: keyboard navigation, proper roles, focus trap
  - Responsive: collapses to burger menu on small screens showing short account names
rationale: Allows users to switch context between accounts, essential for multi-account management.
affects:
  - frontend/components/account-switcher
  - frontend/state (React Context or Redux)
  - backend/api/accounts
  - frontend/layout/sidebar
---
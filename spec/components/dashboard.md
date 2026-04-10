---
decision: Build React Dashboard page with stats cards (income, expenses, net) for current month and a simple bar chart comparing monthly totals over last 6 months. Use Recharts library for charts.
constraints:
  - Fetch data from GET /dashboard/stats with optional account filter
  - Display 3 stat cards with formatted currency and percentage change vs previous month
  - Bar chart shows credit and debit totals per month for selected account (or all)
  - Responsive layout: stack cards on mobile; chart reflows
  - Handle loading and error states gracefully
  - Pull category list from atomic/ configs for potential future filtering
rationale: Gives users quick insights into their financial activity and trends.
affects:
  - frontend/pages/dashboard
  - frontend/components/dashboard-stats
  - frontend/components/chart
  - backend/api/dashboard
---
---
decision: Create React ValidationTable component displaying pending OCR transactions in editable rows with dropdown for category assignment and submit button to POST corrections to /pending-reviews/{token}/validate.
constraints:
  - Accept props: transactions array, validation_token, onSuccess, onError
  - Each row shows date, description, amount (editable fields), category (dropdown from SPENDING_CATEGORIES)
  - Inline editing with validation (amount numeric, date valid)
  - Submit disabled until at least one change made or all categories assigned
  - Show loading state during submission; handle errors gracefully
  - Use consistent table styling; support sorting on columns
  - Accessible: focus management, screen reader announcements
rationale: Enables human review and correction of OCR results to ensure data accuracy before commit.
affects:
  - frontend/components/validation-table
  - frontend/services/api
  - backend/api/validation
  - backend/services/validation
---
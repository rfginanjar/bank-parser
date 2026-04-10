---
decision: Provide GET /pending-reviews to list statements awaiting review and POST /pending-reviews/{token}/validate to accept corrected transactions. Use one-time token stored in PendingReview with expiration.
constraints:
  - Token must be cryptographically random and expire after 24 hours
  - One-time use only; invalidate after successful validation
  - Validation payload includes list of transactions with optional corrections
  - Return appropriate errors for invalid/expired tokens
rationale: Facilitates human-in-the-loop validation to ensure OCR accuracy and correct categorization.
affects:
  - backend/api/validation
  - backend/models/PendingReview
  - frontend/validation-ui
---
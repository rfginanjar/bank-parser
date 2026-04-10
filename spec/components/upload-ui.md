---
decision: Build React UploadButton component that accepts file drop or click, calls POST /upload with FormData, displays progress bar during upload, and handles success/error states with user feedback.
constraints:
  - Limit file types to PDF, JPG, PNG, max 10MB
  - Use XMLHttpRequest or fetch with progress tracking
  - Disable button during upload; show percentage or spinner
  - On success, dispatch event or callback with statement_id for downstream processing
  - Show error message (toast/inline) on failure with retry option
  - Accessible: keyboard support, ARIA labels
rationale: Provides user-friendly file submission with clear feedback, essential for upload workflow.
affects:
  - frontend/components/upload-button
  - backend/api/upload
  - frontend/services/api
---
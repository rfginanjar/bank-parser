---
decision: Create POST /upload endpoint that accepts bank statement files (PDF, images). Store file in S3 with unique key, create Statement record with status 'pending', and enqueue OCR processing task.
constraints:
  - Validate file type and size (max 10MB)
  - Generate S3 key with UUID and original extension
  - Compute file_hash (SHA-256) for deduplication
  - Return upload details including statement_id and status
rationale: Enables users to submit bank statements and initiates automated processing pipeline.
affects:
  - backend/api/upload
  - backend/services/s3
  - backend/tasks/ocr
  - backend/models
---
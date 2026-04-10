---
title: OCR Integration
acceptance_criteria:
  - Create Celery task process_statement(statement_id)
  - Call OCR service (Google Vision or Tesseract) on S3 file
  - Invoke transaction parser and store results in Transaction table
  - Update Statement status to 'review' or 'error' with retry logic
  - Write integration test with mocked OCR
blocked_by:
  - Celery Task Queue Setup
  - Transaction Parser Implementation
sprint: sprint1
effort: medium
---

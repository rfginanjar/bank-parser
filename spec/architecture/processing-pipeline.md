---
decision: Define processing pipeline with statuses: pending → processing → extracted → validated → committed. Use Celery for asynchronous task execution with retries and idempotency.
constraints:
  - Status transitions must be atomic
  - Idempotent task design
  - Retry mechanism with exponential backoff
  - Handle failures gracefully with dead-letter queue
rationale: Ensures reliable and scalable processing of uploaded statements through OCR and validation stages.
affects:
  - backend/services/processing
  - backend/tasks/celery
  - backend/api
---
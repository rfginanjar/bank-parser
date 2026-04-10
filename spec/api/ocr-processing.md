---
decision: Implement Celery task for OCR: convert PDF to images, run Tesseract to extract text, then call parser. Expose internal mechanism to trigger processing.
constraints:
  - Support PDF (via pdf2image) and image formats (jpeg, png, tiff)
  - Install Tesseract with required language packs (eng)
  - Set appropriate timeout for OCR task (e.g., 300s)
  - Retry on transient failures up to 3 times
rationale: Provides text extraction from scanned or image-based bank statements.
affects:
  - backend/services/ocr
  - backend/tasks/ocr
  - infrastructure/tesseract
---
---
decision: Build OCR parser that processes raw Tesseract output into structured transaction objects. Use line-by-line scanning with buffer for multi-line descriptions. Detect date, amount, balance, and transaction type via regex patterns.
constraints:
  - Support common bank statement formats (e.g., columns or line-based)
  - Combine multi-line descriptions into a single description field
  - Parse dates in multiple formats (DD/MM/YYYY, MM/DD/YYYY)
  - Handle both credit and debit transactions, indicating type based on amount sign or context
rationale: Transforms unstructured OCR text into consistent transaction data ready for storage.
affects:
  - backend/services/parser
  - backend/services/ocr
  - tests/parser
---
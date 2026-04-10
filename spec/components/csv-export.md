---
decision: Implement frontend CSV export utility that transforms transaction data array into CSV string with proper headers, encoding (UTF-8 with BOM for Excel), and triggers browser download. Provide ExportCSVButton component using this utility.
constraints:
  - Accept data array with fields: date, description, amount, type, balance, category
  - Generate header row with human-readable column names
  - Format dates as YYYY-MM-DD; amounts with 2 decimals and comma thousands separator
  - Add BOM (\uFEFF) at start to ensure Excel displays UTF-8 correctly
  - Create Blob, set MIME type text/csv; use URL.createObjectURL for download
  - Disable button during generation for large datasets; show filename with timestamp
  - Use GET /transactions/export/csv for server-side export when available
rationale: Allows users to download their transaction data for external analysis and record-keeping.
affects:
  - frontend/utils/csv-export
  - frontend/components/export-csv-button
  - backend/api/transactions/export/csv
---
---
decision: Create React CategoryManager component for managing spending categories. For MVP, show list of categories from atomic/configs/categories.json with inline edit of name and color, and allow adding/deleting custom categories (persisted to backend).
constraints:
  - Fetch categories from GET /categories endpoint or use atomic defaults
  - Inline editing: rename category, pick color (preset palette)
  - Add new category with default color; delete only custom categories (not defaults)
  - Persist changes via POST/PUT/DELETE to /categories (new endpoints required)
  - Handle optimistic updates with rollback on error
  - Show confirmation for delete; bulk operations optional
  - Styled consistently with app theme
rationale: Enables users to customize categorization for their transactions, improving data organization.
affects:
  - frontend/components/category-manager
  - backend/api/categories (new)
  - backend/models/category (new)
  - atomic/configs/categories.json
---
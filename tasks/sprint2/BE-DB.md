---
title: Database models
description: Create/adjust Account, Transaction, Category models with indexes
acceptance_criteria:
  - Transaction: methods for monthly aggregation and date filters
  - Account: user relationship and masking method
  - Category: new model (name, color, is_default, optional user_id)
  - Indexes: transactions(account_id,date,category,user_id), accounts(user_id), categories(user_id)
blocked_by: []
sprint: sprint2
effort: small
files:
  - backend/models/account
  - backend/models/transaction
  - backend/models/category
---
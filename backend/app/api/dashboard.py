from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, extract
from app.database import get_db
from app.models.transaction import Transaction
from app.core.auth import get_current_user
from app.models.user import User
from decimal import Decimal
from uuid import UUID

router = APIRouter(tags=["dashboard"])

@router.get("/stats")
async def get_dashboard_stats(
    account_id: UUID = None,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(
        func.sum(case((Transaction.type == "Credit", Transaction.mutation_amount), else_=0)).label("credit_total"),
        func.sum(case((Transaction.type == "Debit", Transaction.mutation_amount), else_=0)).label("debit_total"),
        func.count().label("transaction_count")
    ).where(
        extract('month', Transaction.date) == month,
        extract('year', Transaction.date) == year,
        Transaction.user_id == current_user.id
    )
    if account_id:
        stmt = stmt.where(Transaction.account_id == account_id)
    result = await db.execute(stmt)
    row = result.first()
    credit_total = row.credit_total or Decimal('0.00')
    debit_total = row.debit_total or Decimal('0.00')
    return {
        "credit_total": credit_total,
        "debit_total": debit_total,
        "net_change": credit_total - debit_total,
        "transaction_count": row.transaction_count or 0
    }

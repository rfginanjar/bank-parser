from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.transaction import Transaction
from app.core.auth import get_current_user
from app.models.user import User
from datetime import date
from decimal import Decimal

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/")
async def list_transactions(
    account_id: str = None,
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    search: str = None,
    page: int = 1,
    per_page: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Transaction).where(Transaction.user_id == current_user.id)
    if account_id:
        stmt = stmt.where(Transaction.account_id == account_id)
    if start_date:
        stmt = stmt.where(Transaction.date >= start_date)
    if end_date:
        stmt = stmt.where(Transaction.date <= end_date)
    if category:
        stmt = stmt.where(Transaction.category == category)
    if search:
        stmt = stmt.where(Transaction.description.ilike(f"%{search}%"))
    # Count total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0
    # Apply pagination
    stmt = stmt.order_by(Transaction.date.desc()).offset((page-1)*per_page).limit(per_page)
    result = await db.execute(stmt)
    transactions = result.scalars().all()
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "transactions": [
            {
                "id": str(tx.id),
                "date": tx.date.isoformat(),
                "description": tx.description,
                "mutation_amount": str(tx.mutation_amount.quantize(Decimal('0.01'))),
                "type": tx.type,
                "balance": str(tx.balance.quantize(Decimal('0.01'))),
                "category": tx.category
            }
            for tx in transactions
        ]
    }

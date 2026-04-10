from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.account import Account
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["accounts"])

@router.get("/")
async def list_accounts(
    bank: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Account).where(Account.user_id == current_user.id)
    if bank:
        stmt = stmt.where(Account.bank_name == bank)
    stmt = stmt.order_by(Account.bank_name, Account.account_name)
    result = await db.execute(stmt)
    accounts = result.scalars().all()
    return [
        {
            "id": str(acc.id),
            "account_number": acc.mask_account_number(),
            "account_name": acc.account_name,
            "bank_name": acc.bank_name
        }
        for acc in accounts
    ]

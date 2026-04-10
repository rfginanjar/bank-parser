from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.statement import Statement
from app.models.pending_review import PendingReview
from app.models.transaction import Transaction
from app.models.account import Account
from app.core.auth import get_current_user
from app.models.user import User
from app.services.validation import process_validation
from uuid import UUID

router = APIRouter(prefix="/validation", tags=["validation"])


@router.get("/pending-reviews")
async def list_pending_reviews(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all pending reviews for statements belonging to current user's accounts."""
    result = await db.execute(
        select(PendingReview, Statement, Account)
        .join(Statement, PendingReview.statement_id == Statement.id)
        .join(Account, Statement.account_id == Account.id)
        .where(Account.user_id == current_user.id)
    )
    rows = result.all()
    reviews = []
    for pending, stmt, acct in rows:
        reviews.append({
            "token": str(pending.validation_token),
            "statement_id": str(stmt.id),
            "account_name": acct.account_name,
            "bank_name": acct.bank_name,
            "upload_date": stmt.upload_date.isoformat() if stmt.upload_date else None,
            "expires_at": pending.expires_at.isoformat(),
            "transactions": pending.raw_transactions,
        })
    return reviews


@router.post("/pending-reviews/{token}/validate")
async def validate_review(
    token: str,
    updates: List[Dict] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Validate a pending review token and commit transactions."""
    # Find pending review by token and check expiration
    result = await db.execute(
        select(PendingReview).where(PendingReview.validation_token == token)
    )
    pending = result.scalar_one_or_none()
    if not pending:
        raise HTTPException(status_code=404, detail="Invalid token")
    if pending.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    # Get associated statement and its account
    stmt_result = await db.execute(select(Statement).where(Statement.id == pending.statement_id))
    statement = stmt_result.scalar_one_or_none()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")

    # Resolve account and user
    acct_result = await db.execute(select(Account).where(Account.id == statement.account_id))
    account = acct_result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Validate updates via service
    validation_result = await process_validation(updates)
    errors = validation_result["errors"]
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})
    validated_list = validation_result["validated"]

    try:
        async with db.begin():
            for vdata in validated_list:
                transaction = Transaction(
                    statement_id=statement.id,
                    account_id=statement.account_id,
                    user_id=account.user_id,
                    date=vdata["date"],
                    description=vdata["description"],
                    mutation_amount=vdata["mutation_amount"],
                    type=vdata["type"],
                    balance=vdata["balance"],
                    category=vdata.get("category"),
                )
                db.add(transaction)
            await db.delete(pending)
            statement.status = "committed"
        await db.commit()
        return {"status": "committed", "count": len(validated_list)}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

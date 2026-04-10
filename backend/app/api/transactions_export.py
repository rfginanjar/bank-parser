from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.transaction import Transaction
from app.core.auth import get_current_user
from app.models.user import User
from datetime import date
import csv
import io

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/export/csv")
async def export_transactions_csv(
    account_id: str = None,
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    search: str = None,
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
    stmt = stmt.order_by(Transaction.date.desc())
    result = await db.execute(stmt)
    transactions = result.scalars().all()
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Amount", "Type", "Balance", "Category"])
    for tx in transactions:
        writer.writerow([
            tx.date.isoformat(),
            tx.description,
            f"{tx.mutation_amount:.2f}",
            tx.type,
            f"{tx.balance:.2f}",
            tx.category or ""
        ])
    csv_content = output.getvalue()
    # Prepend BOM for Excel
    bom = "\ufeff"
    csv_content = bom + csv_content
    return Response(content=csv_content, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=transactions.csv"
    })

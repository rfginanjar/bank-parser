import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, UUID, Date, String, Numeric, ForeignKey, UniqueConstraint, Enum as SQLEnum, func, case, extract
from sqlalchemy.dialects.postgresql import UUID
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    statement_id = Column(UUID(as_uuid=True), ForeignKey("statements.id"), nullable=False, index=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    description = Column(String, nullable=False)
    mutation_amount = Column(Numeric(12, 2), nullable=False)
    type = Column(SQLEnum("Debit", "Credit", name="transaction_type"), nullable=False)
    balance = Column(Numeric(12, 2), nullable=False)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('statement_id', 'date', 'mutation_amount', 'balance', name='uq_transaction_unique'),
        Index('ix_transactions_account_date_cat_user', 'account_id', 'date', 'category', 'user_id'),
    )

    @classmethod
    def apply_date_filter(cls, query, start_date=None, end_date=None):
        """Apply date range filter to a query."""
        if start_date:
            query = query.filter(cls.date >= start_date)
        if end_date:
            query = query.filter(cls.date <= end_date)
        return query

    @classmethod
    async def get_monthly_stats(cls, db, account_id=None, user_id=None, month=None, year=None):
        """Return aggregated stats for given month/year and optional account."""
        stmt = select(
            func.sum(case((cls.type == "Credit", cls.mutation_amount), else_=0)).label("credit_total"),
            func.sum(case((cls.type == "Debit", cls.mutation_amount), else_=0)).label("debit_total"),
            func.count().label("transaction_count")
        ).where(
            extract('month', cls.date) == month,
            extract('year', cls.date) == year
        )
        if account_id:
            stmt = stmt.where(cls.account_id == account_id)
        if user_id:
            stmt = stmt.where(cls.user_id == user_id)
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

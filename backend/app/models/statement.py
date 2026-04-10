import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from .base import Base


class Statement(Base):
    __tablename__ = "statements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    period_month = Column(Integer, nullable=False)
    period_year = Column(Integer, nullable=False)
    file_url = Column(String, nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)  # SHA-256 hex
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(
        SQLEnum("pending", "processing", "extracted", "validated", "committed", name="statement_status"),
        default="pending",
        nullable=False,
        index=True
    )

    __table_args__ = (
        UniqueConstraint('account_id', 'period_month', 'period_year', name='uq_statement_period'),
    )

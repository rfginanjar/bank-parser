import uuid
from datetime import datetime
from sqlalchemy import Column, UUID, DateTime, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from .base import Base


class PendingReview(Base):
    __tablename__ = "pending_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    statement_id = Column(UUID(as_uuid=True), ForeignKey("statements.id"), unique=True, nullable=False)
    raw_transactions = Column(JSON, nullable=False)  # list of extracted but unvalidated transactions
    validation_token = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)

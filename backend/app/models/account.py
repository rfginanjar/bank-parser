import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    account_number = Column(String(100), nullable=False)  # encrypted
    account_name = Column(String(255), nullable=False)
    bank_name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="accounts")

    __table_args__ = (
        Index('ix_account_user_bank', 'user_id', 'bank_name'),
    )

    def mask_account_number(self) -> str:
        """Return masked account number showing last 4 digits."""
        if len(self.account_number) <= 4:
            return self.account_number
        return f"****-****-****-{self.account_number[-4:]}"

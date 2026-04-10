import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=False)  # hex color, e.g., #FF5733
    is_default = Column(Boolean, default=False, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)

    __table_args__ = (
        Index('ix_category_user', 'user_id'),
    )

    @classmethod
    def create_defaults(cls):
        """Return list of default spending categories."""
        return [
            cls(name="Food", color="#FF5733", is_default=True, user_id=None),
            cls(name="Transport", color="#33FF57", is_default=True, user_id=None),
            cls(name="Entertainment", color="#3357FF", is_default=True, user_id=None),
            cls(name="Shopping", color="#F333FF", is_default=True, user_id=None),
            cls(name="Bills & Utilities", color="#FF3333", is_default=True, user_id=None),
            cls(name="Health", color="#33FFF3", is_default=True, user_id=None),
            cls(name="Other", color="#C0C0C0", is_default=True, user_id=None),
        ]

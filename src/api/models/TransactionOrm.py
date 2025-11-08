import uuid
from datetime import datetime

from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


class TransactionORM(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    coin: Mapped[str] = mapped_column(String(120), nullable=False)

    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)


    owner = relationship("UserORM", back_populates="transactions")


from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
import uuid


class TransactionOrm(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    coin: Mapped[str] = mapped_column(String(120), nullable=False)

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now()
    )

    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    bought_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    owner = relationship("UserORM", back_populates="transactions")
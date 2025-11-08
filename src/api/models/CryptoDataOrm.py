import uuid
from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


class CryptoDataOrm(Base):
    __tablename__ = "crypto_data"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    amount_p_and_l: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now()
    )

    owner = relationship("UserORM", back_populates="crypto_data")

import uuid
from datetime import datetime

from sqlalchemy import String, Float, ForeignKey, Enum as SqlEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from enum import Enum

class TradeStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"

class TradeRequestOrm(Base):
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )

    receiver_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )

    coin: Mapped[str] = mapped_column(String(120), nullable=False)

    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    status: Mapped[TradeStatus] = mapped_column(
        SqlEnum(TradeStatus, name="trade_status"),
        nullable=False,
        default=TradeStatus.PENDING,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now()
    )

    sender = relationship(
        "PortfolioOrm",
        foreign_keys=[sender_id],
        back_populates="sender_requests",
    )

    receiver = relationship(
        "PortfolioOrm",
        foreign_keys=[receiver_id],
        back_populates="receiver_requests",
    )


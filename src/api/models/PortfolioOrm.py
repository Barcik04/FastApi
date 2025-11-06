# src/portfolio/PortfolioOrm.py
import uuid
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


class PortfolioORM(Base):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)

    coins: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False, default=dict)

    bought_price: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False, default=dict)
    p_and_l:     Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    owner = relationship("UserORM", back_populates="portfolios")

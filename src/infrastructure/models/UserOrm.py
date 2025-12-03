import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.TransactionOrm import TransactionOrm
from src.db import Base
from src.infrastructure.models.PortfolioOrm import PortfolioOrm


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    portfolios = relationship(
        PortfolioOrm, back_populates="owner",
        cascade="all, delete-orphan", passive_deletes=True
    )

    transactions = relationship(
        TransactionOrm, back_populates="owner",
        cascade="all, delete-orphan", passive_deletes=True
    )


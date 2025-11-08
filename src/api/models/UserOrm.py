# src/user/UserOrm.py
import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.TransactionOrm import TransactionORM
from src.db import Base
from src.api.models.PortfolioOrm import PortfolioORM


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    portfolios = relationship(
        PortfolioORM, back_populates="owner",
        cascade="all, delete-orphan", passive_deletes=True
    )

    transactions = relationship(
        TransactionORM, back_populates="owner",
        cascade="all, delete-orphan", passive_deletes=True
    )

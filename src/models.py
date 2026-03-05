from datetime import datetime
from sqlalchemy import DateTime, func
from time import timezone

from sqlalchemy.orm import (
DeclarativeBase, Mapped, mapped_column, relationship)
from sqlalchemy import ForeignKey, String
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    account = relationship("Account", back_populates= "User")

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement= True)
    balance: Mapped[int]
    status: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates= "accounts")
    
class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    from_account_id: Mapped[...] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    to_account_id: Mapped[...] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    #relationship()

class Outbox(Base):
    __tablename__ = "outbox"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    event_type: Mapped[str]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
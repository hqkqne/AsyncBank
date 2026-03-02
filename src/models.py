import datetime
from datetime import DateTime
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
    #created_at: Mapped[] = mapped_column()

    account = relationship("Account", back_populates= "User")

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement= True)
    balance: Mapped[int] = mapped_column()
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
        status: Mapped[str] = mapped_column(...)
        created_at: Mapped[datetime.datetime] =(
            mapped_column(DateTime(timezone = True),
                          server_default= func.now()))#date_time
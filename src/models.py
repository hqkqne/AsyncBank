import datetime
from sqlalchemy import (
func, DateTime, String, ForeignKey, CheckConstraint, Numeric)
from decimal import Decimal
from sqlalchemy.orm import (
DeclarativeBase, Mapped, mapped_column, relationship)
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    account = relationship("Account", back_populates= "User")

class Account(Base):
    __tablename__ = 'accounts'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement= True)
    balance: Mapped[Decimal] = mapped_column(Numeric(15,2), nullable= False)
    currency: Mapped[str] = mapped_column(String(3), default= "USD")
    status: Mapped[str] = mapped_column(default= "...", nullable=False)

    ## relationship
    user = relationship("User", back_populates= "account")
    #transactions
    outgoing_transactions = relationship("Transaction", back_populates="from_account")
    incoming_transactions = relationship("Transaction", back_populates="to_account")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    from_account_id: Mapped["Account"] = mapped_column(ForeignKey("accounts.id", ondelete="SET NULL"))
    to_account_id: Mapped["Account"] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(15))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    from_account = relationship(
        "Account",
        back_populates= "transactions"
    )
    to_account = relationship(
        "Account",
        back_populates="transactions"
    )

    # Limitations
    __table_args__ = (
        CheckConstraint("from_account_id != to_account_id", name = "check_no_self_transfer"),
        CheckConstraint("amount > 0", name = "check_positive_amount")
    )

    class Outbox(Base):
        __tablename__ = "outbox"
        id: Mapped[int] = mapped_column(
            primary_key=True, autoincrement=True)
        event_type: Mapped[str]
        status: Mapped[str]
        created_at: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now()
        )
        processed_at: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now()
        )
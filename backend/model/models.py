from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    bank_accounts = relationship("BankAccount", back_populates="user")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    account_id = Column(Integer, primary_key=True, index=True)
    random_id = Column(Numeric(12, 0), index=True, unique=True)  
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Numeric, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bank_accounts")
    transactions_from = relationship("Transaction", foreign_keys="[Transaction.from_account_id]", back_populates="from_account")
    transactions_to = relationship("Transaction", foreign_keys="[Transaction.to_account_id]", back_populates="to_account")

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    owner_account_id = Column(Integer, ForeignKey("bank_accounts.account_id"))
    from_account_id = Column(Integer, ForeignKey("bank_accounts.account_id"))
    to_account_id = Column(Integer, ForeignKey("bank_accounts.account_id"))
    amount = Column(Numeric)
    transaction_type = Column(String)
    description = Column(String)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    from_account = relationship("BankAccount", foreign_keys=[from_account_id], back_populates="transactions_from")
    to_account = relationship("BankAccount", foreign_keys=[to_account_id], back_populates="transactions_to")
    owner_account = relationship("BankAccount", foreign_keys=[owner_account_id], backref="transactions")

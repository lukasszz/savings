from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    currency = Column(String)

    def __repr__(self):
        return "Asset %s, active=%s" % (self.name, self.active)


class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)

    title = Column(String)
    desc = Column(String)
    active = Column(Boolean)
    date = Column(Date)
    currency = Column(String)

    splits = relationship("TransactionSplit", back_populates="transaction")


class TransactionSplit(Base):
    __tablename__ = 'transaction_split'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(12, 2))
    desc = Column(String)
    id_transaction = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    id_asset = Column(Integer, ForeignKey("asset.id"), nullable=True)
    id_budget = Column(Integer, ForeignKey("budget.id"), nullable=True)

    transaction = relationship("Transaction", back_populates='splits')

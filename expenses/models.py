from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid, Float, ForeignKey
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class Expense(_Base):
    __tablename__ = "expenses"

    id = Column(Uuid, primary_key=True, default=uuid7)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    cash_value = Column(Float, nullable=False)
    frequency = Column(String, nullable=True)
    category_id = Column(Uuid, ForeignKey("categories.id", ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    category = relationship('Category', back_populates='expenses')

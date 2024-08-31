from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class Category(_Base):
    __tablename__ = "categories"

    id = Column(Uuid, primary_key=True, default=uuid7)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    expenses = relationship('Expense', back_populates='category', cascade="all, delete-orphan")


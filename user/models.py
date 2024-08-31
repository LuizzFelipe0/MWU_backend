from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import Column, String, DateTime, Uuid, ForeignKey
from uuid_extensions import uuid7

from mwu.db import Base as _Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(_Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid7)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    expense_id = Column(Uuid, ForeignKey("expenses.id", ondelete='CASCADE'), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid, Enum
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class TypeEnum(enum.Enum):
    Income = 'Income'
    Expense = 'Expense'
    Transfer = 'Transfer'
    Investment = 'Investment'


class Category(_Base):
    __tablename__ = "categories"

    id = Column(Uuid, primary_key=True, default=uuid7)
    user_id = Column(Uuid, primary_key=True, default=uuid7)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(Enum(TypeEnum, name="typeenum"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

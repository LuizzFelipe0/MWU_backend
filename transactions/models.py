import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid, Float, Boolean, Enum
from uuid_extensions import uuid7

from mwu.db import Base as _Base

class RecurrenceIntervalEnum(enum.Enum):
    Weekly = 'Weekly'
    Monthly = 'Monthly'
    Yearly = 'Yearly'


class Transactions(_Base):
    __tablename__ = "transactions"

    id = Column(Uuid, primary_key=True, default=uuid7)
    user_id = Column(Uuid, default=uuid7)
    account_id = Column(Uuid, default=uuid7)
    category_id = Column(Uuid, primary_key=True, default=uuid7)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, nullable=False, default=False)
    recurrence_interval = Column(Enum(RecurrenceIntervalEnum, name="recurrenceintervalenum"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

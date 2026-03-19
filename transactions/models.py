from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class Transactions(_Base):
    __tablename__ = "transactions"

    id = Column(Uuid, primary_key=True, default=uuid7)
    user_id = Column(Uuid, default=uuid7)
    account_id = Column(Uuid, nullable=True)
    category_id = Column(Uuid, primary_key=True, default=uuid7)
    recurrence_id = Column(Uuid, ForeignKey("recurrence_schedules.id"), nullable=True, default=uuid7)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    recurrence = relationship("RecurrenceSchedule", backref="transactions", lazy="joined")


class RecurrenceSchedule(_Base):
    __tablename__ = "recurrence_schedules"

    id = Column(Uuid, primary_key=True, default=uuid7)
    user_id = Column(Uuid, default=uuid7)
    interval = Column(String, nullable=False) # enum (DAILY, WEEKLY, MONTHLY, YEARLY)
    next_due_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False) #
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

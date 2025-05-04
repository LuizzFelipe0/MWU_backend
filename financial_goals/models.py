from datetime import datetime

from sqlalchemy import Column, String, Uuid, Float, Date, DateTime
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class FinancialGoals(_Base):
    __tablename__ = "financial_goals"

    id = Column(Uuid, primary_key=True, default=uuid7)
    user_id = Column(Uuid,default=uuid7)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    target_amount = Column(Float, default=0.0, nullable=False)
    deadline = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

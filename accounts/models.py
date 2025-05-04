from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid, Float
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class Accounts(_Base):
    __tablename__ = "accounts"

    id = Column(Uuid, primary_key=True, default=uuid7)
    name = Column(String)
    type = Column(String, nullable=False)
    account_number = Column(String, nullable=True)
    balance = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

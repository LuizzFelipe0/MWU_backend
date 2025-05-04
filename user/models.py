from datetime import datetime

import uuid_extensions
from sqlalchemy import Column, String, DateTime, Uuid, Float

from mwu.db import Base as _Base


class User(_Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    cpf = Column(String, nullable=False)
    password = Column(String, nullable=False)
    manual_balance = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

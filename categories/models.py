from datetime import datetime

from sqlalchemy import Column, String, DateTime, Uuid
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class Category(_Base):
    __tablename__ = "categories"

    id = Column(Uuid, primary_key=True, default=uuid7)
    user_id = Column(Uuid, default=uuid7)
    category_type_id = Column(Uuid, default=uuid7)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

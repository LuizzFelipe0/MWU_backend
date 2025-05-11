from sqlalchemy import Column, Uuid, String, Boolean
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class CategoryTypes(_Base):
    __tablename__ = "category_types"
    id = Column(Uuid, primary_key=True, nullable=False, default=uuid7)
    name = Column(String, nullable=False)
    is_positive = Column(Boolean, nullable=False)

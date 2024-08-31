from sqlalchemy import Column, String, Uuid, ForeignKey
from uuid_extensions import uuid7

from mwu.db import Base as _Base


class Report(_Base):
    __tablename__ = "report"

    id = Column(Uuid, primary_key=True, default=uuid7)
    expense_id = Column(Uuid, ForeignKey("expenses.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)



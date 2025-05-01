from datetime import datetime

import uuid_extensions
from sqlalchemy import Column, DateTime, Uuid

from mwu.db import Base as _Base


class UsersAccounts(_Base):
    __tablename__ = "user_accounts"
    id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    user_id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    account_id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

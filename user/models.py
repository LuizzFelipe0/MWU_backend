from datetime import datetime

import uuid_extensions
from sqlalchemy import Column, String, DateTime, Uuid

from mwu.db import Base as _Base


class User(_Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    cpf = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)


class UsersAccounts(_Base):
    __tablename__ = "user_accounts"
    id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    user_id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    account_id = Column(Uuid, primary_key=True, default=uuid_extensions.uuid7)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

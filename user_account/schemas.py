from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserAccountInput(BaseModel):
    user_id: UUID
    account_id: UUID


class UserAccountOutput(BaseModel):
    id: UUID
    user_id: UUID
    account_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

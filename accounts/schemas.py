from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AccountInput(BaseModel):
    name: str
    type: str
    account_number: str
    balance: float


class AccountUpdateInput(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    account_number: Optional[str] = None
    balance: Optional[float] = None


class AccountOutput(BaseModel):
    id: UUID
    name: str
    type: str
    account_number: str
    balance: float
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

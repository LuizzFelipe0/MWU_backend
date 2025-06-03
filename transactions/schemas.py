from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TransactionInput(BaseModel):
    user_id: UUID
    account_id: Optional[UUID] = None
    category_id: UUID
    name: str
    description: Optional[str] = None
    amount: float
    date: datetime
    is_recurring: bool
    recurrence_interval: Optional[str] = None
    next_due_date: Optional[datetime] = None


class TransactionUpdateInput(BaseModel):
    user_id: Optional[UUID] = None
    account_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_interval: Optional[str] = None
    next_due_date: Optional[datetime] = None


class TransactionOutput(BaseModel):
    id: UUID
    user_id: UUID
    account_id: Optional[UUID] = None
    category_id: UUID
    name: str
    description: Optional[str] = None
    amount: float
    date: datetime
    is_recurring: bool
    recurrence_interval: Optional[str] = None
    next_due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

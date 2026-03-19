from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, model_validator


class TransactionInput(BaseModel):
    user_id: UUID
    account_id: Optional[UUID] = None
    category_id: UUID
    name: str
    description: Optional[str] = None
    amount: float
    date: datetime

    is_recurring: Optional[bool] = False
    recurrence_interval: Optional[str] = None
    end_date: Optional[datetime] = None
    next_due_date: Optional[datetime] = None


class TransactionUpdateInput(BaseModel):
    user_id: Optional[UUID] = None
    account_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None

    is_recurring: bool = False
    recurrence_interval: Optional[str] = None
    end_date: Optional[datetime] = None
    next_due_date: Optional[datetime] = None


class TransactionOutput(BaseModel):
    id: UUID
    user_id: UUID
    account_id: Optional[UUID] = None
    recurrence_id: Optional[UUID]
    category_id: UUID
    name: str
    description: Optional[str] = None
    amount: float
    date: datetime

    is_recurrence_active: Optional[bool] = None
    recurrence_interval: Optional[str] = None
    end_date: Optional[datetime] = None
    next_due_date: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    @model_validator(mode='before')
    @classmethod
    def flatten_recurrence(cls, data):
        if hasattr(data, "recurrence") and data.recurrence:
            data.is_recurrence_active = data.recurrence.is_active
            data.recurrence_interval = data.recurrence.interval
            data.end_date = data.recurrence.end_date
            data.next_due_date = data.recurrence.next_due_date
        return data

    class Config:
        from_attributes = True

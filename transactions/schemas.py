from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class RecurrenceIntervalEnum(str, Enum):
    Weekly = 'Weekly'
    Monthly = 'Monthly'
    Yearly = 'Yearly'


class TransactionInput(BaseModel):
    user_id: UUID
    account_id: UUID
    category_id: UUID
    amount: float
    type: str
    date: datetime
    is_recurring: bool
    recurrence_interval: RecurrenceIntervalEnum | None


class TransactionOutput(BaseModel):
    id: UUID
    user_id: UUID
    account_id: UUID
    category_id: UUID
    amount: float
    type: str
    date: datetime
    is_recurring: bool
    recurrence_interval: RecurrenceIntervalEnum | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExpenseInput(BaseModel):
    name: str
    date: datetime
    cash_value: float
    category_id: UUID
    frequency: str

class ExpenseOutput(BaseModel):
    id: UUID
    name: str
    date: datetime
    cash_value: float
    frequency: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class FinancialGoalsInput(BaseModel):
    user_id: UUID
    name: str
    description: str | None
    current_amount: float
    target_amount: float
    balance: float
    deadline: date


class FinancialGoalsOutput(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None
    current_amount: float
    target_amount: float
    deadline: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

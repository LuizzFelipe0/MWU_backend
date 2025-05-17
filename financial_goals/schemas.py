from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FinancialGoalsInput(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None
    target_amount: float
    deadline: date


class FinancialGoalsUpdateInput(BaseModel):
    user_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = None
    deadline: Optional[date] = None


class FinancialGoalsOutput(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None
    target_amount: float
    deadline: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

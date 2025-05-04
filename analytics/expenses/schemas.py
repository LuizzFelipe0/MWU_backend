from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class GoalsOutput(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None
    current_amount: float # a ser visto
    target_amount: float
    deadline: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

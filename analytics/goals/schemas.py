from datetime import  date
from uuid import UUID

from pydantic import BaseModel


class GoalsOutput(BaseModel):
    id: UUID
    name: str
    description: str | None
    target_amount: float
    progress_percentage: str
    sum_of_balances: float
    difference_to_achieve_target: float
    deadline: date

    class Config:
        from_attributes = True

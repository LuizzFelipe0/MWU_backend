from pydantic import BaseModel
from uuid import UUID

class RecurrenceSimulationInput(BaseModel):
    recurrence_id: UUID
    iterations: int
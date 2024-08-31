from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoryInput(BaseModel):
    name: str
    description: str


class CategoryOutput(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

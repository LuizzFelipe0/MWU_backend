from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoryInput(BaseModel):
    user_id: UUID
    name: str
    description: str
    type: str


class CategoryOutput(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str
    type: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

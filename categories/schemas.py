from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryInput(BaseModel):
    user_id: UUID
    name: str
    description: str
    type: str


class CategoryUpdateInput(BaseModel):
    user_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None


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

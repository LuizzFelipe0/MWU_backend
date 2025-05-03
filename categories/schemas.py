from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryInput(BaseModel):
    user_id: UUID
    category_type_id: UUID
    name: str
    description: str


class CategoryUpdateInput(BaseModel):
    user_id: Optional[UUID] = None
    category_type_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryOutput(BaseModel):
    id: UUID
    user_id: UUID
    category_type_id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

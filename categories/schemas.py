from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TypeEnum(str, Enum):
    Income = "Income"
    Expense = "Expense"
    Transfer = "Transfer"
    Investment = "Investment"


class CategoryInput(BaseModel):
    user_id: UUID
    name: str
    description: str
    type: TypeEnum | None


class CategoryUpdateInput(BaseModel):
    user_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: TypeEnum = None


class CategoryOutput(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str
    type: TypeEnum | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

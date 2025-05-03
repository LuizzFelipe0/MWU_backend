from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryTypesInput(BaseModel):
    name: str
    is_positive: bool


class CategoryTypesUpdateInput(BaseModel):
    name: Optional[str] = None
    is_positive: Optional[bool] = None


class CategoryTypesOutput(BaseModel):
    id: UUID
    name: str
    is_positive: bool

    class Config:
        from_attributes = True

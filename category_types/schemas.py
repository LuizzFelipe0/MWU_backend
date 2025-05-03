from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryTypesInput(BaseModel):
    name: str


class CategoryTypesUpdateInput(BaseModel):
    name: Optional[str] = None


class CategoryTypesOutput(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

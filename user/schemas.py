from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInput(BaseModel):
    first_name: str
    last_name: str
    cpf: str
    email: str
    password: str


class UserUpdateInput(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserOutput(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    cpf: str
    email: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

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
    manual_balance: Optional[float] = None


class UserUpdateInput(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    manual_balance: Optional[float] = None


class UserOutput(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    cpf: str
    email: str
    manual_balance: float | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserInput(BaseModel):
    first_name: str
    last_name: str
    cpf: str
    email: str
    password: str


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

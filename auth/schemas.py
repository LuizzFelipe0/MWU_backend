from datetime import datetime

from pydantic import BaseModel


class LoginInput(BaseModel):
    email: str
    password: str


class LoginOutput(BaseModel):
    email: str
    first_name: str
    cpf: str
    created_at: datetime

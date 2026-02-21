from uuid import UUID
from pydantic import BaseModel

class LoginInput(BaseModel):
    email: str
    password: str

class UserInfo(BaseModel):
    id: UUID
    email: str
    first_name: str
    cpf: str
    is_admin: bool

class LoginOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo
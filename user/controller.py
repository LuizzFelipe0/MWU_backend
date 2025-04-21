from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.auth.security import hash_password, is_strong_password
from mwu.db import get_db
from .models import User as UserModel
from .schemas import UserOutput as UserOutScheme, UserInput as UserInScheme

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("")
def get_all_users(db: Session = Depends(get_db)) -> list[UserOutScheme | None]:
    users = db.query(UserModel).all()
    return users


@users_router.get("/{user_id}")
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)) -> list[UserOutScheme | None]:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail="User not found with the given id.")
    return user


@users_router.post("", status_code=201, response_model=UserOutScheme)
def create_user(data: UserInScheme, db: Session = Depends(get_db)) -> UserOutScheme:
    if not is_strong_password(data.password):
        raise HTTPException(status_code=422, detail="This Password is not valid, Try Again!")

    user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=hash_password(data.password),
        cpf=data.cpf
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

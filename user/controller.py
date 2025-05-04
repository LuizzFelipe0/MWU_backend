from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.auth.security import hash_password, is_strong_password
from mwu.db import get_db
from .models import User as UserModel
from .schemas import UserOutput as UserOutScheme, UserInput as UserInScheme, UserUpdateInput as UserUpdateInScheme
from .utils import cpf_validator

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("")
def get_all_users(db: Session = Depends(get_db)) -> list[UserOutScheme | None]:
    users = db.query(UserModel).filter(UserModel.deleted_at.is_(None)).all()
    return users


@users_router.get("/deleted")
def get_deleted_users(db: Session = Depends(get_db)) -> list[UserOutScheme | None]:
    deleted_users = db.query(UserModel).filter(UserModel.deleted_at.isnot(None)).all()
    return deleted_users


@users_router.get("/{user_id}")
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)) -> list[UserOutScheme | None]:
    user = (db.query(UserModel).
            filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found with the given id.")
    return user


@users_router.post("", status_code=201, response_model=UserOutScheme)
def create_user(data: UserInScheme, db: Session = Depends(get_db)) -> UserOutScheme:
    if not is_strong_password(data.password):
        raise HTTPException(status_code=422, detail="This Password is not valid, Try Again!")

    if not cpf_validator(data.cpf):
        raise HTTPException(status_code=422, detail="The format or the CPF itself is not valid, Try Again!")

    user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=hash_password(data.password),
        cpf=cpf_validator(data.cpf),
        manual_balance=data.manual_balance
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@users_router.post("/{user_id}/restore", status_code=200, response_model=UserOutScheme)
def restore_deleted_user(user_id: UUID, db: Session = Depends(get_db)) -> UserOutScheme:
    deleted_user = (
        db.query(UserModel)
        .filter(
            UserModel.id == user_id,
            UserModel.deleted_at.isnot(None)).first()
    )

    if not deleted_user:
        raise HTTPException(status_code=404, detail="This User is not deleted or was not found in the database!")

    deleted_user.updated_at = datetime.now()
    deleted_user.deleted_at = None
    db.commit()
    db.refresh(deleted_user)

    return deleted_user


@users_router.patch("/update/{user_id}", status_code=200, response_model=UserOutScheme)
def update_user(user_id: UUID, data: UserUpdateInScheme, db: Session = Depends(get_db)) -> UserUpdateInScheme:
    user = db.query(UserModel).filter(UserModel.id == user_id,
                                      UserModel.deleted_at.is_(None)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    update_data = data.dict(exclude_unset=True)

    if not is_strong_password(data.password):
        raise HTTPException(status_code=422, detail="This Password is not valid, Try Again!")

    if not cpf_validator(data.cpf):
        raise HTTPException(status_code=422, detail="The format or the CPF itself is not valid, Try Again!")

    for key, value in update_data.items():
        setattr(user, key, value)

    user.updated_at = datetime.now()
    db.commit()

    return user


@users_router.delete("/delete/{user_id}", status_code=200, response_model=UserOutScheme)
def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> UserOutScheme:
    user = db.query(UserModel).filter(UserModel.id == user_id,
                                      UserModel.deleted_at.is_(None)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    user.deleted_at = datetime.now()
    db.commit()

    return user
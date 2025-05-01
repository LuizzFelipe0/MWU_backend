from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from accounts.models import Accounts as AccountModel
from mwu.db import get_db
from user.models import User as UserModel
from .models import UsersAccounts as UserAccountM2MModel
from .schemas import UserAccountOutput as UserAccountOutScheme

user_account_router = APIRouter(prefix="/users_acounts", tags=["User Account Relation"])


@user_account_router.get("/users/{user_id}/accounts", response_model=list[UserAccountOutScheme])
def list_accounts_for_user(user_id: UUID, db: Session = Depends(get_db)):
    account_user_relation = db.query(UserAccountM2MModel).filter_by(user_id=user_id).all()
    return account_user_relation


@user_account_router.get("/accounts/{account_id}/users", response_model=list[UserAccountOutScheme])
def list_users_for_account(account_id: UUID, db: Session = Depends(get_db)):
    user_account_relation = db.query(UserAccountM2MModel).filter_by(account_id=account_id).all()
    return user_account_relation


@user_account_router.post("/users/{user_id}/accounts/{account_id}", response_model=UserAccountOutScheme,
                          status_code=201)
def create_user_account_relationship(user_id: UUID, account_id: UUID, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=404, detail="The User was not found")

    account = db.query(AccountModel).filter(AccountModel.id == account_id, AccountModel.deleted_at.is_(None)).first()
    if not account:
        raise HTTPException(status_code=404, detail="The Account was not found")

    existing_relation = db.query(UserAccountM2MModel).filter_by(user_id=user_id, account_id=account_id).first()
    if existing_relation:
        raise HTTPException(status_code=409, detail="The Relationship already exists")

    user_account_relation = UserAccountM2MModel(user_id=user_id, account_id=account_id)

    db.add(user_account_relation)
    db.commit()
    db.refresh(user_account_relation)

    return user_account_relation


@user_account_router.delete("/users/{user_id}/accounts/{account_id}", response_model=UserAccountOutScheme)
def delete_user_account_relationship(user_id: UUID, account_id: UUID, db: Session = Depends(get_db)):
    user_account_relation = db.query(UserAccountM2MModel).filter_by(user_id=user_id, account_id=account_id).first()

    if not user_account_relation:
        raise HTTPException(status_code=404, detail="Relationship not found")

    db.delete(user_account_relation)
    db.commit()

    return user_account_relation

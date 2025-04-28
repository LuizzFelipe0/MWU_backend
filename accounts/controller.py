from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from user.models import User as UserModel, UsersAccounts as UserAccountM2MModel
from .models import Accounts as AccountModel
from .schemas import AccountOutput as AccountOutScheme, AccountInput as AccountInScheme

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@accounts_router.get("")
def get_all_accounts(db: Session = Depends(get_db)) -> list[AccountOutScheme | None]:
    accounts = db.query(AccountModel).all()
    return accounts


@accounts_router.get("/{account_id}")
def get_account_by_id(account_id: UUID, db: Session = Depends(get_db)) -> list[AccountOutScheme | None]:
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found with the given id.")
    return account


@accounts_router.post("", status_code=201, response_model=AccountOutScheme)
def create_account(user_id: UUID, data: AccountInScheme, db: Session = Depends(get_db)) -> AccountOutScheme:
    user = (db.query(UserModel)
            .filter(UserModel.id == user_id, UserModel.deleted_at.is_(None))
            .first())

    if not user:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    account = AccountModel(
        account_number=data.account_number,
        balance=data.balance,
        name=data.name,
        type=data.type
    )
    db.add(account)
    db.flush()  # flush function saves the objects temporary into memory

    user_account = UserAccountM2MModel(
        user_id=user_id,
        account_id=account.id
    )
    db.add(user_account)
    db.commit()

    db.refresh(account)
    db.refresh(user_account)

    return account

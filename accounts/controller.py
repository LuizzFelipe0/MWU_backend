from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
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
        return HTTPException(status_code=404, detail="Account not found with the given id.")
    return account

"""""
@accounts_router.post("", status_code=201, response_model=AccountOutScheme)
def create_account(data: AccountInScheme, db: Session = Depends(get_db)) -> AccountOutScheme:
    account = AccountModel(
        name=data.name,
        description=data.description
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    return account
"""
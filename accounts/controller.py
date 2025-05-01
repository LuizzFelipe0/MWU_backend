from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from .models import Accounts as AccountModel
from .schemas import AccountOutput as AccountOutScheme, AccountInput as AccountInScheme, \
    AccountUpdateInput as AccountUpdateInScheme

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@accounts_router.get("")
def get_all_accounts(db: Session = Depends(get_db)) -> list[AccountOutScheme | None]:
    accounts = db.query(AccountModel).filter(AccountModel.deleted_at.is_(None)).all()
    return accounts


@accounts_router.get("/deleted")
def get_deleted_accounts(db: Session = Depends(get_db)) -> list[AccountOutScheme | None]:
    deleted_accounts = db.query(AccountModel).filter(AccountModel.deleted_at.isnot(None)).all()
    return deleted_accounts


@accounts_router.get("/{account_id}")
def get_account_by_id(account_id: UUID, db: Session = Depends(get_db)) -> list[AccountOutScheme | None]:
    account = (db.query(AccountModel).
               filter(AccountModel.id == account_id, AccountModel.deleted_at.is_(None)))
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found with the given id.")
    return account


@accounts_router.post("", status_code=201, response_model=AccountOutScheme)
def create_account(data: AccountInScheme, db: Session = Depends(get_db)) -> AccountOutScheme:
    account = AccountModel(
        account_number=data.account_number,
        balance=data.balance,
        name=data.name,
        type=data.type
    )
    db.add(account)

    db.commit()
    db.refresh(account)

    return account


@accounts_router.post("/{account_id}/restore", status_code=200, response_model=AccountOutScheme)
def restore_deleted_account(account_id: UUID, db: Session = Depends(get_db)) -> AccountOutScheme:
    deleted_account = (
        db.query(AccountModel)
        .filter(
            AccountModel.id == account_id,
            AccountModel.deleted_at.isnot(None)).first()
    )

    if not deleted_account:
        raise HTTPException(status_code=404, detail="This Account is not deleted or was not found in the database!")

    deleted_account.updated_at = datetime.now()
    deleted_account.deleted_at = None
    db.commit()
    db.refresh(deleted_account)

    return deleted_account


@accounts_router.patch("/update/{account_id}", status_code=200, response_model=AccountOutScheme)
def update_account(account_id: UUID, data: AccountUpdateInScheme,
                   db: Session = Depends(get_db)) -> AccountUpdateInScheme:
    account = db.query(AccountModel).filter(AccountModel.id == account_id,
                                            AccountModel.deleted_at.is_(None)).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found with the given id.")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(account, key, value)

    account.updated_at = datetime.now()
    db.commit()

    return account


@accounts_router.delete("/delete/{account_id}", status_code=200, response_model=AccountOutScheme)
def delete_account(account_id: UUID, db: Session = Depends(get_db)) -> AccountOutScheme:
    account = db.query(AccountModel).filter(AccountModel.id == account_id,
                                            AccountModel.deleted_at.is_(None)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found with the given id.")

    account.deleted_at = datetime.now()
    db.commit()

    return account

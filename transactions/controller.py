from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from accounts.models import Accounts as AccountModel
from categories.models import Category as CategoryModel
from mwu.db import get_db
from user.models import User as UserModel
from .models import Transactions as TransactionModel
from .schemas import TransactionOutput as TransactionOutScheme, TransactionInput as TransactionInScheme

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@transactions_router.get("")
def get_all_transactions(db: Session = Depends(get_db)) -> list[TransactionOutScheme | None]:
    transactions = db.query(TransactionModel).filter(TransactionModel.deleted_at.is_(None)).all()
    return transactions


@transactions_router.get("/deleted")
def get_deleted_transactions(db: Session = Depends(get_db)) -> list[TransactionOutScheme | None]:
    deleted_transactions = db.query(TransactionModel).filter(TransactionModel.deleted_at.isnot(None)).all()
    return deleted_transactions


@transactions_router.get("/{transaction_id}")
def get_transaction_by_id(transaction_id: UUID, db: Session = Depends(get_db)) -> list[TransactionOutScheme | None]:
    transaction = (db.query(TransactionModel).
                   filter(TransactionModel.id == transaction_id, TransactionModel.deleted_at.is_(None)))
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found with the given id.")
    return transaction


@transactions_router.post("", status_code=201, response_model=TransactionOutScheme)
def create_transaction(data: TransactionInScheme, db: Session = Depends(get_db)) -> TransactionOutScheme | None:
    user = db.query(UserModel).filter(UserModel.id == data.user_id,
                                      UserModel.deleted_at.is_(None)).first()

    account = (db.query(AccountModel).
               filter(AccountModel.id == data.account_id, AccountModel.deleted_at.is_(None)))

    category = db.query(CategoryModel).filter(CategoryModel.id == data.category_id,
                                              CategoryModel.deleted_at.is_(None)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found with the given id.")

    if not category:
        raise HTTPException(status_code=404, detail="Category not found with the given id.")

    transaction = TransactionModel(
        user_id=data.user_id,
        category_id=data.category_id,
        account_id=data.account_id,
        name=data.name,
        amount=data.amount,
        date=data.date,
        is_recurring=data.is_recurring,
        next_due_date=data.next_due_date
    )
    db.add(transaction)

    db.commit()
    db.refresh(transaction)

    return transaction

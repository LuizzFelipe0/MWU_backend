from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mwu.db import get_db
from .models import Transactions as TransactionModel
from .schemas import TransactionOutput as TransactionOutScheme

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@transactions_router.get("")
def get_all_transactions(db: Session = Depends(get_db)) -> list[TransactionOutScheme | None]:
    transactions = db.query(TransactionModel).all()
    return transactions

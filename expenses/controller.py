from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import Expense as ExpenseModel
from .schemas import ExpenseOutput as ExpenseOutScheme, ExpenseInput as ExpenseInScheme
from mwu.db import get_db

expenses_router = APIRouter(prefix="/expenses", tags=["Expenses"])


@expenses_router.get("")
def get_all_expenses(db: Session = Depends(get_db)) -> list[ExpenseOutScheme | None]:
    expenses = db.query(ExpenseModel).all()
    return expenses

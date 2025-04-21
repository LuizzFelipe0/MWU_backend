from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from .models import FinancialGoals as FinancialGoalModel
from .schemas import FinancialGoalsOutput as FinancialGoalOutScheme

financial_goals_router = APIRouter(prefix="/financial_goals", tags=["Financial Goals"])


@financial_goals_router.get("")
def get_all_financial_goals(db: Session = Depends(get_db)) -> list[FinancialGoalOutScheme | None]:
    financial_goals = db.query(FinancialGoalModel).all()
    return financial_goals


@financial_goals_router.get("/{financial_goal_id}")
def get_financial_goal_by_id(financial_goal_id: UUID, db: Session = Depends(get_db)) -> list[
    FinancialGoalOutScheme | None]:
    financial_goal = db.query(FinancialGoalModel).filter(FinancialGoalModel.id == financial_goal_id).first()
    if financial_goal is None:
        return HTTPException(status_code=404, detail="Account not found with the given id.")
    return financial_goal

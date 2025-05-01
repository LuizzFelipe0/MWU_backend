from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mwu.db import get_db
from user.models import User as UserModel
from .models import FinancialGoals as FinancialGoalModel
from .schemas import FinancialGoalsOutput as FinancialGoalOutScheme, FinancialGoalsInput as FinancialGoalInScheme, \
    FinancialGoalsUpdateInput as FinancialGoalUpdateInScheme

financial_goals_router = APIRouter(prefix="/financial_goals", tags=["Financial Goals"])


@financial_goals_router.get("")
def get_all_financial_goals(db: Session = Depends(get_db)) -> list[FinancialGoalOutScheme | None]:
    financial_goals = db.query(FinancialGoalModel).all()
    return financial_goals


@financial_goals_router.get("/{financial_goal_id}")
def get_financial_goal_by_id(financial_goal_id: UUID, db: Session = Depends(get_db)) -> list[
    FinancialGoalOutScheme | None]:
    financial_goal = db.query(FinancialGoalModel).filter(FinancialGoalModel.id == financial_goal_id)
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial Goal not found with the given id.")
    return financial_goal


@financial_goals_router.post("", status_code=201, response_model=FinancialGoalOutScheme)
def create_financial_goal(data: FinancialGoalInScheme, db: Session = Depends(get_db)) -> FinancialGoalOutScheme:
    user = db.query(UserModel).filter(UserModel.id == data.user_id,
                                      UserModel.deleted_at.is_(None)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    financial_goal = FinancialGoalModel(
        user_id=data.user_id,
        name=data.name,
        description=data.description,
        current_amount=data.current_amount,
        target_amount=data.target_amount,
        deadline=data.deadline
    )

    db.add(financial_goal)
    db.commit()
    db.refresh(financial_goal)

    return financial_goal


@financial_goals_router.patch("/update/{financial_goal_id}", status_code=200, response_model=FinancialGoalOutScheme)
def update_financial_goal(financial_goal_id: UUID, data: FinancialGoalUpdateInScheme,
                          db: Session = Depends(get_db)) -> FinancialGoalUpdateInScheme:
    financial_goal = db.query(FinancialGoalModel).filter(FinancialGoalModel.id == financial_goal_id).first()

    user = db.query(UserModel).filter(UserModel.id == data.user_id,
                                      UserModel.deleted_at.is_(None)).first()
    if data.user_id is not None and user is None:
        raise HTTPException(status_code=404, detail="User not found with the given id.")

    if not financial_goal:
        raise HTTPException(status_code=404, detail="Financial Goal not found with the given id.")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(financial_goal, key, value)

    financial_goal.updated_at = datetime.now()
    db.commit()

    return financial_goal


@financial_goals_router.delete("/delete/{financial_goal_id}", status_code=204)
def delete_financial_goal(financial_goal_id: UUID, db: Session = Depends(get_db)):
    financial_goal = db.query(FinancialGoalModel).filter(FinancialGoalModel.id == financial_goal_id).first()
    if not financial_goal:
        raise HTTPException(status_code=404, detail="Account not found with the given id.")

    db.delete(financial_goal)
    db.commit()

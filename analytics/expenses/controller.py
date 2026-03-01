from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi_utils.cbv import cbv

from analytics.expenses.schemas import (
    MonthlyCategoryExpense,
    TotalExpenseCategoryDistribution,
)
from analytics.expenses.service import ExpensesService
from auth.utils import get_current_user

expenses_router = APIRouter(prefix="/expenses", tags=["Expenses Analysis"])


@cbv(expenses_router)
class ExpensesController:
    service: ExpensesService = Depends()

    @expenses_router.get("/monthly/category-type", response_model=list[MonthlyCategoryExpense])
    def get_monthly_expenses_by_category_type(
            self,
            current_user = Depends(get_current_user),
            is_recurring_expense: Optional[bool] = Query(None, description="Filter by recurring expenses."),
    ):
        return self.service.get_monthly_expenses_by_category(user_id=current_user.id, is_recurring_expense=is_recurring_expense)
    @expenses_router.get("/distribution", response_model=list[TotalExpenseCategoryDistribution])
    def get_total_expense_distribution(self, current_user = Depends(get_current_user)):
        return self.service.get_total_expense_distribution(user_id=current_user.id)

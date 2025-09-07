from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi_utils.cbv import cbv

from analytics.expenses.schemas import (
    MonthlyCategoryExpense,
    TotalExpenseCategoryDistribution,
)
from analytics.expenses.service import ExpensesService

expenses_router = APIRouter(prefix="/expenses-analysis", tags=["Expenses Analysis"])


@cbv(expenses_router)
class ExpensesController:
    service: ExpensesService = Depends()

    @expenses_router.get("/expenses/{user_id}/monthly-by-category", response_model=list[MonthlyCategoryExpense])
    def get_monthly_expenses_by_category_type(
            self,
            user_id: UUID,
            is_recurring_expense: Optional[bool] = Query(None, description="Filter by recurring expenses."),
    ):
        return self.service.get_monthly_expenses_by_category(user_id, is_recurring_expense)
    @expenses_router.get("/expenses/{user_id}/distribution", response_model=list[TotalExpenseCategoryDistribution])
    def get_total_expense_distribution(self, user_id: UUID):
        return self.service.get_total_expense_distribution(user_id)

from pydantic import BaseModel


class MonthlyExpense(BaseModel):
    year: int
    month: int
    category_type_name: str
    category_name: str
    is_positive: bool
    percentage: float
    total_amount: float


class TotalExpenseCategoryDistribution(BaseModel):
    category_type_name: str
    percentage: float
from fastapi import FastAPI

from categories.controller import categories_router
from expenses.controller import expenses_router

app = FastAPI(title="MWU (Money With You)",
              description="Application to help families manage their user expenses. "
                          "The application allows you to import receipts and monthly bills (water, electricity, gas),"
                          "automatically categorize these expenses, and generate monthly and annual expense reports.")

app.include_router(categories_router)
app.include_router(expenses_router)

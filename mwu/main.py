import uvicorn
from fastapi import FastAPI

from accounts.controller import accounts_router
from categories.controller import categories_router
from financial_goals.controller import financial_goals_router
from transactions.controller import transactions_router
from user.controller import users_router
from user_account.controller import user_account_router

app = FastAPI(title="MWU (Money With You)",
              description="Application to help families manage their user transactions. "
                          "The application allows you to import receipts and monthly bills (water, electricity, gas),"
                          "automatically categorize these transactions, and generate monthly and annual expense reports.")

app.include_router(accounts_router)
app.include_router(user_account_router)
app.include_router(users_router)

app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(financial_goals_router)


if __name__ == "__main__":
    uvicorn.run("mwu.main:app", host="127.0.0.1", port=8000, reload=True)

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "MWU": "Money With You",
        "Description": "Application to help families manage their user expenses. "
                       "The application allows you to import receipts and monthly bills (water, electricity, gas),"
                       "automatically categorize these expenses, and generate monthly and annual expense reports."
    }


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

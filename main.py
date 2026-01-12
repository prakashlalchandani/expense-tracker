from fastapi import FastAPI
from database import engine
from models import sql_models

# Import both routers
from routers import expenses, auth

# Create Tables
sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Routers
app.include_router(expenses.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is LIVE"}
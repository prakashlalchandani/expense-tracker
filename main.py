from fastapi import FastAPI
from database import engine
from models import sql_models

# Import both routers
from routers import auth, expenses, users

# Create Tables
sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(expenses.router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is LIVE"}
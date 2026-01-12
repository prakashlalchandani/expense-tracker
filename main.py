from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import datetime
import models
import database

# create the tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# the session manager
# this function yields a database session to anyone who asks for it
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# pydantic model (validator)
class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: str


# API routes
@app.post("/add-expense")
# Notice the new argument: db: Session = Depends(get_db)
# FastAPI automatically runs get_db(), gets the session, and passes it here.
def add_new_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):

    # 1. Create the Database Object (SQLAlchemy Model)
    # We map the Pydantic data (expense.category) to the SQL Model columns
    db_expense = models.Expense(
        date=str(datetime.date.today()),
        category=expense.category,
        amount=expense.amount,
        description=expense.description
    )

    # Add to the "staging area"
    db.add(db_expense)

    # commit (save to hard drive)
    db.commit()
    
    # refresh (get the new id created by the DB)
    db.refresh(db_expense)

    return {"status": "Expense Added", "id": db_expense.id, "data": expense}

@app.get("/get-expenses")
def get_all_expenses(db: Session = Depends(get_db)):
    # SQL translation: "SELECT * FROM expenses"
    all_expenses = db.query(models. Expense).all()
    return all_expenses

@app.get("/get-summary")
def get_summary(db: Session = Depends(get_db)):
    # SQL translation: "SELECT * FROM expenses"
    expenses = db.query(models.Expense).all()

    # We can still use Python/Pandas logic for the summary if we want!
    # Or simple Python math:
    total = 0
    breakdown = {}

    for x in expenses:
        total += x.amount
        if x.category in breakdown:
            breakdown[x.category] += x.amount
        else:
            breakdown[x.category] = x.amount
            
    return {"total_spent": total, "breakdown": breakdown}


@app.delete("/delete-expense/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    # 1. Find the expense by ID
    # SQL Translation: SELECT * FROM expenses WHERE id = expense_id
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    # check if it exists
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # delete it
    # SQL Transaction DELETE from expense where id = ...
    db.delete(expense)
    db.commit()

    return {"status": "success", "message": "Expense deleted successfully"}


@app.put("update-expense/{expense_id}")
def update_expense(expense_id: int, expense_update: ExpenseCreate, db: Session = Depends(get_db)):

    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    # check if exists
    if db_expense in None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # update the fields (overwrite old data with new data)
    db_expense.category = expense_update.category
    db_expense.amount = expense_update.amount
    db_expense.description = expense_update.description

    # save change
    db.commit()
    db.refresh(db_expense)

    return {"status": "Success", "data": db_expense}
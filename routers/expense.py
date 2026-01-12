from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import datetime

# UPDATED IMPORTS based on new folder structure
from database import get_db
from models import sql_models, schemas

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# 1. CREATE
@router.post("/add", response_model=schemas.ExpenseResponse)
def add_new_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = sql_models.Expense(
        date=str(datetime.date.today()),
        category=expense.category,
        amount=expense.amount,
        description=expense.description
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# 2. READ ALL
@router.get("/all", response_model=List[schemas.ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(sql_models.Expense).all()

# 3. SUMMARY
@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    expenses = db.query(sql_models.Expense).all()
    total = 0
    breakdown = {}
    
    for x in expenses:
        if x.amount is None:
            continue
        total += x.amount
        if x.category in breakdown:
            breakdown[x.category] += x.amount
        else:
            breakdown[x.category] = x.amount
            
    return {"total_spent": total, "breakdown": breakdown}

# 4. DELETE
@router.delete("/delete/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(sql_models.Expense).filter(sql_models.Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return {"status": "success", "message": "Expense deleted successfully"}

# 5. UPDATE
@router.put("/update/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense_update: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = db.query(sql_models.Expense).filter(sql_models.Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db_expense.category = expense_update.category
    db_expense.amount = expense_update.amount
    db_expense.description = expense_update.description
    
    db.commit()
    db.refresh(db_expense)
    return db_expense
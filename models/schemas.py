from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: str

class ExpenseResponse(ExpenseCreate):
    id: int
    date: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
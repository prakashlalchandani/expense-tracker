from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import sql_models, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# create user
@router.post("/create", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
                # check if email already exists
                existing_user = db.query(sql_models.User).filter(sql_models.User.email == user.email).first()
                if existing_user:
                        raise HTTPException(status_code=400, detail="Email already registered")
                
                # create new user
                new_user = sql_models.User(
                        username = user.username,
                        email = user.email,
                        password = user.password
                )

                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user

# get user profile
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
        user = db.query(sql_models.User).filter(sql_models.User.id == user_id).first()
        if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user
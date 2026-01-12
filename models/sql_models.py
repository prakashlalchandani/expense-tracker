from sqlalchemy import Column, Integer, Float, String
from database import Base


class User(Base):
    
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Expense(Base):
    
    # name of the table in the database
    __tablename__= "expenses"

    # columns (spreadsheet headers)
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    category = Column(String)
    amount = Column(Float)
    description = Column(String)

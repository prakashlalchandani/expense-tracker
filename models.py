from sqlalchemy import Column, Integer, String, Float
from database import Base

class Expense(Base):
    
    # name of the table in the database
    __tablename__= "expense"

    # columns (spreadsheet headers)
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    category = Column(String)
    amount = Column(Float)
    description = Column(String)

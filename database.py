from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# database url
# This tells Python: "Use SQLite, and save the file as 'sql_app.db'"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. The SessionLocal
# Each time we talk to the DB, we open a "Session". 
# This Class is the factory that creates those sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base
# A class that all our Database Models will inherit from.
Base = declarative_base()
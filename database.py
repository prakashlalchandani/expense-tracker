from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# 1. THE DATABASE URL
# ---------------------------------------------------------
# This string tells SQLAlchemy WHERE to look and WHAT language to speak.
# - "sqlite": The type of database (could be 'postgresql', 'mysql', etc.)
# - "///": Means "relative path" (look in the current folder).
# - "./sql_app.db": The name of the file that will be created on your hard drive.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# ---------------------------------------------------------
# 2. THE ENGINE (The Physical Connection)
# ---------------------------------------------------------
# The Engine is the starting point for any SQLAlchemy application.
# It is the actual "pipe" that connects your Python code to the file on the disk.
# 
# connect_args={"check_same_thread": False}:
# This is a special setting ONLY for SQLite.
# - By default, SQLite only allows the thread that created the connection to use it.
# - FastAPI uses multiple threads (async) to handle requests faster.
# - This setting tells SQLite: "It's okay, let other threads use this connection too."
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ---------------------------------------------------------
# 3. THE SESSION MAKER (The Factory)
# ---------------------------------------------------------
# Think of 'engine' as the electricity grid. You don't plug your toaster directly
# into the high-voltage line. You use a wall socket.
#
# 'SessionLocal' is a Class (a Factory) that creates those "wall sockets" (Sessions).
# Every time a user makes a request (e.g., "Add Expense"), we will create 
# a NEW instance of this class to handle just that one request.
#
# - autocommit=False: We want to explicitly say "db.commit()" only when we are sure
#   everything is correct. We don't want the DB to save automatically after every line.
# - autoflush=False: Prevents the DB from refreshing data while we are still editing it.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------
# 4. THE BASE (The Blueprint)
# ---------------------------------------------------------
# This function returns a Class.
# Later, in 'models.py', we will say: "class Expense(Base):"
# This tells SQLAlchemy: "Hey, this 'Expense' class is a Database Table, 
# please track it using the features inside 'Base'."
Base = declarative_base()

# ---------------------------------------------------------
# 5. THE DEPENDENCY (The Manager)
# ---------------------------------------------------------
# This is the most critical function for FastAPI.
# It manages the lifecycle of a database session.
def get_db():
    # A. OPEN: Create a new database session for this specific request.
    db = SessionLocal()
    try:
        # B. USE: 'yield' gives the session to the function (e.g., 'add_new_expense').
        # The function runs its code, and this function PAUSES here.
        yield db
    finally:
        # C. CLOSE: This runs AFTER the request is finished (even if there was an error!).
        # It closes the connection to free up resources.
        # If we didn't do this, the database would eventually freeze from too many open connections.
        db.close()
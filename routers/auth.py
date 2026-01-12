from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/login")
def login():
    return {"message": "This will be the login page soon!"}
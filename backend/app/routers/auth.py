# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.models.user import User
from app.dependencies import get_db  # Import the shared get_db dependency

# Define get_db here or import from a shared location
# def get_db():
#     from app.models.database import SessionLocal
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    print(f"Attempting login for user(auth.py): {form_data.username}")
    print(f"Attempting login for user(auth.py): {form_data.password}")
    print(f"User found: {user is not None}")
    if not user or not verify_password(form_data.password, user.hashed_password):
        print("Invalid credentials")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    print(f"Login successful for user: {form_data.username}")
    return {"access_token": token, "token_type": "bearer"}

from app.core.auth_utils import get_current_user

@router.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):
    print(f"Accessing dashboard for user: {current_user.username}")  
    return {"message": f"Welcome {current_user.username}!"}



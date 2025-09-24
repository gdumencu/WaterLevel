# backend\app\core\auth_utils.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db  # careful with circular imports

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("userName")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return db.query(User).filter(User.username == username).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

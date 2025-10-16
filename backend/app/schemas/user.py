# backend/app/schemas/user.py
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


# ----------------------
# Base model for shared fields
# ----------------------
class UserBase(BaseModel):
    username: Annotated[str, constr(min_length=3, max_length=50)]
    email: EmailStr
    role: Annotated[str, constr(min_length=3, max_length=20)]
    is_active: Optional[bool] = True


# ----------------------
# Model used for creating new users
# ----------------------
class UserCreate(UserBase):
    password: Annotated[str, constr(min_length=6)]  # plain password input


# ----------------------
# Model used for returning users (read-only)
# ----------------------
class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Important for SQLAlchemy integration


# ----------------------
# Model used for updating existing users
# ----------------------
class UserUpdate(BaseModel):
    username: Optional[Annotated[str, constr(min_length=3, max_length=50)]] = None
    email: Optional[EmailStr] = None
    role: Optional[Annotated[str, constr(min_length=3, max_length=20)]] = None
    is_active: Optional[bool] = None
    password: Optional[Annotated[str, constr(min_length=6)]] = None

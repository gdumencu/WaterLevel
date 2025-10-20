# backend/app/auth/dependencies.py

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from typing import Dict
# from jose import jwt, JWTError

# # OAuth2 scheme for JWT bearer token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# # Secret key for JWT decoding (replace with your actual secret)
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"

# def get_current_user_with_role(token: str = Depends(oauth2_scheme)) -> Dict:
#     """
#     Extracts user info and role from JWT token.
#     Raises 401 if token is invalid or expired.
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("username")
#         role: str = payload.get("role")
#         if username is None or role is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials",
#             )
#         return {"username": username, "role": role}
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )

# backend/auth/utils.py

from fastapi import Depends, HTTPException, status
from .dependencies import get_current_user_with_role

def admin_only(user=Depends(get_current_user_with_role)):
    """
    Allows access only to Admin users.
    """
    if user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

def operator_or_admin(user=Depends(get_current_user_with_role)):
    """
    Allows access to Operator and Admin users.
    """
    if user["role"] not in ["Admin", "Operator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator or Admin access required"
        )

def all_roles(user=Depends(get_current_user_with_role)):
    """
    Allows access to all authenticated users.
    """
    pass  # No restriction

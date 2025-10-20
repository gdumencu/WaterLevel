# backend/app/auth/utils.py

from fastapi import Depends, HTTPException, status
from app.core.auth_utils import get_current_user_with_role  # Import from auth_utils.py

# ----------------------------
# Role-based access dependencies
# ----------------------------

def admin_only(user=Depends(get_current_user_with_role)):
    """
    Dependency to allow access only to Admin users.
    
    Raises HTTP 403 if the user's role is not 'admin'.
    """
    print(f"[DEBUG] Checking admin access for user: {user}")
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

def operator_or_admin(user=Depends(get_current_user_with_role)):
    """
    Dependency to allow access to users with 'operator' or 'admin' roles.
    
    Raises HTTP 403 if the user's role is not 'operator' or 'admin'.
    """
    if user["role"] not in ["admin", "operator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator or Admin access required"
        )

def all_roles(user=Depends(get_current_user_with_role)):
    """
    Dependency for any authenticated user, regardless of role.
    
    Does not restrict access; just ensures the user is authenticated.
    """
    return user  # Simply returns user info; no restriction

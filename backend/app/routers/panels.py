# backend/routes/panels.py
from fastapi import APIRouter, Depends
from ..auth.utils import admin_only, operator_or_admin, all_roles

router = APIRouter(tags=["Panels"])

@router.get("/uart-config")
def get_uart_config(user=Depends(admin_only)):
    """
    UART Config panel - Admin only
    """
    return {"panel": "UART Config", "access": "Admin"}

@router.get("/job-config")
def get_job_config(user=Depends(operator_or_admin)):
    """
    Job Config panel - Admin and Operator
    """
    return {"panel": "Job Config", "access": "Admin, Operator"}

@router.get("/chart")
def get_chart_panel(user=Depends(all_roles)):
    """
    Chart panel - All roles
    """
    return {"panel": "Chart", "access": "All"}

@router.get("/data-view")
def get_data_view_panel(user=Depends(operator_or_admin)):
    """
    Raw & Aggregate Data panel - Admin and Operator
    """
    return {"panel": "Raw & Aggregate Data", "access": "Admin, Operator"}

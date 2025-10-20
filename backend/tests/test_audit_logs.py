"""
tests/test_audit_logs.py
Integration tests for Audit Logging endpoints (Task T8 - Lock/Unlock)
"""

from fastapi.testclient import TestClient
from app.main import app
from app.models import AuditLog
from app.db.database import get_db
from datetime import datetime, timedelta
import jwt

client = TestClient(app)

# Helper to create JWT token for test users
def create_token(user_id: str, role: str):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, "test-secret", algorithm="HS256")

# Mock user and token
mock_user_id = "test-user"
mock_token = create_token(mock_user_id, "admin")

# -----------------------------
# Test: Fetch logs for current user
# -----------------------------
def test_get_my_audit_logs():
    headers = {
        "Authorization": f"Bearer {mock_token}",
        "X-User": mock_user_id
    }
    response = client.get("/api/audit/logs/me?start=2025-10-01&end=2025-10-31", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for entry in response.json():
        assert entry["action"] in ["lock", "unlock"]
        assert entry["role"] in ["admin", "operator"]
        assert "created_at" in entry

# -----------------------------
# Test: Unauthorized access
# -----------------------------
def test_unauthorized_access():
    response = client.get("/api/audit/logs/me")
    assert response.status_code == 401

# -----------------------------
# Test: Role restriction
# -----------------------------
def test_viewer_cannot_access_logs():
    viewer_token = create_token("viewer-user", "viewer")
    headers = {
        "Authorization": f"Bearer {viewer_token}",
        "X-User": "viewer-user"
    }
    response = client.get("/api/audit/logs/me", headers=headers)
    assert response.status_code == 403  # Forbidden for viewers
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.setup_test_users import create_test_user
from app.dependencies import get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_users():
    create_test_user("testuser", "testpass")
    create_test_user("admin", "adminpass")

# Fixture for test user credentials
@pytest.fixture
def test_user():
    return {"username": "testuser", "password": "testpass"}

# Test login endpoint
def test_login_success(test_user):
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test login failure
def test_login_failure():
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"

# Test protected route access
def test_protected_route():
    login = client.post("/login", data={"username": "testuser", "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


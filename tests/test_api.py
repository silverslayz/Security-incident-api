"""
Basic API tests for Security Incident Management API.
Run with: pytest tests/
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Security Incident Management API"
    assert data["status"] == "operational"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_user_registration():
    """Test user registration endpoint"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "role": "viewer"
    }

    response = client.post("/api/v1/auth/register", json=user_data)

    # Note: This will fail on second run (duplicate user)
    # In production, use a test database or cleanup
    if response.status_code == 201:
        assert response.json()["username"] == user_data["username"]
        assert response.json()["email"] == user_data["email"]
    elif response.status_code == 400:
        assert "already registered" in response.json()["detail"]


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_incidents_requires_auth():
    """Test that incident endpoints require authentication"""
    response = client.get("/api/v1/incidents/")
    assert response.status_code == 403  # Forbidden without auth


def test_api_docs_available():
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200


# Additional tests to add:
# - Test full authentication flow (register -> login -> access protected endpoint)
# - Test RBAC (different roles accessing different endpoints)
# - Test incident CRUD operations
# - Test audit logging
# - Test input validation (invalid data)
# - Test pagination and filtering

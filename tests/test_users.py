import jwt
import pytest
from app import schemas
from app.config import settings


def test_root(client):
    resp = client.get("/")
    print(resp.json().get("message"))
    assert resp.json().get("message") == 'Welcome to my FastAPI application!'
    assert resp.status_code == 200


def test_create_user(client):
    resp = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    new_user = schemas.UserCreateResponse(**resp.json())
    assert isinstance(new_user.data.id, int)
    assert new_user.data.email == "test@example.com"
    assert resp.status_code == 201
    assert resp.json().get("message") == "User created successfully"


def test_login_user(client, test_user):
    resp = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = schemas.Token(**resp.json())
    payload = jwt.decode(token.access_token, settings.jwt_secret_key, algorithms=[settings.algorithm])
    assert payload.get("user_id") == test_user["id"]
    assert isinstance(token.access_token, str)
    assert token.token_type == "bearer"
    assert resp.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("test@example.com", "wrongpassword", 403),
    ("mark@example.com", "testpassword", 403),
    ("john@gmail.com", "wrongpassword", 403),
    (None, "testpassword", 422),
    ("sna@gmail.com", None, 422),
])
def test_incorrect_login(client, email, password, status_code):
    resp = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )
    assert resp.status_code == status_code
    if status_code == 403:
        assert resp.json().get("detail") == "Invalid Credentials"

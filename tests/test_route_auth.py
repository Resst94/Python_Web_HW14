from unittest.mock import Mock

from sqlalchemy import select

from src.database.models import User
from tests.conftest import TestingSessionLocal

user_data = {"username": "agent007", "email": "agent007@gmail.com", "password": "12345678"}


def test_create_user(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user_data.get("email")
    assert "id" in data["user"]
    assert "password" not in data


def test_repeat_create_user(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user_data
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client):
    response = client.post(
        "/api/auth/login",
        data={"username": user_data.get('email'), "password": user_data.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_user(client, session):
    with TestingSessionLocal() as session:
        current_user = session.execute(select(User).where(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            session.commit()

    response = client.post("api/auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


def test_login_wrong_password(client):
    response = client.post(
        "/api/auth/login",
        data={"username": user_data.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_wrong_email_login(client):
    response = client.post("api/auth/login",
                           data={"username": "email", "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


def test_validation_error_login(client):
    response = client.post("api/auth/login",
                           data={"password": user_data.get("password")})
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data

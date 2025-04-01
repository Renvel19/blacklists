import json
import pytest

from flask_jwt_extended import create_access_token

from src import create_app
from src.db import db

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def get_headers(token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

def test_get_token_success(client):
    response = client.get("/blacklists/token")

    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 10

def test_get_not_blocked_user_success(client):
    token = create_access_token(identity="test")


    response = client.get(
        "/blacklists/ejemplo@correo.com",
        headers=get_headers(token)
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "El usuario no está bloqueado"
    assert response.get_json()["isBlocked"] == False
    assert len(response.get_json()["reasons"]) == 0

def test_get_blocked_user_success(client):
    token = create_access_token(identity="test")


    response = client.get(
        "/blacklists/test1@test.co",
        headers=get_headers(token)
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "El usuario está bloqueado"
    assert response.get_json()["isBlocked"] == True
    assert len(response.get_json()["reasons"]) > 0

def test_get__invalid_email(client):
    token = create_access_token(identity="test")

    response = client.get(
        "/blacklists/ejemplo@",
        headers=get_headers(token)
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Formato de correo electrónico inválido"


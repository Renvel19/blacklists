import json
from src import create_app
from src.db import db

import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import patch

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


def test_post_blacklist_success(client):
    token = create_access_token(identity="test")
    payload = {
        "email": "ejemplo@correo.com",
        "app_uuid": "a8eab7b6-6e9a-4e7d-ae5a-df6a3b4191a7",
        "blocked_reason": "Razón de prueba"
    }

    response = client.post(
        "/blacklists",
        data=json.dumps(payload),
        headers=get_headers(token)
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "Email agregado a la lista negra exitosamente"


def test_post_blacklist_invalid_email(client):
    token = create_access_token(identity="test")
    payload = {
        "email": "invalido",
        "app_uuid": "a8eab7b6-6e9a-4e7d-ae5a-df6a3b4191a7",
        "blocked_reason": "Motivo"
    }

    response = client.post(
        "/blacklists",
        data=json.dumps(payload),
        headers=get_headers(token)
    )

    assert response.status_code == 400
    assert "Formato de correo electrónico inválido" in response.get_json()["message"]

def test_post_blacklist_missing_fields(client):
    token = create_access_token(identity="test")

    payload = {
        "email": "falta_uuid@example.com"
    }

    response = client.post(
        "/blacklists",
        data=json.dumps(payload),
        headers=get_headers(token)
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Faltan campos obligatorios"

def test_post_blacklist_invalid_uuid(client):
    token = create_access_token(identity="test")

    payload = {
        "email": "uuid-malo@example.com",
        "app_uuid": "esto-no-es-un-uuid",
        "blocked_reason": "Motivo válido"
    }

    response = client.post(
        "/blacklists",
        data=json.dumps(payload),
        headers=get_headers(token)
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "UUID de la app inválido"

def test_post_blacklist_reason_too_long(client):
    token = create_access_token(identity="test")

    payload = {
        "email": "muylargo@example.com",
        "app_uuid": "a8eab7b6-6e9a-4e7d-ae5a-df6a3b4191a7",
        "blocked_reason": "A" * 256
    }

    response = client.post(
        "/blacklists",
        data=json.dumps(payload),
        headers=get_headers(token)
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "El motivo no puede exceder 255 caracteres"


def test_post_blacklist_db_error(client):
    token = create_access_token(identity="test")

    payload = {
        "email": "dberror@example.com",
        "app_uuid": "a8eab7b6-6e9a-4e7d-ae5a-df6a3b4191a7",
        "blocked_reason": "Simular fallo en DB"
    }

    with patch("src.blueprints.blacklist.db.session.commit") as mock_commit:
        mock_commit.side_effect = Exception("Simulando error de base de datos")

        response = client.post(
            "/blacklists",
            data=json.dumps(payload),
            headers=get_headers(token)
        )

        assert response.status_code == 500
        body = response.get_json()
        assert body["message"] == "Error al guardar en la base de datos"
        assert "Simulando error de base de datos" in body["error"]
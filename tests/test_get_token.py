import json
from src import create_app
from src.db import db
import pytest


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


def test_get_token_success(client):
    response = client.get("/blacklists/token")

    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 10

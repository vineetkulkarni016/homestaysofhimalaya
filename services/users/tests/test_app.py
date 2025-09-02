from fastapi.testclient import TestClient

from services.users.app import app
from services.common.auth import create_access_token

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200


def test_secure():
    token = create_access_token({"sub": "tester"})
    r = client.get("/secure", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["user"] == "tester"

import pytest
from fastapi.testclient import TestClient

from main import app, emails

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean():
    emails.clear()
    yield
    emails.clear()


def test_signup():
    r = client.post("/signup", json={"email": "Ada@X.org", "age": 36})
    assert r.status_code == 201
    assert r.json() == {"email": "ada@x.org"}


def test_duplicate():
    client.post("/signup", json={"email": "ada@x.org", "age": 36})
    r = client.post("/signup", json={"email": "ADA@x.org", "age": 36})
    assert r.status_code == 409


@pytest.mark.parametrize("age, code", [(12, 422), (13, 201)])
def test_age_limit(age, code):
    r = client.post("/signup", json={"email": f"kid{age}@x.org", "age": age})
    assert r.status_code == code

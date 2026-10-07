from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_book():
    r = client.post("/books", json={"title": "Dune", "year": 1965})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "Dune", "year": 1965}


def test_read_missing():
    r = client.get("/books/999")
    assert r.status_code == 404


def test_empty_title():
    r = client.post("/books", json={"title": "", "year": 1965})
    assert r.status_code == 422

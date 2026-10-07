from fastapi.testclient import TestClient

from main import app, books

client = TestClient(app)


def test_add_first():
    r = client.post("/books", json={"title": "Dune", "year": 1965})
    assert r.status_code == 201
    assert len(books) == 1


def test_add_second():
    client.post("/books", json={"title": "Emma", "year": 1815})
    assert len(books) == 1


def test_starts_empty():
    assert books == {}

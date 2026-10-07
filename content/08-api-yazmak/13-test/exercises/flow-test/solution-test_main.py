from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_book_lifecycle():
    created = client.post("/books", json={"title": "Dune", "year": 1965})
    assert created.status_code == 201
    book_id = created.json()["id"]

    read = client.get(f"/books/{book_id}")
    assert read.status_code == 200
    assert read.json() == {"title": "Dune", "year": 1965}

    assert client.delete(f"/books/{book_id}").status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404

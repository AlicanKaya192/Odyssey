import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize("score, letter", [
    (100, "A"), (90, "A"), (89, "B"), (80, "B"), (70, "C"), (69, "F"), (0, "F"),
])
def test_letters(score, letter):
    r = client.get("/grade", params={"score": score})
    assert r.status_code == 200
    assert r.json()["letter"] == letter


@pytest.mark.parametrize("score", [-1, 101])
def test_out_of_range(score):
    assert client.get("/grade", params={"score": score}).status_code == 422

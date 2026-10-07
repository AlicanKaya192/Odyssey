from fastapi.testclient import TestClient

from main import app, require_key

client = TestClient(app)


def test_stats_need_a_key():
    assert client.get("/admin/stats").status_code == 401


def test_stats_with_override():
    app.dependency_overrides[require_key] = lambda: None
    try:
        r = client.get("/admin/stats")
        assert r.status_code == 200
        assert r.json() == {"books": 3}
    finally:
        app.dependency_overrides.clear()

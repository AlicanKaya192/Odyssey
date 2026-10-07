from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Testlerini buraya yaz: def test_...(): ve assert

from fastapi.testclient import TestClient

from main import app, emails

client = TestClient(app)

# Testlerini yaz: 201 + kucuk harfli e-posta, ayni e-posta 409, yas siniri (12 -> 422, 13 -> 201)
# emails kumesini her testten once temizle

from fastapi.testclient import TestClient

from main import app, emails

client = TestClient(app)

# Write your tests: 201 + the lower-cased email, the same email 409, the age limit (12 -> 422, 13 -> 201)
# clear the emails set before every test

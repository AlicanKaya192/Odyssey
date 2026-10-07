from fastapi.testclient import TestClient

from main import app, require_key

client = TestClient(app)

# 1) anahtarsiz istek 401
# 2) require_key'i dependency_overrides ile degistirip /admin/stats -> {"books": 3}

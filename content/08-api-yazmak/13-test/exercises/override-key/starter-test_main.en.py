from fastapi.testclient import TestClient

from main import app, require_key

client = TestClient(app)

# 1) a request without a key gives 401
# 2) swap require_key with dependency_overrides and /admin/stats -> {"books": 3}

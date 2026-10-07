from fastapi import FastAPI, HTTPException

app = FastAPI()
reports = {1: "ready", 2: "pending"}

# GET /reports/{report_id}:
#   yoksa 404, detail {"code": "not_found"}
#   "pending" ise 503, detail {"code": "not_ready"}, baslik Retry-After: 30
#   "ready" ise {"id": .., "status": "ready"}

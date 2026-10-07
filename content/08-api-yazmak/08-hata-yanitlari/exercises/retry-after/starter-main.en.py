from fastapi import FastAPI, HTTPException

app = FastAPI()
reports = {1: "ready", 2: "pending"}

# GET /reports/{report_id}:
#   missing -> 404, detail {"code": "not_found"}
#   "pending" -> 503, detail {"code": "not_ready"}, header Retry-After: 30
#   "ready" -> {"id": .., "status": "ready"}

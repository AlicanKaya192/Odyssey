from fastapi import FastAPI, HTTPException

app = FastAPI()
reports = {1: "ready", 2: "pending"}


@app.get("/reports/{report_id}")
def get_report(report_id: int):
    if report_id not in reports:
        raise HTTPException(status_code=404, detail={"code": "not_found"})
    if reports[report_id] == "pending":
        raise HTTPException(status_code=503, detail={"code": "not_ready"},
                            headers={"Retry-After": "30"})
    return {"id": report_id, "status": "ready"}

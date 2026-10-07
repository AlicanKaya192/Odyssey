from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()
jobs = []


class Report(BaseModel):
    rows: int = Field(ge=1)


@app.post("/reports")
def make_report(report: Report):
    if report.rows > 1000:
        jobs.append(report.rows)
        return JSONResponse(status_code=202, content={"queued": True, "position": len(jobs)})
    return {"rows": report.rows, "status": "done"}

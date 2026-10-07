from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()
jobs = []


class Report(BaseModel):
    rows: int = Field(ge=1)


# POST /reports:
#   rows 1000'i gecmiyorsa -> 200, {"rows": rows, "status": "done"}
#   rows > 1000 -> jobs listesine ekle, 202, {"queued": true, "position": len(jobs)}

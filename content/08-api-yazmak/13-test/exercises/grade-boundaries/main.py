from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/grade")
def grade(score: Annotated[int, Query(ge=0, le=100)]):
    if score >= 90:
        letter = "A"
    elif score >= 80:
        letter = "B"
    elif score >= 70:
        letter = "C"
    else:
        letter = "F"
    return {"score": score, "letter": letter}

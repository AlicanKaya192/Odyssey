from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/tags")
def tags(tag: list[str] = Query(default=[])):
    return {"tags": sorted(tag), "count": len(tag)}

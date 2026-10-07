from fastapi import FastAPI, Query

app = FastAPI()

# GET /tags?tag=b&tag=a -> {"tags": abece sirasiyla, "count": kac tane}

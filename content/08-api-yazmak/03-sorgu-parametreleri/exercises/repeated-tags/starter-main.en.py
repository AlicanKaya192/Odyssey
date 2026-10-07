from fastapi import FastAPI, Query

app = FastAPI()

# GET /tags?tag=b&tag=a -> {"tags": in alphabetical order, "count": how many}

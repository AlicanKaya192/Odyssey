from fastapi import FastAPI

app = FastAPI()
state = {"count": 0}

# GET /counter: state'i dondur
# POST /counter: sayiyi 1 artir ve state'i dondur

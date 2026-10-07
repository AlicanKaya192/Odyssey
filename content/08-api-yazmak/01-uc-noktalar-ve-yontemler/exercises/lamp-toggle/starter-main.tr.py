from fastapi import FastAPI

app = FastAPI()
lamp = {"on": False}

# GET /lamp: lambanin durumu
# POST /lamp/toggle: acsa kapat, kapaliysa ac; yeni durumu dondur

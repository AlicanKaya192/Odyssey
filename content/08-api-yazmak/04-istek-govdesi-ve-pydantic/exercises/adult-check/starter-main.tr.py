from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# User modeli: name (metin), age (tam sayi)
# POST /users -> {"name", "age", "adult": 18 ve ustu mu}

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Settings modeli: theme ("dark"), font_size (14), beta (False) - hepsinin varsayilani var
# POST /settings -> modeli oldugu gibi dondur

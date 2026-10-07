from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Book modeli:
#   title: 1-80 karakter
#   year: 1450 ile 2100 arasi (ikisi de dahil)
#   pages: 0'dan buyuk
# POST /books -> 201, kitabi oldugu gibi dondur

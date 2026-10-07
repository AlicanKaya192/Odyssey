from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Book: title (ornek "Dune", aciklama "The book's title"), year (ornek 1965, aciklama "Year of first publication")
# POST /books -> 201, kitabi dondur, tags ["books"]
# GET /old-books -> [] ; tags ["books"], belgede eskimis (deprecated) gorunsun

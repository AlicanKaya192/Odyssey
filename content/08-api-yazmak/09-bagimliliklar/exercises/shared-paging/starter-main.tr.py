from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI()
books = ["Dune", "Emma", "Ubik", "Kindred", "Beloved"]
movies = ["Alien", "Heat", "Up"]

# paging bagimliligi: limit (1-5, varsayilan 2), offset (0 ya da buyuk, varsayilan 0)
#   {"limit": .., "offset": ..} dondurur
# GET /books ve GET /movies ikisi de paging'i kullanarak dilim dondursun

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Book model:
#   title: 1-80 characters
#   year: between 1450 and 2100 (both included)
#   pages: greater than 0
# POST /books -> 201, return the book as it is

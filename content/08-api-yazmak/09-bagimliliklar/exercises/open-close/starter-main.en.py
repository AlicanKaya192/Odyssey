from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
items = {1: "pen", 2: "book"}
events = []

# get_conn: a yield dependency. First append "open" to events, give "conn",
#   append "close" when the endpoint is done (even on an error; try/finally)
# GET /items -> items (uses get_conn)
# GET /items/{item_id} -> {"id", "name"}; 404 "Item not found" if missing (uses get_conn)
# GET /events -> the events list (does NOT use get_conn)

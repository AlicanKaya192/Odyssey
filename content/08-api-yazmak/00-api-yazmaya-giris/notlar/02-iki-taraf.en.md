The server-side counterpart of everything you learned on the client side
in the Using APIs module. You can come back to this table throughout the module.

| Concept | Using APIs: client (requests) | Writing APIs: server (FastAPI) | Section |
|---|---|---|---|
| Method and address | `requests.get(BASE + "/books")` | `@app.get("/books")` | 01 |
| Path parameter | Building the `/books/42` address | `@app.get("/books/{book_id}")` + `book_id: int` | 02 |
| Query parameter | `params={"page": 2}` | `def list_books(page: int = 1)` | 03 |
| Body | `json={"title": "Dune"}` | `def add(book: Book)` (a Pydantic model) | 04 |
| Validation | Getting 422 | Field rules (`Field(min_length=1)`) | 05 |
| Status code | Reading `r.status_code` | `status_code=201`, `HTTPException(404)` | 06, 08 |
| CRUD | Sending GET / POST / PUT / DELETE | Writing four endpoints | 07 |
| Identity | `headers={"Authorization": ...}` | Reading and checking the header | 10 |
| Pagination | Fetching page by page with `page` | Slicing with `page`, `per_page` | 03, 09 |
| Rate limit, retry | Waiting on 429 and 5xx | Giving the right code at the right time | 08 |
| Docs | Reading the docs | `/docs` by itself | 15 |
| Tests | Seeing the answer with `print` | `TestClient` and pytest | 13 |

Keep in mind: as a client you asked "what does this API do?"; as a server
you will ask "what does this API promise?". Every endpoint is a promise:
if this request comes to this address, this answer with this code.

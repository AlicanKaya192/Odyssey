All of the track's patterns on one page.

## The application and endpoints

```python
from fastapi import FastAPI

app = FastAPI(title="Library API", version="1.0.0")


@app.get("/books/{book_id}")
def read_book(book_id: int, full: bool = False):
    ...
```

| Code | Meaning |
|---|---|
| `{book_id}` in the address | A path parameter |
| `full: bool = False` | An optional query |
| `book: Book` (a model) | The body |
| `Annotated[int, Query(ge=1)]` | A query with a rule |
| `Annotated[str, Header()]` | A header |

## Models and validation

```python
from pydantic import BaseModel, Field, field_validator


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1450, le=2100)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()
```

## The answer

| Code | What it does |
|---|---|
| `status_code=201` | The success code |
| `-> BookOut` / `response_model=BookOut` | Filters the answer |
| `raise HTTPException(404, detail="...")` | An error answer |
| `JSONResponse(status_code=202, content={...})` | A code decided on the spot |
| `response.headers["Location"] = ...` | A header |

## Dependencies and identity

```python
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    ...
```

## The database

| Code | What it does |
|---|---|
| `db.execute("... WHERE id = ?", (book_id,))` | A parameterised query |
| `.fetchone()` / `.fetchall()` | A row / rows |
| `db.commit()` | Make it permanent |
| `cur.lastrowid` / `cur.rowcount` | The new number / affected rows |

## Layout, tests, running

| Code | What it does |
|---|---|
| `APIRouter(prefix="/books", tags=["books"])` | A router for one file |
| `app.include_router(books.router)` | Add the router |
| `client = TestClient(app)` | A client in tests |
| `@pytest.fixture(autouse=True)` | Before every test |
| `uvicorn main:app --reload` | Run while developing |

## Status codes

`200` OK · `201` created · `204` no body · `400` a request that makes no
sense · `401` no identity · `403` not allowed · `404` not found · `409` a
clash · `422` validation · `500` a server error

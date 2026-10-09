# Overall Review

You've reached the end of the Writing APIs module. In the Using APIs module you were on one side of the table,
sending requests; now you can write the other side, the server that answers
them, from start to finish. In this section you see what you learned once
more through the journey of a request; then there's a 40-question mixed exam
and five exercises that bring the topics together.

## The journey of a request

<figure class="fig">
  <div class="flow">
    <span class="node">Middleware</span><span class="arrow">→</span>
    <span class="node acc">Depends<br><small>401 · 403</small></span><span class="arrow">→</span>
    <span class="node acc">Validation<br><small>422</small></span><span class="arrow">→</span>
    <span class="node">Endpoint<br><small>404 · 409</small></span><span class="arrow">→</span>
    <span class="node ok">Answer<br><small>201</small></span>
  </div>
  <figcaption>Each box is a section. A request stuck in one box never reaches the later ones; the code you get tells you where it got stuck.</figcaption>
</figure>

When a `POST /books` request reaches the server, this happens in order:

1. **Middleware** (15): in front of every request; starts timing.
2. **Routing** (01, 12): the address and method are matched to an endpoint;
   otherwise `404` / `405`.
3. **Dependencies** (09, 10): the key or token is checked (`401`, `403`), the
   database connection is opened (11).
4. **Validation** (02–05): the path, query and body must fit the template
   and rules; otherwise `422` and the function is never called.
5. **The endpoint** (07): does its job; `404` if not found, `409` on a clash
   (08).
6. **The response model** (06): the answer is filtered (the password doesn't
   go out), the status code is set (`201`).
7. On the way back, the `yield` dependency closes the connection, the
   middleware adds its header, and background tasks (14) run after the
   answer.

## Topics and sections

| Topic | Section | Main tools |
|---|---|---|
| Endpoints, methods | 00–01 | `@app.get`, `@app.post`, `uvicorn` |
| Path and query | 02–03 | `{book_id}`, `limit: int = 10` |
| Body and validation | 04–05 | `BaseModel`, `Field`, `field_validator` |
| The answer | 06 | `response_model`, `status_code`, `JSONResponse` |
| A full resource | 07 | `POST/GET/PUT/PATCH/DELETE`, `exclude_unset` |
| Errors | 08 | `HTTPException`, `exception_handler` |
| Dependencies | 09 | `Depends`, `yield`, `dependency_overrides` |
| Identity | 10 | `APIKeyHeader`, `HTTPBearer`, `pbkdf2_hmac`, `secrets` |
| A database | 11 | `sqlite3`, `?`, `commit`, `rowcount` |
| Project layout | 12 | `APIRouter`, `include_router` |
| Testing | 13 | `TestClient`, `pytest`, fixtures |
| async | 14 | `async def`, `await`, `gather`, `BackgroundTasks`, `lifespan` |
| Docs | 15 | `/docs`, `summary`, CORS, middleware |
| Serving a model | 16 | `joblib`, Pipeline, `int()`/`float()` |

## What do I do when?

| Situation | Do | Code |
|---|---|---|
| An incoming value may be nonsense | A rule on the field | `Field(ge=..., le=...)` → `422` |
| No such record | Raise an error | `HTTPException(404)` |
| The same name already exists | A clash | `409` (`IntegrityError` in SQLite) |
| The answer has a secret field | A response model | `response_model=UserOut` |
| The same code in three endpoints | A dependency | `Depends(...)` |
| I don't know who it is | Identity | `401` |
| I know, but they're not allowed | Permission | `403` |
| The data must persist | A database | `sqlite3` + `commit` |
| User input goes into a query | A parameter | `?` (never an f-string) |
| The file got too big | Split it | `APIRouter` |
| Did a change break something? | A test | `pytest` |
| There's a blocking call inside | A plain function | `def` (not async) |
| A model must load once | Startup | `lifespan` |
| The model returned NumPy | Convert | `int()`, `float()`, `.tolist()` |

## Traps we learned by measuring

Bugs found by running code along the track that produce a wrong result
**without an error**:

- Ids with `len(books) + 1`: a record is overwritten after a deletion (07).
- No `exclude_unset` in `PATCH`: fields not sent turn into `None` (07); a
  sent `null` makes the response model give `500`.
- Forgetting `return` in a validator: the field is `null` (05).
- Forgetting `commit`: `201` but no data (11).
- `time.sleep` inside `async def`: five times slower, no error (14).
- Forgetting the scaler: the same species for every flower (16).

The shared lesson: **seeming to work doesn't mean being right.** That's
exactly what tests (13) are for.

## From here

- **The Docker track:** putting this API in an image and running it the same
  everywhere.
- **From Here** in the notes: a real database (PostgreSQL), SQLAlchemy, JWT,
  continuous integration.

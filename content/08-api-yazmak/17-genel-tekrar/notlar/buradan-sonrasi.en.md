This track covered writing an API from start to finish. Here are the topics
and tools you'll meet when you move on to a real project.

## First: your own API

- Pick a subject (your library, your film list, your expenses) and write
  its CRUD.
- Make it persistent with SQLite, protect it with tokens, write its tests.
- Put it in an image the way you did in the Docker track.

## The next steps

| Topic | What it's for |
|---|---|
| PostgreSQL | A real database many users write to at once |
| SQLAlchemy / SQLModel | Writing SQL with Python classes (an ORM) |
| Alembic | Updating the database when the table layout changes (migrations) |
| JWT (`PyJWT`) | Signed tokens the server doesn't store |
| `bcrypt` / `argon2` | Password hashing as it's done in real projects |
| `httpx.AsyncClient` | Calling another API from an async endpoint |
| GitHub Actions | Running the tests on every push (named in the Git track's last note) |
| Observability (logging, metrics) | Watching what happens on the server |

## Resources

- **The FastAPI docs** (fastapi.tiangolo.com): tutorial and reference; the
  details of every topic in this track.
- **The Pydantic docs** (docs.pydantic.dev): every validation option.
- **MDN HTTP** (developer.mozilla.org): status codes, headers, CORS.

## Continuing in Odyssey

- The **Docker** track: running the API the same everywhere.
- **API 1**: using other APIs; now you know both sides.

`routers/books.py` says `from models import BookIn` but `models.py` is
empty; the application doesn't start.

**What to do:** write the `BookIn` model in `models.py`:

- `title`: at least 1 character
- `year`: 1450–2100

- `POST /books` `{"title": "Dune", "year": 1965}` → `201`, `{"id": 1, "title": "Dune", "year": 1965}`
- `POST /books` `{"title": "", "year": 1965}` → `422`
- `POST /books` `{"title": "X", "year": 3000}` → `422`

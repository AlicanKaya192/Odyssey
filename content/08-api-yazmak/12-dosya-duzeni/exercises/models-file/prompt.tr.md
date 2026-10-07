`routers/books.py` `from models import BookIn` diyor ama `models.py` boş;
uygulama açılmıyor.

**Yapman gereken:** `models.py`'ye `BookIn` modelini yaz:

- `title`: en az 1 karakter
- `year`: 1450–2100

- `POST /books` `{"title": "Dune", "year": 1965}` → `201`, `{"id": 1, "title": "Dune", "year": 1965}`
- `POST /books` `{"title": "", "year": 1965}` → `422`
- `POST /books` `{"title": "X", "year": 3000}` → `422`

The book API in `main.py` is ready (read-only). Write **at least three**
tests in `test_main.py`:

1. `POST /books` with a valid book returns `201` and
   `{"id": 1, "title": ..., "year": ...}`.
2. A missing book (`GET /books/999`) returns `404`.
3. An empty title (`{"title": "", ...}`) returns `422`.

Your tests will also run against broken versions of the application: for
every bug at least one must fail.

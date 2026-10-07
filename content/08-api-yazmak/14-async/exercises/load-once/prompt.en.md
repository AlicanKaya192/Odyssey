`load_words()` stands in for a slow load and increases `stats["loads"]` on
every call.

**What to do:**

1. `lifespan`: fill `words` with `load_words()` while the server starts
   (**once**), clear it while it stops. `app = FastAPI(lifespan=lifespan)`.
2. `GET /check?word=...` → `{"word": ..., "known": true/false}` (look it up
   lower-cased).
3. `GET /stats` → `stats`.

- `GET /check?word=Python` → `{"word": "Python", "known": true}`
- after several requests `GET /stats` → `{"loads": 1}`

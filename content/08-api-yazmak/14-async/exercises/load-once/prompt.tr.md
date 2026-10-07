`load_words()` yavaş bir yüklemenin yerine geçiyor ve her çağrıda
`stats["loads"]`'u artırıyor.

**Yapman gerekenler:**

1. `lifespan`: sunucu açılırken `words`'ü `load_words()` ile doldur
   (**bir kez**), kapanırken temizle. `app = FastAPI(lifespan=lifespan)`.
2. `GET /check?word=...` → `{"word": ..., "known": true/false}` (küçük
   harfe çevirip bak).
3. `GET /stats` → `stats`.

- `GET /check?word=Python` → `{"word": "Python", "known": true}`
- birkaç istekten sonra `GET /stats` → `{"loads": 1}`

Gerçek bir veritabanı bağlantısının provası: bağlantı her istekte açılıp
kapanacak, `events` listesi ne olduğunu kaydedecek.

**Yapman gerekenler:**

1. `get_conn`: `yield`'li bağımlılık. Önce `events`'e `"open"` ekle,
   `"conn"` ver; uç nokta bitince **hata olsa da** `"close"` ekle.
2. `GET /items` ve `GET /items/{item_id}` (`404`, `"Item not found"`)
   `get_conn` kullansın.
3. `GET /events` → `events` (bağlantı kullanmaz).

- `GET /items`, `GET /items/9` (`404`), `GET /events` → `["open", "close", "open", "close"]`

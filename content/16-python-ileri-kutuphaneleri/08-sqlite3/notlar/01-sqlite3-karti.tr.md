## Bağlantı

| Yazım | Ne yapar |
|---|---|
| `sqlite3.connect("app.db")` / `(":memory:")` | dosya / bellek |
| `conn.row_factory = sqlite3.Row` | satıra adla erişim |
| `with conn:` | işlem: başarıda commit, hatada rollback |
| `contextlib.closing(conn)` | blok sonunda kapat |

## Sorgu

| Yazım | Ne verir |
|---|---|
| `conn.execute(sql, (a, b))` | imleç (cursor) |
| `conn.execute(sql, {"ad": a})` | adlı yer tutucuyla (`:ad`) |
| `conn.executemany(sql, liste)` | toplu ekleme |
| `cur.fetchone()` / `fetchall()` | bir satır / hepsi |
| `for row in conn.execute(...)` | satır satır |
| `cur.rowcount`, `cur.lastrowid` | etkilenen satır, yeni kimlik |

## Tablo

```sql
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total REAL CHECK (total >= 0),
    day TEXT
);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders (customer);
```

## Türler

| Python | SQLite |
|---|---|
| `int`, `bool` | `INTEGER` (`bool` 0/1) |
| `float` | `REAL` |
| `str` | `TEXT` |
| `date`, `datetime` | `TEXT` (ISO) |
| `None` | `NULL` |

## Kurallar

- Değerler `?` ya da `:ad` ile; SQL metnine biçimlendirme yok.
- Birlikte olması gereken yazmalar tek `with conn:` bloğunda.
- Sık süzülen sütuna indeks; `EXPLAIN QUERY PLAN` ile bak.
- Tek parametre `(x,)`.

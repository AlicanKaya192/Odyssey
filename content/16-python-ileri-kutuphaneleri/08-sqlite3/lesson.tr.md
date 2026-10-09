# sqlite3

Python patikasının Veritabanı bölümünde `sqlite3` ile tablo kurdun, veri
ekledin ve sorguladın, `?` yer tutucusunun neden önemli olduğunu ve
`commit`'i gördün. Bu bölüm gerçek bir uygulamanın veritabanı katmanında
gereken ileri konuları anlatıyor: satırlara adla ulaşmak, toplu ekleme,
SQL enjeksiyonunun gerçekte nasıl çalıştığı, **işlemler** (transaction),
**indeksler** ve sorgu planı, tarihleri saklamak.

## Row ve executemany

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute(
    "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
rows = [("pen", 1.5), ("ink", 0.5), ("book", 12.0)]
conn.executemany("INSERT INTO products (name, price) VALUES (?, ?)", rows)
for row in conn.execute("SELECT * FROM products WHERE price > ?", (1,)):
    print(row["id"], row["name"], row["price"], dict(row))
print(conn.execute("SELECT COUNT(*) FROM products").fetchone()[0])
```

```text
1 pen 1.5 {'id': 1, 'name': 'pen', 'price': 1.5}
3 book 12.0 {'id': 3, 'name': 'book', 'price': 12.0}
3
```

- **`":memory:"`** veritabanını dosya yerine bellekte kurar: denemeler ve
  testler için.
- **`conn.row_factory = sqlite3.Row`**: satırlar demet yerine **adla**
  ulaşılabilen `Row` nesnesi olur (`row["name"]`); `dict(row)` sözlüğe
  çevirir. Sütun sırası değişince kod bozulmaz.
- **`executemany`** aynı sorguyu bir liste için tek çağrıda çalıştırır;
  binlerce satırda döngüyle `execute`'tan çok daha hızlıdır.
- `INTEGER PRIMARY KEY` kendiliğinden artan kimliktir (1, 2, 3).

## Enjeksiyon: neden ? yazılır

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, admin INTEGER)")
conn.execute("INSERT INTO users VALUES ('ada', 1), ('alan', 0)")
name = "x' OR '1'='1"
unsafe = f"SELECT name FROM users WHERE name = '{name}'"
print(conn.execute(unsafe).fetchall())
print(conn.execute("SELECT name FROM users WHERE name = ?", (name,)).fetchall())
named = "SELECT name FROM users WHERE name = :n"
print(conn.execute(named, {"n": "ada"}).fetchall())
```

```text
[('ada',), ('alan',)]
[]
[('ada',)]
```

Kullanıcının yazdığı `x' OR '1'='1` f-string ile sorguya yapıştırılınca
tırnağı kapatıp **sorgunun anlamını değiştirdi**: koşul her satır için doğru
oldu ve bütün kullanıcılar döndü. `?` ile verilen değer ise yalnızca **veri**
olarak gider; böyle bir ad yok, sonuç boş. Adlı yer tutucu (`:n` +
sözlük) çok parametreli sorgularda daha okunaklıdır. Kural: **SQL metnine
hiçbir değer biçimlendirerek yazılmaz.**

## İşlem: hep birlikte ya da hiç

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts "
             "(name TEXT PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")
conn.executemany("INSERT INTO accounts VALUES (?, ?)", [("ada", 100), ("alan", 20)])
conn.commit()
ADD = "UPDATE accounts SET balance = balance + ? WHERE name = ?"
SUB = "UPDATE accounts SET balance = balance - ? WHERE name = ?"


def transfer(src, dst, amount):
    try:
        with conn:
            conn.execute(ADD, (amount, dst))
            conn.execute(SUB, (amount, src))
    except sqlite3.IntegrityError as error:
        print("IntegrityError:", error)


transfer("ada", "alan", 30)
transfer("alan", "ada", 500)
print(conn.execute("SELECT * FROM accounts ORDER BY name").fetchall())
```

```text
IntegrityError: CHECK constraint failed: balance >= 0
[('ada', 70), ('alan', 50)]
```

- Para transferi iki güncellemedir: birine ekle, ötekinden düş. İkincisi
  başarısız olursa birincisi de geri alınmalı; yoksa para yoktan var olur.
- **`with conn:`** bloğu bir **işlemdir**: hata yoksa `commit`, hata varsa
  `rollback`. İkinci transferde `ada`'ya 500 eklendi, ama `alan`'dan düşmek
  `CHECK (balance >= 0)` kuralını bozdu; işlem geri alındı ve `ada` 70'te
  kaldı.
- **`CHECK`** gibi kısıtlar veriyi veritabanının kendisinde korur: hangi
  kod yazarsa yazsın eksi bakiye kaydedilemez.

## İndeks ve sorgu planı

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, user TEXT, kind TEXT)")
data = [(f"user{i % 5000}", "click" if i % 3 else "view") for i in range(200_000)]
conn.executemany("INSERT INTO events (user, kind) VALUES (?, ?)", data)
query = "SELECT COUNT(*) FROM events WHERE user = ?"
plan = conn.execute("EXPLAIN QUERY PLAN " + query, ("user42",)).fetchall()
print(plan[0][-1])
conn.execute("CREATE INDEX idx_events_user ON events (user)")
plan = conn.execute("EXPLAIN QUERY PLAN " + query, ("user42",)).fetchall()
print(plan[0][-1])
print(conn.execute(query, ("user42",)).fetchone()[0])
```

```text
SCAN events
SEARCH events USING COVERING INDEX idx_events_user (user=?)
40
```

- **`EXPLAIN QUERY PLAN`** veritabanının sorguyu **nasıl** çalıştıracağını
  söyler. İndeks yokken `SCAN`: 200 000 satırın hepsine bakılır.
- **`CREATE INDEX`** sütun için sıralı bir arama yapısı kurar; plan `SEARCH
  ... USING INDEX` oldu: doğrudan ilgili satırlara gidilir. Sık
  süzdüğün (`WHERE`) ve birleştirdiğin sütunlara indeks konur.
- İndeksin bedeli: ekleme ve güncellemede onun da güncellenmesi ve diskte
  yer. Her sütuna indeks konmaz.

## Tarihleri saklamak

```python
import sqlite3
from datetime import date

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (day TEXT, total REAL)")
conn.executemany("INSERT INTO orders VALUES (?, ?)",
                 [(date(2026, 3, d).isoformat(), d * 10.0) for d in (1, 2, 15)])
rows = conn.execute("SELECT day, total FROM orders WHERE day >= ? ORDER BY day",
                    ("2026-03-02",)).fetchall()
print(rows)
print([date.fromisoformat(day) for day, _ in rows][0].weekday())
monthly = "SELECT strftime('%m', day), SUM(total) FROM orders GROUP BY 1"
print(conn.execute(monthly).fetchall())
```

```text
[('2026-03-02', 20.0), ('2026-03-15', 150.0)]
0
[('03', 180.0)]
```

SQLite'ın ayrı bir tarih türü yok; tarih **ISO metni** (`2026-03-02`)
olarak saklanır. ISO biçimi metin olarak sıralanınca tarih sırasına girdiği
için `>=` ve `ORDER BY` doğru çalışır. Okurken `date.fromisoformat` ile geri
çevrilir; SQL içinde `strftime` ile ay, yıl çekilir.

## Sık hatalar

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (x INTEGER)")
cur = conn.execute("INSERT INTO t VALUES (?)", (5,))
print(cur.rowcount, cur.lastrowid)
try:
    conn.execute("INSERT INTO t VALUES (?)", 5)
except sqlite3.ProgrammingError as error:
    print(type(error).__name__)
print(conn.execute("SELECT * FROM t WHERE x = ?", (5,)).fetchall())
```

```text
1 1
ProgrammingError
[(5,)]
```

- Parametreler **dizi** olarak verilir: tek değer için `(5,)` (virgüllü
  demet) ya da `[5]`. Düz `5` `ProgrammingError` verir.
- `cursor.rowcount` etkilenen satır sayısı, `lastrowid` eklenen satırın
  kimliği: "kaç satır güncellendi", "yeni kaydın kimliği ne" soruları için.
- Unutulan `commit` ve kapatılmayan bağlantı: `with conn:` işlem için,
  `contextlib.closing` kapatmak için (contextlib bölümü).

## Özet

- `row_factory = sqlite3.Row` adla erişim; `executemany` toplu ekleme.
- Değerler her zaman `?` ya da `:ad` ile; f-string ile asla.
- `with conn:` işlem: başarıda `commit`, hatada `rollback`; `CHECK`,
  `UNIQUE`, `NOT NULL` kısıtları.
- `EXPLAIN QUERY PLAN` + `CREATE INDEX`: `SCAN` yerine `SEARCH`.
- Tarih ISO metni; `date.fromisoformat`, SQL'de `strftime`.

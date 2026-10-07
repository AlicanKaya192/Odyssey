# Veritabanı: SQLite

Şimdiye kadar kayıtlar bir sözlükte duruyordu. Sunucu kapanınca hepsi
gidiyor. Gerçek bir API veriyi **veritabanında** tutar. Bu bölümde Python'un
içinde gelen **SQLite** ile çalışıyorsun: kurulum yok, sunucu yok, veritabanı
tek bir dosya (`library.db`).

SQL patikasında `SELECT`, `INSERT`, `WHERE` yazmıştın; burada aynı komutları
Python'dan, `sqlite3` modülüyle gönderiyorsun.

## Tabloyu kurmak

```python
import sqlite3

DB_PATH = "library.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        year INTEGER NOT NULL)""")
    conn.commit()
    conn.close()


init_db()
```

- `sqlite3.connect(DB_PATH)`: dosyayı açar, yoksa oluşturur.
- `IF NOT EXISTS`: program her açıldığında çalışıyor; tablo varsa
  dokunmuyor.
- `id INTEGER PRIMARY KEY AUTOINCREMENT`: numarayı veritabanı veriyor.
  CRUD bölümündeki `next_id` sayacına artık gerek yok.
- `UNIQUE`: aynı başlık iki kez girilemez.

## İstek başına bağlantı: `yield`'li bağımlılık

Bağımlılıklar bölümünde "aç ve kapat" kalıbını görmüştün. İşte gerçek
kullanımı:

```python
from typing import Annotated
from fastapi import Depends


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


DB = Annotated[sqlite3.Connection, Depends(get_db)]
```

- Her istek kendi bağlantısını alıyor; cevaptan sonra kapanıyor.
- `row_factory = sqlite3.Row`: satırlar sütun adıyla okunabiliyor
  (`row["title"]`) ve `dict(row)` ile sözlüğe dönüyor.
- `check_same_thread=False`: FastAPI bağımlılığı ve uç noktayı farklı iş
  parçacıklarında çalıştırabilir; `sqlite3` varsayılan olarak bağlantının
  başka bir iş parçacığında kullanılmasını reddeder. Bizim ölçümümüzde hata
  çıkmadı, ama bağlantı istek başına açıldığı için bu ayar güvenli ve
  yaygın yol.

## Eklemek: `INSERT` + `commit`

```python
@app.post("/books", status_code=201)
def create_book(book: BookIn, db: DB):
    try:
        cur = db.execute("INSERT INTO books (title, year) VALUES (?, ?)",
                         (book.title, book.year))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Title already exists")
    return {"id": cur.lastrowid, **book.model_dump()}
```

- `?` yer tutucuları ve ayrı verilen değerler: **parametreli sorgu**.
  Aşağıda neden önemli olduğunu göreceksin.
- `cur.lastrowid`: veritabanının yeni satıra verdiği numara.
- `db.commit()`: değişikliği kalıcı yapıyor. **Unutursan** cevap `201`
  gidiyor ama veri kaydedilmiyor. Ölçtük: `commit`'siz eklenen kitaptan sonra
  `GET /books` → `[]`.
- `UNIQUE` bozulunca `sqlite3.IntegrityError`; onu `409`'a çeviriyoruz.

## Okumak

```python
@app.get("/books/{book_id}")
def read_book(book_id: int, db: DB):
    row = db.execute("SELECT id, title, year FROM books WHERE id = ?",
                     (book_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)
```

- `fetchone()`: tek satır ya da `None`. `fetchall()`: satır listesi.
- `(book_id,)`: tek değer bile olsa **demet** verilir; virgülü unutma.

## Silmek: kaç satır değişti?

```python
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: DB):
    cur = db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
```

`cur.rowcount` etkilenen satır sayısı. Önce `SELECT` yapıp sonra silmeye
gerek yok: hiçbir satır silinmediyse kayıt yoktu.

<figure class="fig">
  <div class="flow">
    <span class="node">İstek</span><span class="arrow">→</span>
    <span class="node acc">get_db()<br><small>connect</small></span><span class="arrow">→</span>
    <span class="node">Uç nokta<br><small>execute + commit</small></span><span class="arrow">→</span>
    <span class="node ok">Cevap</span><span class="arrow">→</span>
    <span class="node acc">finally<br><small>close</small></span>
  </div>
  <figcaption>Her istek kendi bağlantısını açıyor, işini yapıyor, cevap gittikten sonra bağlantı kapanıyor. Veri <code>library.db</code> dosyasında kalıyor.</figcaption>
</figure>

## Ölçtüğümüz akış

```text
POST /books  Dune 1965        201 {"id": 1, "title": "Dune", "year": 1965}
POST /books  Emma 1815        201 {"id": 2, ...}
POST /books  Dune 1965        409 {"detail": "Title already exists"}
GET /books?year=1815          200 [{"id": 2, "title": "Emma", "year": 1815}]
GET /books/9                  404
DELETE /books/1               204
DELETE /books/1               404
POST /books  Ubik 1969        201 {"id": 3, ...}
```

Silinen `1` numarası tekrar verilmedi: `AUTOINCREMENT` numarayı geri
kullanmıyor. Veri dosyada olduğu için sunucu yeniden başlasa da kitaplar
duruyor.

## SQL enjeksiyonu: neden `?`

Sorguyu metin birleştirerek kurmak cazip görünür:

```python
db.execute(f"SELECT id, title FROM books WHERE title = '{title}'")
```

`title=Dune` için doğru çalışıyor. Ama biri şunu gönderirse:

```text
GET /unsafe?title=x' OR '1'='1
200 [{"id": 1, "title": "Dune"}, {"id": 2, "title": "Emma"}]
```

Gelen metin sorgunun **parçası** oldu: `WHERE title = 'x' OR '1'='1'` her
satırı seçti (ölçtük). Aynı yolla tablo silinebilir. Buna **SQL enjeksiyonu**
denir.

`?` ile verilen değer ise her zaman **değer** olarak kalır, asla komut
olmaz. Kural kesin: **kullanıcıdan gelen hiçbir şeyi sorgu metnine
birleştirme.** `LIKE` aramasında bile:

```python
db.execute("SELECT title FROM books WHERE title LIKE ?", (f"%{q}%",))
```

`%` işaretleri değerin içinde, sorgunun değil.

## Özet

- `sqlite3` Python'un içinde; veritabanı tek dosya.
- Tablo program açılınca `CREATE TABLE IF NOT EXISTS`.
- İstek başına bağlantı: `yield`'li `get_db` + `row_factory = sqlite3.Row`.
- Değişiklikten sonra `commit()`; yoksa veri kaybolur.
- `lastrowid` yeni numara, `rowcount` etkilenen satır; `IntegrityError` →
  `409`.
- Değerler her zaman `?` ile: SQL enjeksiyonuna kapı açma.

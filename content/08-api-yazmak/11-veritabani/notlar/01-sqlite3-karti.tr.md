`sqlite3` modülünün API yazarken kullandığın parçaları; hepsi ölçüldü.

| Yazım | Ne yapar? |
|---|---|
| `conn = sqlite3.connect("library.db")` | Dosyayı açar (yoksa oluşturur) |
| `conn.row_factory = sqlite3.Row` | Satırlar `row["title"]` ve `dict(row)` olur |
| `cur = conn.execute(sql, (a, b))` | Tek komut, değerler `?` ile |
| `conn.executemany(sql, [(a, b), ...])` | Aynı komutu çok satırla |
| `cur.fetchone()` | Tek satır ya da `None` |
| `cur.fetchall()` | Satır listesi (boşsa `[]`) |
| `conn.commit()` | Değişiklikleri kalıcı yapar |
| `cur.lastrowid` | `INSERT`'te yeni satırın numarası |
| `cur.rowcount` | `UPDATE` / `DELETE`'te etkilenen satır |
| `conn.close()` | Bağlantıyı kapatır |

## `sqlite3.Row`

```python
row = conn.execute("SELECT * FROM books WHERE id = 1").fetchone()
row["title"]      # 'Dune'
row[1]            # 'Dune' (sırayla da olur)
row.keys()        # ['id', 'title', 'year']
dict(row)         # {'id': 1, 'title': 'Dune', 'year': 1966}
```

FastAPI `Row` nesnesini doğrudan JSON'a çeviremez; `dict(row)` döndür.

## Tek değer de demet

```python
conn.execute("SELECT * FROM books WHERE id = ?", (book_id,))   # doğru
conn.execute("SELECT * FROM books WHERE id = ?", (book_id))    # yanlış: demet değil
```

## Ya hepsi ya hiçbiri: `with conn:`

Birden fazla değişiklik birlikte yapılmalıysa:

```python
with conn:
    conn.execute("INSERT INTO books (title, year) VALUES (?, ?)", ("Emma", 1815))
    conn.execute("INSERT INTO books (title, year) VALUES (?, ?)", ("Dune", 1))
```

`with conn:` blok hatasız biterse `commit`, hata çıkarsa **geri alır**
(rollback). Ölçtük: ikinci satır `UNIQUE`'e takıldı ve `Emma` da
eklenmedi; tabloda yalnızca önceki `Dune` kaldı. Para aktarımı gibi "yarım
kalırsa felaket" işler böyle yazılır. (`with conn:` bağlantıyı
**kapatmaz**; o iş `get_db`'nin `finally`'sinde.)

## Kaç satır var?

```python
conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
```

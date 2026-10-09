Bağlam yöneticisinin en sık görüldüğü yerlerden biri **işlem** (transaction):
"bloktaki değişikliklerin hepsi ya birlikte kaydedilsin ya hiçbiri". Python'un
`sqlite3` bağlantısı bunu `with` ile yapıyor; ama bir tuzağı var.

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE t (x INTEGER)")
    with conn:
        conn.execute("INSERT INTO t VALUES (1)")
    try:
        with conn:
            conn.execute("INSERT INTO t VALUES (2)")
            raise ValueError("stop")
    except ValueError:
        pass
    print(conn.execute("SELECT x FROM t").fetchall())
try:
    conn.execute("SELECT 1")
except sqlite3.ProgrammingError as error:
    print("ProgrammingError:", error)
```

```text
[(1,)]
ProgrammingError: Cannot operate on a closed database.
```

- **`with conn:`** bir işlem bloğudur: blok normal biterse değişiklikler
  kaydedilir (`commit`), hata çıkarsa geri alınır (`rollback`). İkinci
  bloktaki `2` hata yüzünden geri alındı; tabloda yalnızca `1` var.
- **Tuzak:** `with conn:` bağlantıyı **kapatmaz**. Kapatmak için
  **`contextlib.closing`**: `close()` metodu olan herhangi bir nesneyi
  bağlam yöneticisine çevirir ve blok sonunda `close()` çağırır. Dıştaki
  blok bitince bağlantı kapandı; sonraki sorgu hata verdi.

## Kendi işlem desenin

Aynı fikir başka kaynaklara da uygulanır: blok başarılıysa kaydet, değilse
geri al.

```python
from contextlib import contextmanager


@contextmanager
def transaction(data):
    snapshot = dict(data)
    try:
        yield data
    except Exception:
        data.clear()
        data.update(snapshot)
        raise
```

Blokta hata çıkarsa sözlük, bloğa girmeden önceki kopyasına geri döner;
`raise` hatayı yine dışarı iletir (yutmaz). Birinci alıştırma bunun tam
sürümü.

# Genel Tekrar

Python Kütüphaneleri: İleri modülünün sonuna geldin. Artık bir programı
yalnızca çalışır değil, **büyüyebilir** yazmak için gereken araçları
biliyorsun: açık tipler ve kayıt sınıfları, kayıt (log) ve komut satırı,
veritabanı ve serileştirme, doğru para hesabı ve güvenlik, eşzamanlılık,
testler, ölçüm ve bellek. Bu bölüm yolu bir kez daha yürüyor; sonunda
araçların birlikte çalıştığı bir örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">Açık kod<br><small>00–05</small></span><span class="arrow">→</span>
    <span class="node">Programlar<br><small>06–09</small></span><span class="arrow">→</span>
    <span class="node">Hesap<br><small>10–11</small></span><span class="arrow">→</span>
    <span class="node">Eşzamanlılık<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Sağlamlık<br><small>14–16</small></span>
  </div>
  <figcaption>Modülün yolu: önce kodun kendisi, sonra programın dış dünyası, en sonda hız ve sağlamlık.</figcaption>
</figure>

## 1. Kodu açık yazmak (Bölüm 0–5)

| İş | Araç |
|---|---|
| Sonucu hatırlamak | `@lru_cache(maxsize=...)`, `@cache` |
| Argümanı sabitlemek | `functools.partial` |
| Süsleyici yazmak | iç fonksiyon + `@functools.wraps` |
| Sıralama anahtarı | `key=operator.itemgetter(...)`, `attrgetter`, çok anahtar için demet |
| En küçük / büyük N | `heapq.nsmallest`, `nlargest`; sıralı listeye ekleme `bisect.insort` |
| Tip belirtimi | `list[int]`, <code>X &#124; None</code>, `Literal`, `Callable`, `TypedDict` |
| Kayıt sınıfı | `@dataclass`, `field(default_factory=list)`, `frozen=True`, `asdict` |
| Ortak arayüz | `abc.ABC` + `@abstractmethod`; yapısal `typing.Protocol` |
| Kendi `with` bloğu | `@contextmanager` + `yield`; `closing`, `suppress`, `ExitStack` |

Değiştirilebilir varsayılan (`[]`) doğrudan yazılmaz; `lru_cache` argümanları
hashlenebilir olmalı; tip belirtimi çalışma anında denetlenmez.

## 2. Gerçek programlar (Bölüm 6–9)

| İş | Araç |
|---|---|
| Kayıt tutmak | `logging.getLogger(__name__)`, düzeyler, `basicConfig`, işleyici + biçim |
| Hatayla kayıt | `log.exception(...)` (yığın izi dahil) |
| Komut satırı | `argparse.ArgumentParser`, konumsal / seçenekli, `type=`, `choices=`, alt komutlar |
| Dosyada veritabanı | `sqlite3.connect`, `?` yer tutucu, `with conn:` işlem, `Row` |
| Hız için | `executemany`, `CREATE INDEX`, `EXPLAIN QUERY PLAN` |
| Python nesnesini saklamak | `pickle.dump` / `load` (`"wb"` / `"rb"`), `shelve` |

`print` yerine `logging`; SQL'e asla biçimlendirerek değer koyma;
güvenilmeyen pickle verisini asla yükleme.

## 3. Hesap ve güvenlik (Bölüm 10–11)

| İş | Araç |
|---|---|
| Para | `Decimal("19.99")`, `quantize(Decimal("0.01"), rounding=...)` |
| Tam kesir | `Fraction(1, 3)`, `limit_denominator` |
| Parmak izi | `hashlib.sha256(baytlar).hexdigest()`, `file_digest` |
| Şifre saklamak | tuz + `pbkdf2_hmac` / `scrypt`, `hmac.compare_digest` |
| İmza | `hmac.new(anahtar, mesaj, hashlib.sha256)` |
| Güvenli rastgele | `secrets.token_urlsafe`, `token_hex`, `choice` |

Decimal metinden kurulur ve float ile karışmaz; parayı bölerken kalan
kuruş dağıtılır; güvenlikte `random` değil `secrets`.

## 4. Eşzamanlılık (Bölüm 12–13)

| İş | Araç |
|---|---|
| Ağ / disk beklemeleri | `ThreadPoolExecutor` + `map` / `submit` |
| İşlemci yoğun iş | `ProcessPoolExecutor` + `if __name__ == "__main__":` |
| Paylaşılan veri | `threading.Lock`, `queue.Queue` |
| Çok sayıda ağ beklemesi | `asyncio`: `async def`, `await`, `gather`, `TaskGroup` |
| Süre sınırı, eşzamanlı sınır | `asyncio.timeout`, `Semaphore` |
| Async içinde engelleyen çağrı | `asyncio.to_thread` |

`future.result()` işteki hatayı yükseltir; `async def` içinde `time.sleep`
olay döngüsünü durdurur.

## 5. Sağlam kod (Bölüm 14–16)

| İş | Araç |
|---|---|
| Test | `unittest.TestCase`, `assertEqual`, `assertRaises`, `setUp`, `subTest` |
| Dış dünyayı sahtelemek | `unittest.mock.patch` |
| Belgedeki örnekler | `doctest` |
| Küçük parçayı ölçmek | `min(timeit.repeat(...))` |
| Zaman nereye gidiyor | `cProfile` + `pstats` |
| Bellek | `tracemalloc` (`take_snapshot`, `compare_to`), `weakref`, `gc` |

Önce ölç, sonra düzelt; testler kenar durumları kapsar; önbelleğe sınır,
dinleyiciye zayıf başvuru.

## Hepsi bir arada

Siparişleri SQLite'tan okuyan, dataclass'a çeviren, vergiyi `Decimal` ile
iş parçacığı havuzunda hesaplayan ve kayıt tutan küçük bir program.

```python
import io
import logging
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

stream = io.StringIO()
FORMAT = "%(levelname)s %(name)s %(message)s"
logging.basicConfig(stream=stream, level=logging.INFO, format=FORMAT)
log = logging.getLogger("shop")
CENT = Decimal("0.01")
SCHEMA = "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT, total TEXT)"


@dataclass(frozen=True)
class Order:
    id: int
    customer: str
    total: Decimal


def load(conn: sqlite3.Connection) -> list[Order]:
    rows = conn.execute("SELECT id, customer, total FROM orders ORDER BY id")
    return [Order(i, c, Decimal(t)) for i, c, t in rows]


def with_tax(order: Order) -> Decimal:
    return (order.total * Decimal("1.20")).quantize(CENT, rounding=ROUND_HALF_UP)


with closing(sqlite3.connect(":memory:")) as conn:
    with conn:
        conn.execute(SCHEMA)
        conn.executemany("INSERT INTO orders (customer, total) VALUES (?, ?)",
                         [("ada", "19.99"), ("alan", "5.01"), ("ada", "0.10")])
    orders = load(conn)
log.info("loaded %d orders", len(orders))
with ThreadPoolExecutor(max_workers=3) as pool:
    gross = list(pool.map(with_tax, orders))
print(orders[0])
print([str(g) for g in gross], sum(gross))
print(stream.getvalue().strip())
```

```text
Order(id=1, customer='ada', total=Decimal('19.99'))
['23.99', '6.01', '0.12'] 30.12
INFO shop loaded 3 orders
```

- **sqlite3:** tablo bir işlemde (`with conn:`) kuruluyor, değerler `?` ile
  giriyor, bağlantı `closing` ile kapanıyor (contextlib).
- **dataclasses + typing:** her satır değişmez (`frozen`) bir `Order`;
  fonksiyonlar tipleriyle belgelenmiş.
- **decimal:** tutar veritabanında metin, programda `Decimal`; vergi kuruşa
  "beş yukarı" ile yuvarlanıyor. Float hiç yok.
- **concurrent.futures:** her siparişin vergisi havuzda; sonuçlar sırayla.
- **logging:** program ne yaptığını `print` değil kayıtla söylüyor.

## Sık hatalar

| Hata | Doğrusu |
|---|---|
| `def f(items=[])` | `items=None` ya da `field(default_factory=list)` |
| `lru_cache(maxsize=None)` sınırsız veriyle | `maxsize` ver |
| Süsleyicide `wraps` unutmak | `@functools.wraps(func)` |
| `print` ile hata ayıklamak | `logging` |
| `f"... WHERE name = '{name}'"` | `?` yer tutucusu |
| İnternetten gelen pickle'ı yüklemek | JSON |
| `Decimal(0.1)` | `Decimal("0.1")` |
| Şifreyi `sha256` ile saklamak | tuz + `pbkdf2_hmac` |
| Güvenlik kodunu `random` ile üretmek | `secrets` |
| Paylaşılan sayacı kilitsiz artırmak | `with lock:` |
| `async def` içinde `time.sleep` | `await asyncio.sleep` / `to_thread` |
| Yalnızca "mutlu yol" testi | kenar durumlar |
| Ölçmeden hızlandırmak | `cProfile`, `timeit` |
| Sonsuza kadar büyüyen modül sözlüğü | sınır, `lru_cache(maxsize=...)` |

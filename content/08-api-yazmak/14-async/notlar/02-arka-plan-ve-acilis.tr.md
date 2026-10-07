Cevaptan sonra yapılan işler ve sunucu açılıp kapanırken çalışan kod.

## Birden fazla arka plan işi

```python
@app.post("/orders")
def place_order(tasks: BackgroundTasks):
    tasks.add_task(update_stock)
    tasks.add_task(send_receipt, "ada@x.org")
    return {"ok": True}
```

İşler **eklendiği sırayla**, cevaptan sonra çalışıyor (ölçtük:
`task1`, sonra `task2 hi`). `add_task(işlev, argümanlar...)`: argümanlar
işlevden sonra virgülle.

## Arka plan işi ne için değil?

- Mutlaka olması gereken işler (ödeme, kayıt): sunucu o sırada kapanırsa iş
  yarıda kalır ve kimse bilmez.
- Dakikalar süren işler: aynı sunucunun kaynaklarını yer. Bunlar için ayrı
  iş kuyruğu sistemleri (Celery, RQ) kullanılır.

## Açılışta ve kapanışta: `lifespan`

Modeli belleğe yüklemek, veritabanı bağlantı havuzunu kurmak gibi işler
**her istekte değil, bir kez** yapılmalı:

```python
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    events.append("startup")     # sunucu açılırken
    yield
    events.append("shutdown")    # sunucu kapanırken


app = FastAPI(lifespan=lifespan)
```

Ölçtük: `TestClient` ile `with` bloğuna girince `startup`, çıkınca
`shutdown` yazıldı. Bir ML modelini sunarken modeli tam buraya yükleyeceksin
(Model Sunmak bölümü).

`yield`'li bağımlılıktan farkı:

| | `yield`'li bağımlılık | `lifespan` |
|---|---|---|
| Ne zaman? | Her istekte | Sunucu başına bir kez |
| Örnek | Veritabanı bağlantısı | Model yükleme |

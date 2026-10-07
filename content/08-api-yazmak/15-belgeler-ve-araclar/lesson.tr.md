# Belgeler ve Araçlar

API'yi başkaları kullanacak: bir mobil uygulama, bir web sayfası, başka bir
ekip. Onların API'ni **kodunu okumadan** anlayabilmesi gerekiyor. FastAPI
belgeyi koddan kendisi üretiyor; bu bölümde o belgeyi zenginleştiriyor ve
API'yi dış dünyaya hazırlayan birkaç aracı (CORS, ara katman) görüyorsun.

## Belge nereden geliyor?

Yazdığın her uç nokta, model ve kural **OpenAPI** adlı standart bir
belgeye çevriliyor. Üç adreste duruyor (ölçtük, üçü de `200`):

| Adres | Ne? |
|---|---|
| `/openapi.json` | Belgenin kendisi: makinenin okuyacağı JSON |
| `/docs` | Swagger UI: dene düğmeli sayfa |
| `/redoc` | ReDoc: okumak için düzenli sayfa |

`/openapi.json` bir standart olduğu için başka araçlar da okuyabiliyor:
istemci kodu üreten araçlar, test araçları, API kataloglar.

## Uygulamanın kimliği

```python
app = FastAPI(
    title="Library API",
    version="1.2.0",
    description="Books and authors of a small library.",
)
```

`/openapi.json`'da:

```text
"openapi": "3.1.0"
"info": {"title": "Library API", "description": "Books and authors of a small library.",
         "version": "1.2.0"}
```

`/docs` sayfasının başlığında da bunlar görünüyor. `version` senin API'nin
sürümü; değişiklik yaptıkça artırırsın.

## Uç noktayı anlatmak

```python
@app.get("/books/{book_id}", tags=["books"], summary="Read one book",
         responses={404: {"description": "No book with this id"}})
def read_book(book_id: int):
    """Returns the book with the given id.

    The id is the number given when the book was added.
    """
    ...
```

| Yazım | Belgede |
|---|---|
| `tags=["books"]` | "books" başlığı altında |
| `summary="..."` | Uç noktanın kısa adı |
| İşlevin docstring'i | Uzun açıklama (ölçtük: olduğu gibi `description` oldu) |
| `responses={404: {...}}` | Olası hata cevapları listesine `404` eklendi |

`summary` yazılmazsa FastAPI işlevin adından üretiyor: `add_book` →
`"Add Book"`. Fena değil ama "Read one book" daha açık.

`responses` olmadan belgede yalnızca `200` ve FastAPI'nin kendi `422`'si
görünüyor; senin `HTTPException(404)`'ün görünmüyor, çünkü FastAPI kodunu
çalıştırmadan onu bilemez. Ölçtük: `responses` ile liste `200, 404, 422`.

<figure class="fig">
  <div class="flow">
    <span class="node">Kod<br><small>tags, summary, docstring, modeller</small></span><span class="arrow">→</span>
    <span class="node acc">/openapi.json</span><span class="arrow">→</span>
    <span class="node ok">/docs · /redoc<br><small>istemci üreticileri</small></span>
  </div>
  <figcaption>Belgeyi ayrıca yazmıyorsun: koda eklediğin her bilgi standart bir belgeye dönüşüyor, sayfalar ve araçlar onu okuyor.</figcaption>
</figure>

## Modele örnek

```python
class Book(BaseModel):
    title: str = Field(examples=["Dune"])
    year: int = Field(examples=[1965], description="Year of first publication")
```

`/docs`'taki "dene" düğmesi gövdeyi `"string"` ve `0` yerine `"Dune"` ve
`1965` ile dolduruyor; açıklama alanın yanında yazıyor.

## Eskiyen ve gizlenen uç noktalar

```python
@app.get("/old-books", deprecated=True)
def old_books():
    ...


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
```

- `deprecated=True`: uç nokta çalışıyor ama belgede **üstü çizili**
  görünüyor; "bunu kullanma, yakında kalkacak" demek.
- `include_in_schema=False`: uç nokta çalışıyor (`/health` → `200`) ama
  belgede hiç yok. Sunucuyu izleyen araçların kullandığı iç adresler için.

## Tarayıcıdan çağrılınca: CORS

Bir web sayfası (`https://library.example.com`) senin API'ne
(`https://api.example.com`) tarayıcıdan istek atınca tarayıcı önce sorar:
"bu API başka bir siteden çağrılmaya izin veriyor mu?" İzin, cevaptaki
`Access-Control-Allow-Origin` başlığıyla verilir. Buna **CORS** denir.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://library.example.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

Ölçtük:

```text
GET, Origin: https://library.example.com
    200  access-control-allow-origin: https://library.example.com
GET, Origin: https://evil.example.com
    200  (izin başlığı yok)
OPTIONS ön sorusu, library.example.com
    200  access-control-allow-methods: GET, POST
OPTIONS ön sorusu, evil.example.com
    400  Disallowed CORS origin
```

İkinci satıra dikkat: istek **yine `200`** döndü. CORS sunucuyu korumuyor;
tarayıcıya "bu cevabı o sayfaya gösterme" diyor. `requests` ya da `curl`
CORS'a hiç bakmaz. Gerçek koruma kimlik doğrulama bölümündekiler.

`allow_origins=["*"]` herkese izin verir; kimlik bilgisi taşıyan API'lerde
kullanma, izin verdiğin siteleri tek tek yaz.

## Her isteğe dokunmak: ara katman

Ara katman (middleware) **her** isteğin önünde ve arkasında çalışan kod:

```python
import time
from fastapi import Request


@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response
```

`call_next(request)` isteği uç noktaya iletiyor ve cevabı getiriyor; öncesi
ve sonrası senin. Ölçtük: cevapta `x-process-time: 0.0013`. Günlük yazmak,
süre ölçmek, her cevaba ortak bir başlık eklemek için kullanılır.

## Sunucuyu çalıştırmak

Odyssey'de **Sunucuyu başlat** düğmesi bunu senin yerine yapıyor. Kendi
bilgisayarında:

```text
uvicorn main:app --reload
```

`main:app`: `main.py` dosyasındaki `app` değişkeni. `--reload`: kodu
kaydettikçe sunucu yeniden başlar; yalnızca geliştirirken. Varsayılan
adres `http://127.0.0.1:8000`; belge `http://127.0.0.1:8000/docs`.

## Özet

- Belge koddan üretilir: `/openapi.json`, `/docs`, `/redoc`.
- `FastAPI(title=, version=, description=)`; uç noktada `tags`, `summary`,
  docstring, `responses`.
- `Field(examples=[...], description=...)` dene düğmesini doldurur.
- `deprecated=True` üstü çizili, `include_in_schema=False` gizli.
- CORS tarayıcı içindir, sunucuyu korumaz; izinli siteleri tek tek yaz.
- `@app.middleware("http")`: her isteğin önünde ve arkasında çalışır.

# Hata Yanıtları

İyi bir API yalnızca işler yolunda giderken değil, **gitmediğinde** de
açık konuşur. İstemcinin yazdığı kod hata cevabını okuyup karar verecek:
yeniden mi denesin, kullanıcıya ne desin, hangi alanı işaretlesin. Bu
bölümde hata cevaplarını sen tasarlıyorsun.

## FastAPI'nin kendi hataları

Hiçbir şey yazmadan bile FastAPI bazı hataları kendisi veriyor (ölçtük):

```text
GET /nothing          404 {"detail": "Not Found"}            adres yok
DELETE /items/pen     405 {"detail": "Method Not Allowed"}   yöntem yok
GET /n?x=abc          422 {"detail": [{"type": "int_parsing", ...}]}
GET /boom             500 Internal Server Error             kodunda hata
```

Hepsinde gövde `detail` anahtarıyla geliyor; `500` hariç: o düz metin.

## `HTTPException`

Kendi hatanı göndermek için:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()
stock = {"pen": 3, "book": 0}


@app.get("/items/{name}")
def read_item(name: str):
    if name not in stock:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": name, "stock": stock[name]}
```

- `raise`: `return` değil. İşlev o satırda durur.
- `detail` cevaptaki `{"detail": ...}` olur.

`detail` metin olmak zorunda değil; sözlük de olur ve istemci için daha
kullanışlıdır:

```python
raise HTTPException(status_code=409, detail={"code": "out_of_stock", "item": name})
```

```text
409 {"detail": {"code": "out_of_stock", "item": "pen"}}
```

Metin mesajı insan okur; `"code"` gibi sabit bir alanı **program** okur.
İstemci `if body["detail"]["code"] == "out_of_stock":` yazabilir; mesajın
cümlesi değişse de kodu bozulmaz.

Başlık da eklenebilir:

```python
raise HTTPException(status_code=401, detail="Missing key",
                    headers={"WWW-Authenticate": "Bearer"})
```

## Derindeki hata: kendi istisna sınıfın

Hatanın oluştuğu yer çoğu zaman uç noktanın kendisi değil, onun çağırdığı
bir işlev olur. O işlevin HTTP bilmesi gerekmez:

```python
class OutOfStock(Exception):
    def __init__(self, item: str):
        self.item = item


def take(item: str):
    if stock[item] == 0:
        raise OutOfStock(item)
    stock[item] -= 1
```

`take` sıradan bir Python işlevi; başka bir programda da kullanılabilir.
Bu istisnayı HTTP cevabına **bir kez** çeviren bir yakalayıcı yazarsın:

```python
from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(OutOfStock)
def out_of_stock_handler(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=409,
                        content={"error": "out_of_stock", "item": exc.item})


@app.post("/buy/{item}")
def buy(item: str):
    take(item)
    return {"item": item, "left": stock[item]}
```

```text
POST /buy/pen    200 {"item": "pen", "left": 2}
POST /buy/book   409 {"error": "out_of_stock", "item": "book"}
```

`OutOfStock` hangi uç noktadan, ne kadar derinden fırlatılırsa fırlatılsın
aynı cevaba dönüşüyor.

<figure class="fig">
  <div class="flow">
    <span class="node">buy()</span><span class="arrow">→</span>
    <span class="node no">take()<br><small>raise OutOfStock</small></span><span class="arrow">→</span>
    <span class="node acc">exception_handler</span><span class="arrow">→</span>
    <span class="node ok">409 JSON</span>
  </div>
  <figcaption>İstisna derindeki işlevden yukarı çıkıyor; yakalayıcı onu tek yerde HTTP cevabına çeviriyor.</figcaption>
</figure>

## 422'nin biçimini değiştirmek

FastAPI'nin doğrulama hatası da bir istisna: `RequestValidationError`. Onu
da yakalayıp kendi biçimine çevirebilirsin:

```python
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
def validation_handler(request: Request, exc: RequestValidationError):
    fields = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422,
                        content={"error": "invalid_input", "fields": fields})
```

```text
GET /n?x=abc   422 {"error": "invalid_input", "fields": ["x"]}
```

`exc.errors()` bildiğin `detail` listesi; `loc[1:]` ilk öğeyi (`query`,
`body`) atıp alan adını bırakıyor. Bunu yaparsan bütün API'de aynı biçimi
kullan: istemci her uç noktada hatayı aynı yerden okumalı.

## Beklenmeyen hatalar

`1 / 0` gibi yakalanmamış bir hata `500 Internal Server Error` düz metni
döndürüyor. Bunu da JSON'a çeviren bir yakalayıcı yazılabilir:

```python
@app.exception_handler(Exception)
def unexpected(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal"})
```

```text
GET /boom   500 {"error": "internal"}
```

Bir fark var: bu yakalayıcı cevabı gönderse de hata **yine** sunucu
günlüğüne yazılıyor ve testte istisna olarak yükseliyor (ölçtük). Bu
iyi bir şey: `500` bir hatadır ve görülmesi gerekir. **Hatanın ayrıntısını
istemciye gönderme**; `str(exc)` kodunun içini (dosya yolları, sorgular)
dışarı sızdırır.

## Özet

- `raise HTTPException(status_code=..., detail=..., headers=...)`.
- `detail` sözlük olabilir; programın okuyacağı sabit bir `code` koy.
- Kendi istisna sınıfın + `@app.exception_handler(Sınıf)`: hata derinde,
  çeviri tek yerde.
- `RequestValidationError` yakalanarak `422`'nin biçimi değiştirilebilir.
- Beklenmeyen hatada istemciye ayrıntı verme; ayrıntı günlükte kalır.

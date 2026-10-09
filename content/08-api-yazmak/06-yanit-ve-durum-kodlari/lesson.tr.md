# Yanıt Modelleri ve Durum Kodları

Şimdiye kadar **gelen** veriye kalıp koydun. Bu bölüm öbür yön: **giden**
cevap. İki soru var: cevapta hangi alanlar olacak (yanıt modeli) ve
cevabın durum kodu ne olacak.

## Sorun: içerideki her şey dışarı çıkmamalı

Kullanıcı kaydı tutan bir API düşün. Kayıtta şifre de var:

```python
users[1] = {"id": 1, "name": "Ada", "password": "secret"}
```

`return users[1]` yazarsan şifre de cevaba gider. Her uç noktada elle
alan silmek unutulmaya açık. Çözüm: cevabın kalıbını da bir modelle
tarif etmek.

## Yanıt modeli

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = {}


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str


@app.post("/users", status_code=201, response_model=UserOut)
def create_user(user: UserIn):
    new_id = len(users) + 1
    users[new_id] = {"id": new_id, **user.model_dump()}
    return users[new_id]
```

İşlev şifreli sözlüğü döndürüyor, ama cevap:

```text
POST /users  {"name": "Ada", "password": "secret"}
201          {"id": 1, "name": "Ada"}
```

`response_model=UserOut`: FastAPI dönen değeri bu modelden geçiriyor;
modelde olmayan alanlar (`password`) **atılıyor**. Girdi ve çıktı için iki
ayrı model yazmak (`UserIn` / `UserOut`) bu yüzden yaygın.

<figure class="fig">
  <div class="flow">
    <span class="node">Gelen gövde<br><small>name, password</small></span><span class="arrow">→</span>
    <span class="node acc">UserIn</span><span class="arrow">→</span>
    <span class="node">İşlevin<br><small>kayıt: id, name, password</small></span><span class="arrow">→</span>
    <span class="node acc">UserOut</span><span class="arrow">→</span>
    <span class="node ok">Cevap<br><small>id, name</small></span>
  </div>
  <figcaption>Girdi modeli gelen gövdeyi, yanıt modeli giden cevabı süzüyor. Şifre kayıtta duruyor ama <code>UserOut</code>'ta olmadığı için dışarı çıkmıyor.</figcaption>
</figure>

## Dönüş tipi de olur

Aynı şey işlevin dönüş tipiyle de yazılabiliyor:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int) -> UserOut:
    return users[user_id]
```

`-> UserOut` → cevap `{"id": 1, "name": "Ada"}`. Fazladan alanlar burada da
atılıyor (ölçtük: `password` ve `admin` içeren sözlük döndürdük, ikisi de
gitmedi). Liste için `-> list[UserOut]` ya da
`response_model=list[UserOut]`.

## Yanıt modeli seni de denetler

Döndürdüğün değer modele **uymazsa** hata istemcinin değil senin:

```python
@app.get("/bad", response_model=UserOut)
def bad():
    return {"name": "Ada"}          # id yok
```

```text
GET /bad   500 Internal Server Error
```

Sunucunun günlüğünde sebep yazıyor:

```text
ResponseValidationError: 1 validation error:
  {'type': 'missing', 'loc': ('response', 'id'), 'msg': 'Field required', ...}
```

`loc` bu kez `response` ile başlıyor. İstemci yanlış bir şey göndermedi;
`500` "sunucuda bir hata var" demek.

## Durum kodları

Cevabın ilk satırı, istemcinin gövdeyi okumadan sonucu anlamasını sağlar.
API Kullanmak modülünde okuduğun kodlar burada **senin seçimin**:

| Durum | Ne zaman? |
|---|---|
| `200 OK` | Varsayılan; okuma, güncelleme |
| `201 Created` | Yeni kayıt oluşturuldu (`POST`) |
| `204 No Content` | Başarılı ama gönderilecek gövde yok (`DELETE`) |
| `400 Bad Request` | İstek kurallara uygun ama işlenemiyor |
| `404 Not Found` | Kayıt yok |
| `409 Conflict` | Çakışma: aynı ad zaten var |
| `422 Unprocessable Content` | Doğrulama düştü (FastAPI kendisi) |

Kodun sayısını ezberlemek zorunda değilsin; `status` modülünde adlarıyla
duruyorlar:

```python
from fastapi import status


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    users.pop(user_id, None)
```

```text
DELETE /users/1   204   (gövde yok)
```

`204`'te gövde gönderilmez: işlev bir şey döndürse bile cevap boş gitti
(ölçtük).

## Koda o anda karar vermek

`status_code=201` dekoratörde sabittir. Bazen kod duruma göre değişir;
o zaman `JSONResponse` döndürürsün:

```python
from fastapi.responses import JSONResponse


@app.post("/jobs")
def start_job():
    return JSONResponse(status_code=202, content={"queued": True})
```

`JSONResponse` **olduğu gibi** gider: `response_model` ondan geçmez.
Hata durumları için bir sonraki adım `HTTPException` (Hata Yanıtları
bölümü).

## Başlık eklemek

Yeni kaydın adresini `Location` başlığında vermek iyi bir alışkanlık.
Parametre olarak `Response` iste, başlığı ona yaz:

```python
from fastapi import Response


@app.post("/users", status_code=201)
def create_user(user: UserIn, response: Response):
    ...
    response.headers["Location"] = f"/users/{new_id}"
    return {...}
```

```text
201   location: /users/7
```

## `null` alanları atlamak

```python
@app.get("/book", response_model=Book, response_model_exclude_none=True)
def book():
    return {"title": "Dune", "note": None}
```

Cevap `{"title": "Dune"}`: değeri `None` olan `note` hiç yazılmadı.

## Özet

- `response_model=Model` ya da `-> Model`: cevabın kalıbı; fazladan alanlar
  atılır, eksik alan `500` (`ResponseValidationError`).
- Girdi ve çıktı için ayrı modeller: `UserIn` (şifreli), `UserOut`
  (şifresiz).
- `status_code=` dekoratörde; adlarıyla `status.HTTP_201_CREATED`.
- `204` gövdesiz; anlık karar için `JSONResponse(status_code=...)`.
- Başlık için `response: Response` parametresi.

Aynı kaynağın birkaç modeli olur. Alanları tekrar yazmamak için ortak bir
taban modelden türetilir.

```python
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserIn(UserBase):      # istemcinin gönderdiği
    password: str


class UserOut(UserBase):     # istemciye giden
    id: int
```

- `UserIn`: `name`, `email`, `password`. `POST` gövdesi.
- `UserOut`: `name`, `email`, `id`. Cevap; şifre hiç yok.

Ölçtük: `UserIn` alıp `-> UserOut` döndüren uç nokta
`{"name": "Ada", "email": "a@x.org", "id": 1}` verdi. Alan sırası: önce
taban modelinkiler, sonra eklenenler. Şifresiz gövde `422`
(`loc: ["body", "password"]`).

## Adlandırma

| Model | Ne için? |
|---|---|
| `XBase` | Ortak alanlar; doğrudan kullanılmaz |
| `XIn` / `XCreate` | Oluştururken gelen gövde |
| `XUpdate` | Güncellerken gelen gövde (alanlar çoğu zaman isteğe bağlı) |
| `XOut` / `X` | Cevap |

## `/docs`'ta

Yanıt modeli belgeye de giriyor: `GET /users/{user_id}` açıldığında
"Responses" altında `UserOut` şeması görünüyor. `-> UserOut` yazılan işlevin
OpenAPI kaydında yanıt şeması `#/components/schemas/UserOut` (ölçtük).
Yani istemciyi yazan kişi cevabın şeklini kodu okumadan biliyor.

## Ne zaman `response_model`, ne zaman `-> Model`?

İkisi aynı işi yapar. `-> Model` daha kısa ve editör de anlıyor.
`response_model=` şu durumlarda gerekir:

- İşlev bir sözlük döndürüyor ve editör "bu sözlük `UserOut` değil" diye
  uyarıyor.
- `response_model_exclude_none=True` gibi ek ayarlar yazacaksın.

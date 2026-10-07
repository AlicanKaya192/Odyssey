Sunucu gönderdiğin veriyi reddettiğinde hatayı okumak ve düzeltmek.

## Alıştırma sunucusunun kuralları

| Alan | Kural | Bozulunca `detail` |
|---|---|---|
| `title` | Boş olmayan metin | `title must be a non-empty string` |
| `price` | Pozitif sayı | `price must be a positive number` |
| `author_id` | Var olan bir yazar | `author_id does not exist` |
| gövde | JSON nesnesi | `the body must be a JSON object` |

`POST` ve `PUT`'ta `title` ve `price` zorunlu; `PATCH`'te yalnızca
gönderdiğin alanlar denetleniyor.

## Hata yanıtını kullanmak

```python
r = requests.post(BASE + "/books", json=new, headers=AUTH)
if r.status_code == 422:
    print("rejected:", r.json()["detail"])
elif r.status_code == 201:
    print("created:", r.headers["Location"])
else:
    print("unexpected:", r.status_code)
```

## Göndermeden önce denetlemek

Sunucuya gitmeden yakalanabilecek hataları istemcide de denetlemek iyi bir
alışkanlık; hem istek sayısını azaltır hem de kullanıcıya daha erken haber
verir:

```python
def problems(book):
    found = []
    if not str(book.get("title", "")).strip():
        found.append("title is empty")
    if not isinstance(book.get("price"), (int, float)) or book["price"] <= 0:
        found.append("price must be positive")
    return found
```

Ama son söz her zaman sunucunun: istemcideki denetim sunucunun denetiminin
**yerine geçmez**, yalnızca önüne geçer.

## Sık hatalar

- Fiyatı metin göndermek: `{"price": "11.50"}` → sayı değil, reddedilir.
- `data=` kullanmak: gövde JSON değil, form olarak gider.
- Liste adresine `PATCH` göndermek (`/books`): `405`; tek kaydın adresi
  gerekir (`/books/2`).

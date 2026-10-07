Bir API'nin bütün hata cevapları **aynı şekilde** olmalı. İstemciyi yazan
kişi hatayı her uç noktada aynı yerden okuyabilmeli.

## İyi bir hata gövdesi

```json
{"detail": {"code": "out_of_stock", "message": "Book is out of stock", "item": "book"}}
```

| Alan | Kim okur? | Ne işe yarar? |
|---|---|---|
| `code` | Program | Sabit, kısa, İngilizce: `out_of_stock`, `name_taken` |
| `message` | İnsan | Açıklama; değişebilir |
| Ek alanlar | İkisi | Hangi kayıt, hangi alan: `item`, `field` |

Mesajın cümlesi bir gün değişir; `code` hiç değişmez. İstemcinin kodu
`code`'a bakarak karar vermeli.

## Kaçınılacaklar

- **Aynı durum için farklı kodlar:** bir yerde `404`, başka yerde `400`
  "bulunamadı".
- **Hata için `200`:** `200 {"error": "not found"}` istemciyi yanıltır;
  çoğu istemci önce durum koduna bakar.
- **İçeriği sızdırmak:** `detail=str(exc)` veritabanı sorgusunu, dosya
  yolunu ya da kullanıcı verisini dışarı yollayabilir.
- **İnsanın okuyacağı metne göre karar vermek** (istemci tarafında): mesaj
  değiştiği gün kod bozulur.

## `HTTPException` mı, kendi istisnan mı?

| Durum | Tercih |
|---|---|
| Uç noktanın kendi içinde basit bir `404` | `HTTPException` |
| Hata bir yardımcıda, iş mantığında | Kendi istisna sınıfın + yakalayıcı |
| Aynı hata birçok uç noktada | Kendi istisna sınıfın + yakalayıcı |

Kendi istisna sınıfı iş mantığını HTTP'den ayırır: `take()` işlevi
yarın bir komut satırı aracında da kullanılabilir.

## Yakalayıcının imzası

```python
@app.exception_handler(OutOfStock)
def handler(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=..., content={...})
```

İki parametre (istek ve istisna) ve bir `JSONResponse`. İstisna nesnesinin
alanlarına (`exc.item`) buradan ulaşırsın.

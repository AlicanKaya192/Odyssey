Beş yöntem, dekoratörleri ve her birinin tekrar edilince ne olduğu.

| Yöntem | Dekoratör | Değiştirir mi? | İki kez gönderilince |
|---|---|---|---|
| `GET` | `@app.get` | Hayır | Aynı cevap (güvenli) |
| `POST` | `@app.post` | Evet | İki kayıt oluşabilir |
| `PUT` | `@app.put` | Evet | Sonuç aynı (kaydın tamamı yine aynı değer) |
| `PATCH` | `@app.patch` | Evet | Çoğu zaman aynı |
| `DELETE` | `@app.delete` | Evet | İlki siler, ikincisi `404` |

"İki kez gönderilince sonuç aynı" olan yöntemlere **idempotent** denir
(`GET`, `PUT`, `DELETE`). API Kullanmak modülündeki yeniden deneme kuralı buradan
geliyor: istemci bir isteği tekrar gönderebilir; `POST`'u tekrar etmek
tehlikeli, ötekiler değil.

## Kalıp

```python
@app.get("/items")
def list_items():
    ...


@app.post("/items")
def create_item():
    ...
```

- Bir adres + bir yöntem = bir işlev.
- İşlev adları belgede özet olur (`list_items` → "List Items").
- Aynı adres ve yöntem iki kez yazılırsa **ilki** kazanır; ikincisi hiç
  çağrılmaz. Kopyala-yapıştır sonrası buna dikkat.

## Hangi kod ne zaman (FastAPI kendiliğinden)

| Durum | Kod |
|---|---|
| Uç nokta çalıştı | `200` |
| Adres yok | `404` |
| Adres var, yöntem yok | `405` |
| Sonda `/` fazla | `307` → doğru adrese |
| İşlevin içinde hata | `500` |

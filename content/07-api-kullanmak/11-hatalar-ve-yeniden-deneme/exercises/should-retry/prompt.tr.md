Yeniden deneme kararını bir fonksiyonda topla. Burada istek yok; yalnızca
bölümün karar tablosu.

**Yapman gerekenler:** `should_retry(method, outcome)` fonksiyonunu yaz.
`outcome` ya bir durum kodu (int) ya da `"timeout"` / `"connection"` metni.

- Yöntem tekrarlanabilir değilse (`POST`, `PATCH`) → `False`.
- `outcome` `"timeout"` ya da `"connection"` ise → `True`.
- Kod `429` ya da `500` ve üstüyse → `True`.
- Diğer her şey → `False`.

Yöntem küçük harfle de gelebilir. Sonra `cases` listesindeki her durum için
yöntemi, sonucu ve kararı yazdır.

**Beklenen çıktı:**

```
GET 503 -> True
GET 404 -> False
get timeout -> True
POST 503 -> False
DELETE connection -> True
PUT 429 -> True
GET 200 -> False
patch 500 -> False
```

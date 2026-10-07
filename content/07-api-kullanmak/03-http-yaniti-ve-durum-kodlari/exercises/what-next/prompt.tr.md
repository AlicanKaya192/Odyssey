Durum kodu yalnızca ne olduğunu değil, **ne yapılacağını** da söylüyor. Bu
kararı veren küçük bir fonksiyon yazacaksın; Bölüm 11'deki hata yönetimi
bunun üstüne kurulacak.

**Yapman gerekenler:** `next_step(code)` fonksiyonunu yaz. Şu sırayla karar
versin:

| Kod | Döndür |
|---|---|
| 2xx | `"use the body"` |
| 3xx | `"follow Location"` |
| 401 ya da 403 | `"check your key"` |
| 404 | `"check the address"` |
| 429 | `"wait, then retry"` |
| diğer 4xx | `"fix the request"` |
| 5xx | `"retry later"` |

Sonra `codes` listesindeki her kod için kodu ve kararı yazdır.

**Beklenen çıktı:**

```
200 -> use the body
201 -> use the body
301 -> follow Location
401 -> check your key
403 -> check your key
404 -> check the address
422 -> fix the request
429 -> wait, then retry
500 -> retry later
503 -> retry later
```

Özel durumları (401, 404, 429) genel 4xx kuralından **önce** denetle; yoksa
hepsi `"fix the request"` olur.

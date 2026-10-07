Bölüm 03, 06 ve 11'in tekrarı: bir adrese istek atıp ne olduğunu tek kelimeyle
söyleyen bir fonksiyon.

**Yapman gerekenler:** `diagnose(path)` fonksiyonunu yaz. `timeout=1` ile
istek göndersin ve şunlardan birini döndürsün:

| Durum | Döndür |
|---|---|
| `requests.Timeout` | `"too slow"` |
| `2xx` | `"ok"` |
| `401` ya da `403` | `"need permission"` |
| `404` | `"not found"` |
| `5xx` | `"server error"` |
| diğerleri | `"other"` |

Sonra `paths` listesindeki her adres için adresi ve teşhisi yazdır.

**Beklenen çıktı:**

```
/books/1 -> ok
/books/0 -> not found
/stats -> need permission
/broken -> server error
/slow -> too slow
/me -> need permission
```

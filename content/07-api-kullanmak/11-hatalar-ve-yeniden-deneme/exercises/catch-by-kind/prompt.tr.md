Dört adresin her biri başka bir şekilde sonuçlanıyor. Hepsini tek bir
fonksiyonla, türüne göre ayırarak karşıla.

**Yapman gerekenler:**

1. `fetch(url)` fonksiyonunu yaz. `requests.get(url, timeout=1)` ve
   ardından `raise_for_status()` çağırsın, şunlardan birini döndürsün:
   - sorun yoksa `"ok 200"` (gerçek kodla),
   - `requests.Timeout` → `"timeout"`,
   - `requests.ConnectionError` → `"no connection"`,
   - `requests.HTTPError` → `"http error 404"` (gerçek kodla).
2. `urls` listesindeki her adres için sonucu yazdır.

`except` bloklarını özelden genele yaz.

**Beklenen çıktı:**

```
ok 200
http error 404
timeout
no connection
```

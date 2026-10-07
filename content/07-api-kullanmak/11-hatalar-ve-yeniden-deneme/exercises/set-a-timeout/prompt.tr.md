`/slow` 3 saniye sonra cevap veriyor. Önce sabırsız, sonra sabırlı bir istek
göndereceksin.

**Yapman gerekenler:**

1. `timeout=1` ile `/slow`'a istek gönder; `requests.Timeout` gelirse
   `too slow: gave up after 1 second` yazdır.
2. `timeout=5` ile tekrar gönder; durum kodunu ve gövdedeki `ok` değerini
   yazdır.

**Beklenen çıktı:**

```
too slow: gave up after 1 second
status: 200
ok: True
```

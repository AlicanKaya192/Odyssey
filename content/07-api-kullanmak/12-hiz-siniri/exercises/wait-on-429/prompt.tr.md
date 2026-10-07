`/limited`'den 6 başarılı yanıt toplaman gerekiyor. 429 gelirse `Retry-After`
kadar bekleyip aynı isteği yeniden gönder.

**Yapman gerekenler:**

1. Başarılı yanıt sayısı 6 olana kadar istek gönder.
2. `429` gelirse `int(r.headers["Retry-After"])` saniye bekle ve `waited`
   yazdır; başarılıysa sayacı artır.
3. Sonda başarılı yanıt sayısını ve toplam istek sayısını yazdır.

**Beklenen çıktı:**

```
waited
successful: 6
requests: 7
```

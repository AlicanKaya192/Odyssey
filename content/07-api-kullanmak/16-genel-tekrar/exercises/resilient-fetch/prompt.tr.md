Bölüm 11 ve 12'nin tekrarı: hem meşgul sunucuya hem hız sınırına dayanıklı bir
istek fonksiyonu.

**Yapman gerekenler:**

1. `get(path)` fonksiyonunu yaz: en fazla 5 deneme yapsın;
   - `429` gelirse `Retry-After` kadar beklesin,
   - `5xx` gelirse 1 saniye beklesin,
   - başka bir kod gelirse yanıtı döndürsün;
   - denemeler biterse `None` döndürsün.
2. `/flaky`'yi bir kez, `/limited`'i art arda 5 kez `get` ile iste ve her
   yanıtın kodunu yazdır.

**Beklenen çıktı:**

```
/flaky 200
/limited 200
/limited 200
/limited 200
/limited 200
/limited 200
```

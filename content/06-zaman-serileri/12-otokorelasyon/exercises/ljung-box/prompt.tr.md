Ljung–Box testiyle üç seride kullanılabilir hafıza olup olmadığına bak.

**Yapman gerekenler:**

1. `memory(x, lags)` adında bir fonksiyon yaz: `acorr_ljungbox(x, lags=[lags])`
   çağırsın ve `lb_pvalue` sütunundaki tek değeri dört ondalığa yuvarlayıp
   döndürsün (`float(...)` ile çevir).
2. Üç seri için sonucu ve kararı `ad p karar` biçiminde alt alta yazdır:
   - `"price"`: fiyatın kendisi, 10 gecikme
   - `"price change"`: fiyatın günlük farkı, 10 gecikme
   - `"sales d7"`: satışın `diff(7)`'si, 14 gecikme

   Karar: p < 0.05 ise `memory`, değilse `noise`.
3. Fiyatın günlük farkı için test istatistiğini (`lb_stat`) iki ondalığa
   yuvarlayıp yazdır.

**Beklenen çıktı:**

```
price 0.0 memory
price change 0.2833 noise
sales d7 0.0 memory
12.03
```

Fiyatın kendisi hafızayla dolu görünüyor (trend). Günlük farkında hafıza
bulunamıyor: beyaz gürültüden ayırt edilemiyor. Satışın mevsimsel farkında ise
hâlâ modellenebilir bir yapı var; Bölüm 17'deki modelin işi o.

Büyük bir veri çekme işine başlamadan önce ne kadar süreceğini hesapla. Burada
istek yok; yalnızca hesap.

**Yapman gerekenler:**

1. `min_gap(allowed, window_seconds)` fonksiyonunu yaz: istekler arasındaki
   en kısa süreyi saniye cinsinden, iki ondalığa **yuvarlayarak** döndürsün
   (`round(..., 2)`).
2. `job_minutes(total_requests, allowed, window_seconds)` fonksiyonunu yaz:
   işin en az kaç dakika süreceğini bir ondalığa yuvarlayarak döndürsün.
   (Toplam süre = istek sayısı × en kısa aralık; yuvarlamadan önceki aralıkla
   hesapla.)
3. `jobs` listesindeki her iş için aralığı ve süreyi yazdır.

**Beklenen çıktı:**

```
500 requests: gap 1.0 s, at least 8.3 min
120 requests: gap 0.33 s, at least 0.7 min
10000 requests: gap 3.6 s, at least 600.0 min
```

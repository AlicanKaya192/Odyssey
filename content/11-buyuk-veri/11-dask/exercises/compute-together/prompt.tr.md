Üç farklı sonucu tek bir `dask.compute` çağrısıyla hesapla.

**Yapman gerekenler:**

1. Başlangıç kodu dört CSV dosyasını yazıyor; `dd.read_csv` ile oku.
2. Üç tarif kur:
   - ortalama `unit_price`,
   - `quantity >= 4` olan sipariş sayısı (`shape[0]`),
   - farklı şehir sayısı (`nunique()`).
3. Üçünü tek bir `dask.compute(...)` ile hesapla.
4. Ortalamayı iki ondalığa yuvarlayıp, diğer ikisini olduğu gibi ayrı
   satırlara yazdır.

**Beklenen çıktı:**

```
739.31
44225
8
```

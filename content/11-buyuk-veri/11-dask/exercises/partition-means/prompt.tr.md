Boyları farklı bölümlerde ortalamaların ortalamasının neden yanlış olduğunu
dask ile göster.

**Yapman gerekenler:**

1. `make_orders(120_000)` tablosunu üç dosyaya böl: `part-0.csv` (ilk
   50 000), `part-1.csv` (sonraki 50 000), `part-2.csv` (son 20 000);
   `index=False`.
2. `ddf = dd.read_csv("part-*.csv")`; her bölümün satır sayısını
   `ddf.map_partitions(len).compute()` ile al ve liste olarak yazdır.
3. Her bölümün ortalama `unit_price`'ını
   `ddf.map_partitions(lambda p: p["unit_price"].mean()).compute()` ile al;
   bunların ortalamasını dört ondalığa yuvarlayıp yazdır.
4. dask'ın kendi ortalamasını (`ddf["unit_price"].mean().compute()`) dört
   ondalığa yuvarlayıp yazdır.
5. İki değerin eşit olup olmadığını yazdır.

**Beklenen çıktı:**

```
[50000, 50000, 20000]
740.419
738.3869
False
```

dask'ın `mean`'i toplamı ve sayıyı ayrı biriktiriyor (Bölüm 3); bölüm
ortalamalarının ortalaması küçük bölüme fazla ağırlık veriyor.

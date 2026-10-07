Dört CSV dosyasını tek bir dask tablosu olarak oku ve tembel hesabı gör.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi `orders-0.csv` … `orders-3.csv`
   olarak yazıyor.
2. `ddf = dd.read_csv("orders-*.csv")`; bölüm sayısını yazdır.
3. `total = ddf["quantity"].sum()`; `total`'ın türünün adını
   (`type(total).__name__`) yazdır.
4. `total.compute()` sonucunu yazdır.
5. `len(ddf)` yazdır.

**Beklenen çıktı:**

```
4
Scalar
443926
200000
```

`compute`'tan önce `total` bir sayı değil, bir tarif (`Scalar`).

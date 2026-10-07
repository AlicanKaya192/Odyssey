Ödeme türü başına toplam adedi dask ile hesapla ve pandas'la doğrula.

**Yapman gerekenler:**

1. Başlangıç kodu dört CSV dosyasını yazıyor.
2. `dd.read_csv("orders-*.csv")` ile oku; `groupby("payment")["quantity"].sum()`
   tarifini kur ve `compute()` ile hesapla.
3. Sonucu ada göre sıralayıp her satıra ödeme türünü ve toplamı yazdır.
4. Aynı sonucu pandas ile `orders` tablosundan hesapla ve iki sonucun aynı
   olup olmadığını yazdır (`.equals`, ikisi de ada göre sıralı).

**Beklenen çıktı:**

```
card 319710
cash 35594
transfer 88622
True
```

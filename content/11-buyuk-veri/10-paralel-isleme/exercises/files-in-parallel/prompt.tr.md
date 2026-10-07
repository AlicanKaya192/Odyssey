Dört Parquet dosyasını dört süreçte işle, sonuçları birleştir ve tek
süreçle yapılan hesapla karşılaştır.

**Yapman gerekenler:**

1. `category_quantity(path)` fonksiyonunu dosyanın en dış düzeyinde yaz:
   dosyayı `pd.read_parquet` ile okusun ve
   `groupby("category")["quantity"].sum()` sonucunu döndürsün.
2. `if __name__ == "__main__":` bloğunda:
   - `make_orders(100_000)` tablosunu 25 000'lik dört parçaya böl ve
     `part-0.parquet` … `part-3.parquet` olarak yaz (`index=False`),
   - `ProcessPoolExecutor(max_workers=2)` ile dört dosyayı işle; sonuçları
     `pd.concat(...).groupby(level=0).sum()` ile birleştir,
   - kategoriye göre sıralayıp her satıra kategori ve toplam adedi yazdır,
   - aynı hesabı tablonun tamamında yap ve iki sonucun aynı olup olmadığını
     yazdır.

**Beklenen çıktı:**

```
books 49172
clothing 49153
electronics 30440
home 44366
sports 22432
toys 26628
True
```

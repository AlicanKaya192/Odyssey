Parquet dosyasını `iter_batches` ile parça parça oku ve kategori başına
satılan adedi bul.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi tek grupla yazıyor.
2. `iter_batches(batch_size=60_000, columns=["category", "quantity"])`
   ile gez; her parçayı `to_pandas()` ile tabloya çevir.
3. Her parçada `groupby("category")["quantity"].sum()` sonucunu bir
   listeye ekle; parça sayısını da say.
4. Sonuçları birleştir (`pd.concat(...).groupby(level=0).sum()`),
   büyükten küçüğe sırala ve her satıra kategoriyi ve toplam adedi
   yazdır.
5. Son satıra parça sayısını yazdır.

**Beklenen çıktı:**

```
clothing 99008
books 97594
home 87918
electronics 62055
toys 53359
sports 43992
4
```

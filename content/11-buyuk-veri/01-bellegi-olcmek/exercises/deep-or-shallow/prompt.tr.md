`deep=True`'nun hangi sütunda fark ettiğini kendin gör.

**Yapman gerekenler:**

1. 20 000 siparişlik dosyayı yaz.
2. Dosyayı `payment` sütunu `object` olacak şekilde oku:
   `pd.read_csv("orders.csv", dtype={"payment": object})`.
3. `payment` sütununun belleğini önce `deep` olmadan, sonra `deep=True`
   ile ölç (`df["payment"].memory_usage(...)`); iki sayıyı aynı satıra
   yazdır.
4. Aynısını `quantity` sütunu için yap.
5. `payment` için derin ölçümün sığ ölçüme oranını bir ondalığa yuvarlayıp
   yazdır.

**Beklenen çıktı:**

```
160132 1075752
160132 160132
6.7
```

Sayı sütununda iki ölçüm aynı; `object` metinde sığ ölçüm gerçeğin
küçük bir parçası.

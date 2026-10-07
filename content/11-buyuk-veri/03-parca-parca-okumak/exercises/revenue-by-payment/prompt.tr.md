Ödeme türü başına ciroyu parçalarla hesapla ve tek seferdeki sonuçla
karşılaştır.

**Yapman gerekenler:**

1. 200 000 siparişlik dosyayı yaz.
2. 50 000 satırlık parçalarla oku. Her parçada `revenue = quantity *
   unit_price` sütununu ekle ve `groupby("payment")["revenue"].sum()`
   sonucunu bir listeye koy.
3. Parça sonuçlarını `pd.concat(...).groupby(level=0).sum()` ile birleştir.
4. Büyükten küçüğe sıralayıp her satıra ödeme türünü ve cironun milyon TL
   karşılığını (`/ 1e6`, iki ondalık) yazdır.
5. Dosyayı bir kez de tamamen oku, aynı hesabı yap ve iki sonucun iki
   ondalıkta aynı olup olmadığını yazdır (`True` / `False`).

**Beklenen çıktı:**

```
card 235.58
transfer 65.32
cash 26.53
True
```

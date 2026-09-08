Her ürün için şu biçimde bir etiket üret:

```
etiket
-------------------
Antivirus (Yazilim)
Fare (Aksesuar)
Kablo (Aksesuar)
...
```

Yani: ürün adı, boşluk, parantez içinde kategori.

Tek sütun döndür ve adına `etiket` de. Ada göre sırala.

**`CONCAT` kullan.** `+` ile de birleştirebilirsin ama parçalardan biri
boş olduğunda `+` bütün sonucu siliyor; `CONCAT` boş parçayı atlıyor.
Burada boş bir parça yok ama alışkanlığı doğru yerden edinmek daha iyi.

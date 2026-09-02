Bu alıştırmada bölümün bütün parçalarını bir araya getirip küçük bir rapor
üreteceksin.

**Yapman gerekenler:**

1. `name` sütununu index yapan yeni bir tablo üret, adı `report` olsun.
2. `report` üzerinden **Mina'nın notunu** yazdır.
3. Şehir dağılımını yazdır (her şehirden kaç kişi).
4. **En çok kişinin bulunduğu şehri** yazdır.
5. Tabloda toplam kaç **eksik değer** olduğunu yazdır.
6. Son satırda not ortalamasını (iki basamağa yuvarlanmış) ve en yüksek notu
   **yan yana** yazdır.

**Beklenen çıktı:**

```
91
city
Ankara    3
Izmir     1
Bursa     1
Name: count, dtype: int64
Ankara
0
80.6 91
```

**Üç şeyi birlikte kullanıyorsun:**

- **Index bir sütun olabiliyor.** `set_index("name")` sonrası satırı adıyla
  çağırıyorsun; sayı saymak yerine `loc["Mina", "score"]` yazıyorsun.
- **`value_counts()` bir seri döndürüyor**, o yüzden üzerine `idxmax()`
  uygulanabiliyor.
- **`isna().sum()` sütun başına** sayı veriyor; tablonun tamamı için bir kez
  daha toplaman gerekiyor. Sonuç sıfır — bu veri temiz, ama gerçek veride
  ilk bakılacak sayı budur.

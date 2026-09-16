Bölümün bütün parçalarını bu kez **bir dosyadan** başlayarak
kullanacaksın. Kodu en baştan sen yazıyorsun: içe aktarma da dahil.

Veri `students.csv` dosyasında; ilk satırları şöyle:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**Yapman gerekenler:**

1. `pandas`'ı içe aktar ve dosyayı `data` adıyla oku.
2. Tablonun boyutunu yazdır.
3. `name` sütununu index yapan yeni bir tablo üret, adı `report` olsun;
   onun üzerinden **Mina'nın notunu** yazdır.
4. Her şehirden kaç kişi olduğunu **sözlük olarak** yazdır.
5. En çok kişinin bulunduğu şehri yazdır.
6. Tabloda toplam kaç **eksik değer** olduğunu yazdır.
7. Son satırda not ortalamasını (iki ondalık) ve en yüksek notu **yan
   yana** yazdır.

**Beklenen çıktı:**

```
(12, 5)
91
{'Ankara': 4, 'Izmir': 3, 'Bursa': 3, 'Adana': 2}
Ankara
0
77.42 91
```

**Üç şey birlikte:**

- **`read_csv` ilk satırı sütun adı yapıyor** ve sayı gibi görünen
  sütunları sayıya çeviriyor; `score` üzerinde doğrudan ortalama
  alabilmen bundan.
- **Index bir sütun olabiliyor.** `set_index("name")` sonrası satırı sayıyla
  değil adıyla çağırıyorsun: `loc["Mina", "score"]`.
- **`isna().sum()` sütun başına** sayı veriyor; tablonun tamamı için bir kez
  daha toplaman gerekiyor. Sonuç sıfır — bu dosya temiz. Gerçek veride ilk
  bakılacak sayı bu.

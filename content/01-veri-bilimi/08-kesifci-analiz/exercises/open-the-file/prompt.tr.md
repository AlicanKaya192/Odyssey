Yeni bir veri dosyası açtığında yapılacak ilk dört kontrolü
yazacaksın.

Dosyanın tamamı (`survey.csv`):

```text
city,age,hours,score
Ankara,24,12,88
Izmir,31,5,62
Ankara,28,9,82
Bursa,45,,45
Izmir,22,14,91
Ankara,38,7,70
Bursa,52,3,51
Izmir,27,11,
Ankara,33,6,66
Izmir,29,13,89
```

**Yapman gerekenler:**

1. İçe aktarmayı yaz ve dosyayı oku.
2. Tablonun **boyutunu** yazdır.
3. Sütun **tiplerini** okunur bir liste olarak yazdır.
4. Toplam **boş hücre** sayısını yazdır.
5. `city` sütununda **kaç farklı değer** olduğunu yazdır.

**Beklenen çıktı:**

```
(10, 4)
['str', 'int64', 'float64', 'float64']
2
3
```

**Neden bu dördü:**

- **Boyut** ölçeği söylüyor. On satırlık veri ile yüz binlik veri farklı
  şeyler.
- **Tipler** temizlik gerekip gerekmediğini söylüyor. Burada ilginç bir şey
  var: `hours` ve `score` dosyada tam sayı, ama `float64` çıktı. Sebebi boş
  hücreler: `NaN` bir ondalık sayı, tam sayı sütunu onu taşıyamadığı için
  pandas bütün sütunu ondalığa çeviriyor.
- **Boş hücreler** hangi sonuçlara güvenebileceğini belirliyor.
- **Kaç farklı kategori** olduğu: 3 ise gruplayabilirsin, 10.000 ise o sütun
  bir kimlik sütunudur.

Yeni bir veri açtığında yapılacak ilk dört kontrolü yazacaksın.

**Yapman gerekenler:**

1. Tablonun **boyutunu** yazdır.
2. Sütun **tiplerini** okunur bir liste olarak yazdır.
3. Tablodaki **toplam boş hücre** sayısını yazdır.
4. `city` sütununda **kaç farklı değer** olduğunu yazdır.

**Beklenen çıktı:**

```
(10, 4)
['str', 'int64', 'int64', 'int64']
0
3
```

**Neden bu dördü:**

- **Boyut** ölçeği söylüyor. On satırlık bir veriyle yüz binlik veri farklı
  şeyler.
- **Tipler** temizlik gerekip gerekmediğini söylüyor. Bir sayı sütunu `str`
  görünüyorsa ortalama alamazsın.
- **Boş hücreler** hangi sonuçlara güvenebileceğini belirliyor.
- **Kaç farklı kategori** var: 3 ise gruplayabilirsin, 10.000 ise o sütun
  bir kimlik sütunudur.

`sum()` iki kez gerekiyor: birincisi sütun başına sayıyor, ikincisi onları
topluyor.

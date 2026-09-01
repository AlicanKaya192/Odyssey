Bu alıştırmada veritabanı işlerini fonksiyonların içine koyacaksın — gerçek
bir programda kod böyle düzenleniyor.

Bağlantı ve tablo senin için hazır. Üç fonksiyon yazacaksın; hepsi
`cursor` ve `connection` değişkenlerini kullanacak.

**Yapman gerekenler:**

1. `add_student(name, grade)` — bir satır ekler, `commit` çağırır ve
   tablodaki **toplam satır sayısını** döndürür.

2. `update_grade(name, grade)` — o ismin notunu günceller, `commit` çağırır
   ve **etkilenen satır sayısını** döndürür (`cursor.rowcount`).
   Böyle bir isim yoksa `0` dönmeli.

3. `find_grade(name)` — o ismin notunu döndürür. İsim yoksa `None` döndürür.

4. Sırayla şunları yap ve her sonucu yazdır:
   - `add_student("Ada", 90)`
   - `add_student("Brian", 40)`
   - `update_grade("Ada", 95)`
   - `find_grade("Ada")`
   - `find_grade("Nobody")`

**Beklenen çıktı:**

```
1
2
1
95
None
```

Dikkat: `find_grade` için `fetchone` sonucunu **kontrol etmen** gerekiyor;
sonuç yoksa `None` geliyor ve `[0]` yazarsan hata alırsın.

> Değerleri her zaman `?` ile ver. `UPDATE ... WHERE name = ?` yazmayı
> unutma — `WHERE` olmadan bütün tablo güncellenir.

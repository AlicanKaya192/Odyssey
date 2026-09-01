İlk veritabanını kuracaksın. Diskte iz kalmasın diye bellekte çalışacaksın.

**Yapman gerekenler:**

1. `sqlite3` modülünü al ve `":memory:"` veritabanına bağlan. Bağlantıyı
   `connection` adlı değişkende tut.
2. Bir `cursor` al.
3. `students` adında bir tablo kur: `name TEXT` ve `grade INTEGER`.
4. İki satır ekle: `("Ada", 90)` ve `("Brian", 40)`. Değerleri `?` yer
   tutucusuyla ver.
5. Değişiklikleri kalıcı yap.
6. Bütün satırları oku, `rows` adlı değişkende tut ve yazdır.
7. Satır sayısını yazdır.

**Beklenen çıktı:**

```
[('Ada', 90), ('Brian', 40)]
2
```

Dikkat: her satır bir **demet** olarak geliyor, sözlük değil.

> Ekleme komutu: `cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))`

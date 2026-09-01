Satırları tek tek eklemek yerine hepsini bir seferde ekleyeceksin.

**Yapman gerekenler:**

1. `":memory:"` veritabanına bağlan ve `students` tablosunu kur:
   `name TEXT`, `grade INTEGER`, `city TEXT`.
2. Şu satırları **`executemany` ile** ekle:

```python
[
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
]
```

3. Değişiklikleri kalıcı yap.
4. `total` adlı değişkende toplam satır sayısını tut (`COUNT(*)` kullan).
5. `names` adlı değişkende bütün isimleri **liste** olarak tut. Her satır
   demet geldiği için isimleri tek tek çıkarman gerekiyor.
6. Önce `total`, sonra `names` yazdır.

**Beklenen çıktı:**

```
4
['Ada', 'Brian', 'Grace', 'Alan']
```

> `COUNT(*)` sonucu da bir satır olarak geliyor: `cursor.fetchone()[0]`

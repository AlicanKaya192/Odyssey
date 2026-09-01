Veritabanının asıl işi soruları cevaplamak. Bu alıştırmada Python'da döngü
yazmadan iki soru soracaksın.

**Yapman gerekenler:**

1. `":memory:"` veritabanına bağlan, `students` tablosunu kur
   (`name TEXT`, `grade INTEGER`, `city TEXT`) ve şu satırları ekle:

```python
[
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
]
```

2. `passing` adlı değişkende **notu 50 ve üstü** olanları, **nottan büyükten
   küçüğe sıralı** olarak tut. Yalnızca `name` ve `grade` sütunlarını al.

3. `londoners` adlı değişkende **şehri London olanların adlarını** liste
   olarak tut. Şehri `?` yer tutucusuyla ver.

4. Önce `passing`, sonra `londoners` yazdır.

**Beklenen çıktı:**

```
[('Ada', 90), ('Grace', 75), ('Alan', 60)]
['Ada', 'Brian', 'Alan']
```

Dikkat: tek elemanlı demette sondaki virgül şart — `("London",)`.

> Süzme `WHERE`, sıralama `ORDER BY ... DESC` ile yapılıyor.

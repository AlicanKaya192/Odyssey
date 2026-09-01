Bu alıştırmada hesabı Python'a değil veritabanına yaptıracaksın.

**Yapman gerekenler:**

1. `":memory:"` veritabanına bağlan, `students` tablosunu kur
   (`name TEXT`, `grade INTEGER`, `city TEXT`) ve şu satırları ekle:

```python
[
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
    ("Edith", 95, "New York"),
]
```

2. `by_city` adlı bir **sözlük** kur: anahtar şehir adı, değer o şehrin
   **ortalaması tam sayıya yuvarlanmış** hâli. Ortalamayı `AVG` ile
   veritabanına hesaplattır, `GROUP BY city` kullan.
   Şehirleri **alfabetik sıralı** getir.

3. `best_city` adlı değişkende ortalaması en yüksek şehrin adını tut.

4. Önce `by_city`, sonra `best_city` yazdır.

**Beklenen çıktı:**

```
{'London': 63, 'New York': 85}
New York
```

London ortalaması `(90 + 40 + 60) / 3 = 63.33`, yuvarlanınca `63`.
New York ortalaması `(75 + 95) / 2 = 85.0`, yuvarlanınca `85`.

Dikkat: `AVG` ondalıklı sayı döndürüyor; `round(...)` ile tam sayıya
çevirmen gerekiyor.

> Sıralama için `ORDER BY city` ekle. En yükseği bulmak için sözlükte dolaş.

`warehouses` adında bir tablo kur.

| Sütun | Tip | Kural |
|---|---|---|
| `code` | `NVARCHAR(10)` | birincil anahtar |
| `city` | `NVARCHAR(30)` | boş kalamaz |
| `capacity` | `INT` | boş kalamaz |

Yalnızca tabloyu kur, satır ekleme.

Kontrol tablonun **yapısına** bakıyor: sütunların adı, tipi, uzunluğu, boş
kalıp kalamadığı ve birincil anahtarın hangi sütun olduğu. Yani tipleri
tam olarak yazıldığı gibi seç — `VARCHAR` ile `NVARCHAR` farklı sayılıyor.

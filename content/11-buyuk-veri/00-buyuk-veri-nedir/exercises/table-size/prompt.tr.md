Bir tablonun kaç MB tutacağını dosyayı hiç okumadan hesaplayan bir
fonksiyon yaz.

**Yapman gerekenler:**

`table_mb(rows, columns)` adında bir fonksiyon yaz:

- Tablodaki her değer `int64` ya da `float64`, yani **8 bayt**.
- Toplam baytı `rows * columns * 8` ile bul.
- Sonucu megabayta çevir (`/ 1024**2`) ve **bir ondalığa** yuvarlayıp
  döndür.

Örnekler:

- `table_mb(1_000_000, 10)` → `76.3`
- `table_mb(10_000_000, 6)` → `457.8`
- `table_mb(1000, 1)` → `0.0`

Fonksiyonun yazdırmasına gerek yok; denetleyici onu farklı sayılarla
çağırıp döndürdüğü değere bakacak.

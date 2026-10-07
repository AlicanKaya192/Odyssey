Veri seti hazır; şimdi bir soruya cevap ver: hangi ülkenin yazarlarından kaç
kitap var ve ortalama fiyatları ne?

**Yapman gerekenler:**

1. Bütün kitapları `fetch_all` ile çek.
2. Yazarın ülkesine göre kitap sayısını ve fiyat toplamını `by_country`
   sözlüğünde topla (`{ülke: [sayı, toplam]}` gibi).
3. Ülkeleri kitap sayısına göre çoktan aza (eşitse ülke adına göre) sırala;
   her biri için ülkeyi, sayıyı ve ortalama fiyatı (iki ondalık) yazdır.

**Beklenen çıktı:**

```
UK 10 books, average 9.49
US 6 books, average 10.21
PL 3 books, average 12.20
IE 2 books, average 11.40
RU 2 books, average 16.10
```

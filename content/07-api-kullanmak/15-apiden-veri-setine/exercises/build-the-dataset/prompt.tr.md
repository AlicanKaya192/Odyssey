Hattın tamamı: çek, düzleştir, denetle, yaz.

**Yapman gerekenler:**

1. `to_row(book)` fonksiyonunu yaz: `id`, `title`, `author` (yazarın adı),
   `country`, `year` (int), `price` (float), `tags` (`|` ile birleşik)
   anahtarlı bir sözlük döndürsün.
2. Bütün kitapları `fetch_all` ile çek, satırlara çevir.
3. Denetle: kimlikler tekil olmalı ve satır sayısı 23 olmalı (`assert`).
4. `books.csv`'ye `csv.DictWriter` ile yaz (`newline=""`, `utf-8`).
5. Dosyayı yeniden açıp ilk üç satırını ve toplam satır sayısını (başlık
   hariç) yazdır.

**Beklenen çıktı:**

```
id,title,author,country,year,price,tags
1,Emma,Austen,UK,1815,12.5,classic|novel
2,Dune,Herbert,US,1965,9.99,scifi|classic
rows: 23
```

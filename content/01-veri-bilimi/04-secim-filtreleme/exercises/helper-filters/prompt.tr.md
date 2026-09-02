Uzun koşulları kısaltan üç metodu ve bir kısayolu kullanacaksın.

**Yapman gerekenler:**

1. Şehri `Izmir` **veya** `Bursa` olanların `name` ve `city` sütunlarını
   yazdır — `isin` kullan.
2. Yaşı 21 ile 22 **arasında** olanların adlarını liste hâlinde yazdır —
   `between` kullan.
3. Şehri Ankara **olmayanların** adlarını liste hâlinde yazdır — aynı
   maskenin tersini al.
4. En yüksek notlu **iki satırın** `name` ve `score` sütunlarını yazdır.

**Beklenen çıktı:**

```
    name   city
1  Kerem  Izmir
3  Deniz  Bursa
5   Sila  Izmir
['Ada', 'Mina', 'Efe']
['Kerem', 'Deniz', 'Sila']
   name  score
2  Mina     91
4   Efe     88
```

**Bilmen gerekenler:**

- `isin`, birçok değeri `|` ile bağlamanın kısa yolu.
- `between(21, 22)` **iki ucu da** içeri alıyor — Python dilimlerine
  alışkınsan bunu `21 <= x < 22` sanabilirsin.
- `~` bir maskenin tersini alıyor. `!=` ile tek tek yazmaktan kısa.
- `nlargest` hepsini sıralamıyor, yalnızca en büyükleri buluyor; büyük
  veride farkı hissediliyor.

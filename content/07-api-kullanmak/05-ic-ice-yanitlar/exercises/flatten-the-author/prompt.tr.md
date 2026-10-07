Her kitaptan tablonun bir satırını kuracaksın. `author` iç içe bir sözlük ve
Herbert'in kaydında `country` yok; fiyat metin olarak gelmiş.

**Yapman gerekenler:**

1. `rows` adlı bir liste kur. Her satır şu anahtarlara sahip bir sözlük
   olsun: `id`, `title`, `price` (**float**), `author_name`,
   `author_country` (yoksa `"unknown"`).
2. Her satırı `|` ile ayırarak yazdır.
3. Son satırda fiyatların toplamını iki ondalıkla yazdır.

**Beklenen çıktı:**

```
1 | Emma | 12.5 | Austen | UK
2 | Dune | 9.99 | Herbert | unknown
3 | Ulysses | 15.0 | Joyce | IE
4 | Solaris | 11.2 | Lem | PL
5 | Persuasion | 8.75 | Austen | UK
total price: 57.44
```

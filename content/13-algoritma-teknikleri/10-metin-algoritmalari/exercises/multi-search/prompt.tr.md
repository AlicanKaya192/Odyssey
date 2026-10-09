`multi_search(text, patterns)` fonksiyonunu yaz: bütün kalıplar **aynı
uzunlukta**. Metindeki her eşleşme için `(konum, kalıp)` demetini, konuma göre
sıralı bir liste olarak döndürsün.

Rabin-Karp fikri: kalıpları bir **kümeye** koy, metnin her penceresini kümede
ara (Python kümesi arka planda hash kullanıyor). Böylece kalıp sayısı ne olursa
olsun her pencere tek bir arama.

**Beklenen çıktı:**

```
(4, 'cat')
(19, 'mat')
(30, 'hat')
```

pandas'ta tek bir köşeli parantez fark yaratıyor. Bu alıştırmada onu
gözünle göreceksin.

**Yapman gerekenler:**

1. `name` ve `score` sütunlarını içeren bir tablo üret, adı `subset` olsun.
2. `subset` tablosunu yazdır.
3. `data["score"]` ifadesinin **tipinin adını** yazdır.
4. `data[["score"]]` ifadesinin **tipinin adını** yazdır.

**Beklenen çıktı:**

```
    name  score
0    Ada     82
1  Kerem     74
2   Mina     91
3  Deniz     68
4    Efe     88
Series
DataFrame
```

Tipin adını `type(x).__name__` veriyor.

**Son iki satır bu bölümün en önemli ayrımı:** aynı sütunu istedin, biri
**seri** biri **tablo** döndü. Fark tek bir köşeli parantez. Serinin
metotları başka (`str.lower()`, `value_counts()`), tablonunki başka
(`shape` iki değer veriyor). Hangisini aldığını bilmezsen `AttributeError`
alıp neden olduğunu uzun süre anlamıyorsun.

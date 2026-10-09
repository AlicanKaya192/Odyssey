`by_columns(rows, cols)` fonksiyonunu yaz: satırları (`rows`, liste
listesi) `cols` listesindeki sütun numaralarına göre sırayla sıralayıp
döndürsün: önce ilk sütun, eşitse ikincisi... `itemgetter(*cols)` bütün
sütunları birlikte veren anahtardır.

**Beklenen çıktı:**

```
['pen', 3, 1.5]
['book', 3, 12.0]
['ink', 10, 0.5]
```

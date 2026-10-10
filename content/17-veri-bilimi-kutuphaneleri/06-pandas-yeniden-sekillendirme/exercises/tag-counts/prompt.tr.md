`tag_counts(tags)` her biri virgülle ayrılmış etiketler olan metinlerin
listesini alıyor (`"gift,fast"`). Her etiketin kaç kez geçtiğini
`{etiket: sayı}` olarak, etiket adına göre sıralı döndürsün:
`str.split(",")` → `explode` → `value_counts()` → `sort_index()`.
**Döngü yazma.**

**Beklenen çıktı:**

```
{'eco': 1, 'fast': 3, 'gift': 2}
```

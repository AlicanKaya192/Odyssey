Bu alıştırmada `bisect` modülünü kullanacaksın.

1. `count_value(items, x)`: sıralı listede `x`'in kaç kez geçtiğini döndürsün.
2. `count_in_range(items, low, high)`: sıralı listede `low <= değer <= high`
   olan kaç değer olduğunu döndürsün.

İkisi de `O(log n)` olmalı: `.count()` ya da döngü kullanma, iki sınırın
farkını al. Hangi sınır için `bisect_left`, hangisi için `bisect_right`?
`low` ve `high`'ın kendisi de sayılmalı.

**Beklenen çıktı:**

```
3
0
6
0
```

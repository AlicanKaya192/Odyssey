`order_by_grade(records)` fonksiyonunu yaz: `records` `[ad, not]`
çiftlerinden oluşan bir liste, notlar 1 ile 5 arasında. Öğrencilerin
**adlarını** nota göre artan sırayla döndürsün; aynı nottakiler **girdideki
sıralarını korusun**.

- `[["Ada", 3], ["Bora", 1], ["Cem", 3], ["Deniz", 2]]` →
  `["Bora", "Deniz", "Ada", "Cem"]`

Her not için bir kova listesi kur (`buckets[grade].append(name)`), sonra
kovaları sırayla birleştir. `sorted` ve `.sort()` kullanma.

**Beklenen çıktı:**

```
['Bora', 'Deniz', 'Ada', 'Cem']
[]
```

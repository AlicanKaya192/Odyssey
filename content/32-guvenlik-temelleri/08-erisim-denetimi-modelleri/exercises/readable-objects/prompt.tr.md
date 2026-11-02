Bell-LaPadula düzeyleri: `LEVELS = ["public", "internal", "secret",
"top-secret"]`. `objects` nesne adından gizlilik derecesine giden bir
sözlük.

`readable_objects(clearance, objects)` yetki düzeyi `clearance` olan
birinin **okuyabileceği** nesnelerin adlarını abece sırasında döndürsün
(yukarı okuma yok: nesnenin düzeyi ≤ kişinin düzeyi).

**Beklenen çıktı:**

```
['menu', 'plan']
['menu', 'plan', 'salary']
[]
```

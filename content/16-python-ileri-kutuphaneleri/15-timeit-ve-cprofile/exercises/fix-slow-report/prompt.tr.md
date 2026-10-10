`report(rows)` her farklı değerin kaç kez geçtiğini sayıyor ama her anahtar
için `rows.count` ile listenin tamamını tarıyor: 300 000 satırda süre
sınırını aşıyor. Aynı sözlüğü **tek geçişte** üreten bir çözüm yaz
(`collections.Counter`). Beklenen çıktı:

```
8000 38
```

**Beklenen çıktı:**

```
8000 38
```

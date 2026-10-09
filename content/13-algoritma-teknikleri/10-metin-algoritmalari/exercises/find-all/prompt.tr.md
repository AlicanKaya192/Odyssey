`find_all(text, pattern)` fonksiyonunu **saf arama** ile yaz: kalıbın metinde
başladığı bütün konumları sırayla döndürsün; üst üste binenler de sayılır
(`"aaaa"` içinde `"aa"`: `0, 1, 2`).

`find`, `index`, `count`, `startswith` yok: harfleri kendin karşılaştır.

**Beklenen çıktı:**

```
[0, 7]
[0, 1, 2]
[]
```

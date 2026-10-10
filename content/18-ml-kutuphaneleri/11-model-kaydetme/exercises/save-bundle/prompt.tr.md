`save_bundle(path, threshold)` modeli bir sözlükle kaydedip geri yüklüyor.
Sözlüğe `"sklearn"` (`sklearn.__version__`) ve `"columns"` (`COLUMNS`)
anahtarlarını da eklesin. Fonksiyon `[anahtarlar, eşik, sütunlar]` döndürüyor;
başlangıç kodunda iki anahtar eksik.

**Beklenen çıktı:**

```
['columns', 'model', 'sklearn', 'threshold']
0.3
['age', 'income', 'visits', 'score']
```

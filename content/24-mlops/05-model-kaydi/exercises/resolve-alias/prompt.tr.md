Kayıt bir sözlük: her model adının altında `"versions"` listesi (`{"version": ..., "file": ...}`) ve `"aliases"` sözlüğü (`{"production": 2}`) var. `resolve(registry, name, alias)` fonksiyonunu yaz ve etiketin gösterdiği sürümün **dosya yolunu** döndür.

- Model adı kayıtta yoksa `None`.
- Etiket yoksa `None`.
- Etiketin gösterdiği numarada sürüm yoksa `None`.

**Beklenen çıktı:**

```
models/churn-v2.pkl
models/churn-v1.pkl
None
None
```

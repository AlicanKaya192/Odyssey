`store.py`'deki `read_model()` modeli diskten okuyor ve her çağrıyı sayıyor (`reads["count"]`). `get_model()` fonksiyonunu yaz:

- İlk çağrıda `read_model()` ile modeli okusun ve modül düzeyindeki `_model` değişkenine koysun.
- Sonraki çağrılarda diski okumadan aynı nesneyi döndürsün.

Beş istekten sonra disk yalnızca **bir kez** okunmuş olmalı.

**Beklenen çıktı:**

```
reads: 1
same object: True
version: 3
```

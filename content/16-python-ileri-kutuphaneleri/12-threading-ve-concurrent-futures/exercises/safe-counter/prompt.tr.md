`Counter.add_many(n)` değeri `n` kez artırıyor; dört iş parçacığı aynı
sayacı 500'er kez artırınca 2000 olmalı ama artışlar kayboluyor. `__init__`
içinde bir `threading.Lock()` kur ve oku-yaz adımını `with self.lock:`
bloğuna al.

**Beklenen çıktı:**

```
2000
```

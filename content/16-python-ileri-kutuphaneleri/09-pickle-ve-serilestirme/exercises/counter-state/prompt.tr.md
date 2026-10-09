`Counter` sınıfı bir `threading.Lock` tutuyor ve bu yüzden pickle'lanamıyor.
Sınıfa `__getstate__` (özelliklerin kopyası, `lock` çıkarılmış) ve
`__setstate__` (durumu geri koy, `lock`'u yeniden kur) ekle. Alttaki kod
sayacı gidip getirip bir kez daha artırıyor.

**Beklenen çıktı:**

```
3 lock
```

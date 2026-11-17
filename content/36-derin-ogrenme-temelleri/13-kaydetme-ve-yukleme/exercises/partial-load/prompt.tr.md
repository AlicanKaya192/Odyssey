`missing_after_load(extra)` küçük bir modeli kaydediyor ve sonuna `extra` tane
`ReLU + Linear(3, 3)` eklenmiş daha uzun bir model kuruyor. Kaydedilen
sayıları uzun modele `strict=False` ile yükle ve sonucun `missing_keys`
listesini döndür.

**Beklenen çıktı:**

```
['4.weight', '4.bias']
```

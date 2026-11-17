Kazançlı veri, 1B evrişimli ağ, optimizer ve `DataLoader` hazır.

1. 10 dönem eğit: `model.train()`, her grupta `zero_grad`, `cross_entropy`,
   `backward`, `step`.
2. `model.eval()`; test pencerelerinde (`500:600`) tahmin et.
3. `acc` (doğruluk) ve `recall` (arıza sınıfının duyarlılığı) hesapla.

**Beklenen çıktı:**

```
True True
```

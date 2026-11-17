`apply_kernel(signal, kernel)` yanlılıksız bir `nn.Conv1d(1, 1,
len(kernel))` kursun, ağırlığını `kernel` yapsın, sinyali `(1, 1, T)`
şeklinde ondan geçirsin ve çıkışı düz liste olarak döndürsün.

**Beklenen çıktı:**

```
[0.0, 1.0, 2.0, 0.0, -2.0, -1.0]
[6.0, 9.0]
```

`TwoLayer` sınıfının katmanları hazır; `forward` girdiyi olduğu gibi
döndürüyor. `forward`'ı düzelt: `first` → ReLU → `second`. `output` bütün
ağırlıkları 0,5 yapıp çıktıyı veriyor.

**Beklenen çıktı:**

```
[[4.5, 4.5]]
[[0.5, 0.5]]
```

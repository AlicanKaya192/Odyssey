`lora_forward(x, W, b, A, B, alpha)` LoRA katmanının çıkışını hesaplasın:
`x · Wᵀ + b + (x · Aᵀ · Bᵀ) · alpha / r`. Rank `r`, `A`'nın satır sayısı.
Her değeri 3 basamakla, iç içe liste olarak döndürsün.

**Beklenen çıktı:**

```
[[4.0, 2.0]]
```

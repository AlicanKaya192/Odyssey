`lora_forward(x, W, A, B)` donuk `W` ve LoRA düzeltmesiyle katmanın çıktısını
döndürsün: `x @ W + (x @ A) @ B`. Sonuç her sayısı 3 basamağa yuvarlanmış
iç içe liste. (`x @ (W + A @ B)` ile aynı sonucu verir; büyük katmanda
`(x @ A) @ B` daha ucuzdur.)

**Beklenen çıktı:**

```
[[1.0, 3.0]]
```

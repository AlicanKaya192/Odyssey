`param_bytes(sizes, bytes_per_value)` art arda doğrusal katmanlardan oluşan
bir ağın parametre belleğini bayt olarak hesaplasın. `sizes = [64, 128, 10]`
iki katman demek: `Linear(64, 128)` ve `Linear(128, 10)`; her katmanda
ağırlık ve sapma var.

**Beklenen çıktı:**

```
38440
19220
```

`gan_param_count(z_dim, hidden)` dersteki iki ağı kursun: üretici
`z_dim → hidden → 1` (arada ReLU), ayırt edici `1 → hidden → 1` (arada
`LeakyReLU(0.2)`). İki ağın parametre sayısını `[üretici, ayırt edici]`
listesi olarak döndürsün.

**Beklenen çıktı:**

```
[97, 49]
[33, 25]
```

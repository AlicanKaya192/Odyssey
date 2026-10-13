`sgd_step(v, u_pos, u_negs, lr)` bir çift için dersteki güncellemeyi
yapsın:

- `g_pos = σ(v · u_pos) − 1`, her olumsuz için `g_k = σ(v · u_k)`
- `v` için türev `g_pos · u_pos + Σ g_k · u_k`
- `u_pos ← u_pos − lr · g_pos · v`, `u_k ← u_k − lr · g_k · v`,
  `v ← v − lr · türev` (hepsi **eski** değerlerle)

Üç sonucu 3 basamaklı listeler olarak `[v, u_pos, u_negs]` döndürsün.

**Beklenen çıktı:**

```
[0.517, -0.532]
[1.013, -1.013]
[[0.174, 0.126]]
```

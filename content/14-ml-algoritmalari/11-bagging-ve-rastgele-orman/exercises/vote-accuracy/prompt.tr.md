`vote_accuracy(n, p)` fonksiyonunu yaz: her biri `p` olasılıkla doğru, hataları
bağımsız `n` modelin (n tek) çoğunluk oyunun doğru olma olasılığı:
`Σ C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ`, `k` `n // 2 + 1`'den `n`'e. `round(..., 3)`.
`math.comb` kullanabilirsin.

**Beklenen çıktı:**

```
1 0.6
5 0.683
25 0.846
101 0.979
0.306
```

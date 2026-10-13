`forward(A, E, W1, W2)` dersteki ağın ileri hesabını yapsın (sabitler yok):
`x = A @ E`, `h = ReLU(x @ W1)`, `p = softmax(h @ W2)`. Olasılıkları 3
basamaklı liste listesi olarak döndürsün.

**Beklenen çıktı:**

```
[[0.679, 0.321]]
[[0.731, 0.269], [0.378, 0.622]]
```

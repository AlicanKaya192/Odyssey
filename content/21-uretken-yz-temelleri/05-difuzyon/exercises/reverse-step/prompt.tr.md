`reverse_step(x, eps_hat, t, z)` geri sürecin bir adımını uygulasın:
`(x - betas[t] / sqrt(1 - alpha_bar[t]) * eps_hat) / sqrt(alphas[t])`;
`t` 0 değilse sonuca `sqrt(betas[t]) * z` eklensin (son adımda gürültü
yok). `x`, `eps_hat` ve `z` nokta listeleri. Sonuç, her sayısı 4 basamağa
yuvarlanmış iç içe liste.

**Beklenen çıktı:**

```
[[0.7319, -1.2633], [2.0708, 0.1124]]
[[0.499, -1.0021]]
```

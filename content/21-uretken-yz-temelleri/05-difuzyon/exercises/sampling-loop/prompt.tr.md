Başlangıç kodu dersteki ağı 3000 adım eğitiyor (`net`). `generate(n, seed)`
geri süreci yazsın: `rng = np.random.default_rng(seed)`,
`x = rng.normal(size=(n, 2))`; `t` 99'dan 0'a: `eps_hat = forward(features(x,
np.full(n, t)), net)[-1]`, geri adım formülü, `t` 0 değilse
`np.sqrt(betas[t]) * rng.normal(size=x.shape)` ekle. Sonunda
`mode_report(x)` ile `[en az n'nin %2'sini alan küme sayısı, kümeye yakın
oran]` döndür; oran 3 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[8, 0.615]
```

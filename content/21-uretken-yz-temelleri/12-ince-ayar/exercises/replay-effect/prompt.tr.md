Salt okunur `finetune_tools.py` dersteki veriyi ve fonksiyonları içeriyor
(`X_old`, `y_old`, `X_new`, `y_new`, `init`, `train`, `accuracy`).
`replay_effect(k, seed)`: `rng = np.random.default_rng(seed)` ile ağı kur
ve 0–4'te ön eğit (`train(init([64, 32, 10], rng), X_old[:700], y_old[:700],
500)`). Yeni görevin her rakamından 10 örnek al (dersteki `few`). `k > 0` ise
`rng.choice(700, k, replace=False)` ile eski örnek seçip karıştır. 300 adım
ince ayar yap ve `[yeni görev doğruluğu, eski görev doğruluğu]` döndür
(test kümeleri `X_new[400:]` ve `X_old[700:]`).

**Beklenen çıktı:**

```
0 [0.931, 0.065]
50 [0.901, 0.95]
```

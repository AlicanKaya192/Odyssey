Başlangıç kodu halkadan 2000 nokta (`x0`), küme merkezlerini ve dersteki
gürültü takvimini hazırlıyor. `noisy_near(t, seed)` `t`. adımın gürültülü
hâlini kursun: `eps = np.random.default_rng(seed).normal(size=x0.shape)`,
`xt = sqrt(alpha_bar[t]) * x0 + sqrt(1 - alpha_bar[t]) * eps`. Döndür:
`[en yakın merkeze uzaklığı 0,3'ten küçük noktaların oranı, xt'nin bütün
değerlerinin standart sapması]`; oran 3, sapma 2 basamağa yuvarlanmış
`float`.

**Beklenen çıktı:**

```
0 [0.993, 1.41]
29 [0.109, 1.3]
99 [0.041, 1.01]
```

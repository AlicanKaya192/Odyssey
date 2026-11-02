Oturum süresinden (`minutes`) `n` = 4 ve `n` = 64 kişilik 3000'er örneklem
çek: `rng.choice(x, size=(3000, n)).mean(axis=1)` (aynı `rng`, önce 4 sonra
64). Her satıra `n`, ortalamaların ortalaması (2 basamak), ortalamaların
standart sapması (3 basamak) ve `x.std() / np.sqrt(n)` formülünü (3 basamak)
yaz. Son iki sütun birbirine yakın çıkmalı.

**Beklenen çıktı:**

```text
4 9.03 3.052 3.064
64 9.05 0.764 0.766
```

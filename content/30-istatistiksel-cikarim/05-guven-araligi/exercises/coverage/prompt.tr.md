`coverage(values, n, reps, seed, level)` güven aralığı yönteminin sözünü
tutup tutmadığını ölçsün: `np.random.default_rng(seed)` ile `reps` tane `n`
kişilik iadeli örneklem çek, her biri için `level` güvenli t aralığı kur ve
`values`'ın gerçek ortalamasını yakalayanların payını 3 basamakla döndür.
Başlangıç kodu çarpanı hep 1,96 alıyor: hem küçük örneklemde hem %90'da
yanlış.

**Beklenen çıktı:**

```text
0.937
0.904
```

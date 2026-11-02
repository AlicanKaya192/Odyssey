`efficiency_ratio(values, n, reps, seed)` medyanın ortalamaya göre kaç kat
veri istediğini ölçsün: `np.random.default_rng(seed)` ile `reps` tane `n`
kişilik iadeli örneklem çek, ortalamaların ve medyanların standart
sapmalarını bul ve **varyansların** oranını, yani
`(sd_median / sd_mean) ** 2` değerini 2 basamakla döndür. Başlangıç kodu
kareyi almıyor.

**Beklenen çıktı:**

```text
2.69
```

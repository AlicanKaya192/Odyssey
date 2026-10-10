Müşteriler farklı gün sayısı (`days`) boyunca sigortalı. `claim_model()`
Poisson GLM'i `offset=np.log(d3["days"])` ile eğitsin ve
`[risk_oran_oranı, sabit]` döndürsün (`np.exp` ile oran oranı; ikisi de 3
basamak). Başlangıç kodu offset'i unutuyor.

**Beklenen çıktı:**

```
[1.578, -3.958]
```

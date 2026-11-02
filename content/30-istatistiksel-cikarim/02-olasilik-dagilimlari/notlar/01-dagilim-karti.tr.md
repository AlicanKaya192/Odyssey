## Dağılım nesnesi kurmak

```python
from scipy import stats

buyers = stats.binom(n=20, p=0.114)      # kesikli
visits = stats.poisson(mu=3.0)           # kesikli
load = stats.norm(loc=850, scale=120)    # sürekli
wait = stats.expon(scale=10)             # sürekli, ortalaması 10
```

## Her dağılımda aynı metotlar

| Metot | Soru | Not |
|---|---|---|
| `pmf(k)` | tam `k` olasılığı | yalnızca kesikli |
| `pdf(x)` | `x`'teki yoğunluk | yalnızca sürekli; olasılık değil |
| `cdf(x)` | `x` ya da daha azı | birikimli |
| `sf(x)` | `x`'ten fazlası | `1 - cdf(x)`, küçük olasılıkta daha kesin |
| `ppf(q)` | altında `q` kalan değer | `cdf`'nin tersi |
| `mean()`, `std()` | beklenen değer, sapma | |
| `rvs(size, random_state)` | rastgele örnek | tohumla tekrarlanabilir |

## Hangi dağılım?

| Durum | Dağılım |
|---|---|
| Evet/hayır sonuçlu $n$ bağımsız deneme | binom |
| Tek bir evet/hayır | Bernoulli (`stats.bernoulli(p)`) |
| Bir aralıkta kaç olay | Poisson |
| İki olay arasında geçen süre | üstel (`stats.expon`) |
| Simetrik, çan biçimli ölçüm | normal |
| Her değer eşit olası | düzgün (`stats.uniform`) |

## Formüller

- Binom: ortalama $np$, sapma $\sqrt{np(1-p)}$.
- Poisson: ortalama ve varyans $\lambda$.
- Normal: %68 / %95 / %99,7 kuralı; $\pm 1{,}96\,\sigma$ içinde tam %95.

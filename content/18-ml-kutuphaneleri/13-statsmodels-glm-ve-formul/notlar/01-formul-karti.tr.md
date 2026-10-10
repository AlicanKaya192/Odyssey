## Formül dili

| Yazım | Anlamı |
|---|---|
| `y ~ a + b` | `a` ve `b` ile `y`; sabit kendiliğinden |
| `y ~ a + b - 1` | sabitsiz |
| `C(c)` | kategorik (kukla sütunlar) |
| `C(c, Treatment('X'))` | taban kategori `X` |
| `a:b` | yalnızca etkileşim |
| `a * b` | `a + b + a:b` |
| `I(a ** 2)`, `I(a / 1000)` | işlem olduğu gibi |
| `np.log(a)`, `np.sqrt(a)` | NumPy fonksiyonları |
| `Q("my col")` | adında boşluk olan sütun |

## Modeller

| Yazım | Sonuç türü |
|---|---|
| `smf.ols(f, data)` | sürekli sayı |
| `smf.logit(f, data)` | 0/1; `np.exp(params)` olasılık oranı |
| `smf.glm(f, data, family=sm.families.Poisson())` | sayım; `offset=np.log(süre)` |
| `smf.glm(f, data, family=sm.families.NegativeBinomial(alpha=1.0))` | aşırı yayılmış sayım |
| `smf.glm(f, data, family=sm.families.Binomial())` | 0/1, GLM yoluyla (logit ile aynı) |
| `smf.glm(f, data, family=sm.families.Gamma(link=sm.families.links.Log()))` | artı, sağa çarpık (tutar) |

## Katsayıyı okumak

| Model | `exp(katsayı)` |
|---|---|
| OLS | gerekmez: birim başına değişim |
| Logit | olasılık oranı (odds ratio) |
| Poisson / Neg. binom | oran oranı (rate ratio) |
| Log bağlantılı Gamma | ortalamanın çarpanı |

## Kurallar

- Tahmin için yeni veri ham verilir; formül kodlamayı kendisi uygular.
- `.fit(disp=0)` logit/negatif binom eğitim mesajlarını susturur.
- Sayım modelinde gözlem süresi farklıysa `offset` unutulmaz.

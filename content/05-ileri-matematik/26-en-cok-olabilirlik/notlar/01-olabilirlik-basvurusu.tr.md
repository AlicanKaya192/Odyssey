Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Formül |
|---|---|
| olabilirlik | $L(\theta) = \prod_{i} f(x_i \mid \theta)$ (veri sabit) |
| log-olabilirlik | $\ell(\theta) = \sum_{i} \ln f(x_i \mid \theta)$ |
| MLE | $\hat{\theta} = \arg\max_\theta \ell(\theta)$ |
| negatif log-olabilirlik | $\text{NLL} = -\ell(\theta)$, en küçük yapılır |
| Laplace düzeltmesi | $\hat{p} = \frac{k + 1}{n + 2}$ |

## Hazır sonuçlar

| Dağılım | MLE |
|---|---|
| Bernoulli / binom | $\hat{p} = \frac{k}{n}$ |
| Poisson | $\hat{\lambda} = \bar{x}$ |
| Üstel | $\hat{\lambda} = \frac{1}{\bar{x}}$ |
| Normal | $\hat{\mu} = \bar{x}$, $\hat{\sigma}^2 = \frac{1}{n}\sum (x_i - \bar{x})^2$ |
| Kategorik | $\hat{p}_k = \frac{n_k}{n}$ |

## Adımlar

1. $\ell(\theta) = \sum \ln f(x_i \mid \theta)$'yı yaz; sabitleri at.
2. $\ell'(\theta) = 0$'ı çöz.
3. İkinci türevin negatif olduğunu (ya da uçları) kontrol et.
4. Kapalı çözüm yoksa NLL'ye gradyan inişi uygula.

## Kayıplarla bağlantı

| Model varsayımı | NLL |
|---|---|
| normal gürültü, sabit $\sigma$ | kare hataların toplamı (MSE) |
| Bernoulli hedef | log-loss (ikili çapraz entropi) |
| kategorik hedef | çapraz entropi |

## Pratik ipuçları

- Log al: çarpım toplam olur, küçük sayılar taşmaz.
- $g(\hat{\theta})$, $g(\theta)$'nın MLE'sidir (değişmezlik).
- Hiç görülmemiş sonuca $0$ verme; düzeltme ya da önsel ekle.

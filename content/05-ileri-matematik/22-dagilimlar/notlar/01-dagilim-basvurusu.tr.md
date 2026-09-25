Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kesikli dağılımlar

| Dağılım | $P(X = k)$ | $E[X]$ | $\operatorname{Var}(X)$ | Ne zaman |
|---|---|---|---|---|
| Bernoulli($p$) | $p^k (1 - p)^{1 - k}$, $k \in \{0, 1\}$ | $p$ | $p(1 - p)$ | tek evet–hayır |
| Binom($n, p$) | $\binom{n}{k} p^k (1 - p)^{n - k}$ | $np$ | $np(1 - p)$ | $n$ bağımsız denemede başarı |
| Poisson($\lambda$) | $\dfrac{e^{-\lambda} \lambda^k}{k!}$ | $\lambda$ | $\lambda$ | sabit hızda olay sayısı |

Büyük $n$, küçük $p$ ve $np = \lambda$ ise binom $\approx$ Poisson.

## Sürekli dağılımlar

| Dağılım | Yoğunluk | $E[X]$ | $\operatorname{Var}(X)$ |
|---|---|---|---|
| Tekdüze($a, b$) | $\frac{1}{b - a}$ | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ |
| Üstel($\lambda$) | $\lambda e^{-\lambda x}$ | $\frac{1}{\lambda}$ | $\frac{1}{\lambda^2}$ |
| Normal($\mu, \sigma^2$) | $\frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ |

Üstel: $P(X > t) = e^{-\lambda t}$, hafızasız.

## Normal dağılım

- $\mu \pm \sigma$: yüzde $68$; $\mu \pm 2\sigma$: yüzde $95$;
  $\mu \pm 3\sigma$: yüzde $99{,}7$.
- $Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)$.

| $z$ | $0{,}5$ | $1$ | $1{,}5$ | $1{,}96$ | $2$ | $3$ |
|---|---|---|---|---|---|---|
| $P(Z \leq z)$ | $0{,}691$ | $0{,}841$ | $0{,}933$ | $0{,}975$ | $0{,}977$ | $0{,}999$ |

Simetri: $P(Z \leq -z) = 1 - P(Z \leq z)$.

## Makine öğrenmesinde

| Model | Dağılım |
|---|---|
| lojistik regresyon, ikili sınıflandırma | Bernoulli |
| softmax, çok sınıflı | kategorik |
| doğrusal regresyon, MSE | normal hata |
| sayım regresyonu | Poisson |

## Pratik ipuçları

- "Kaç tane" sorusunda sabit deneme sayısı varsa binom, yoksa Poisson.
- "Ne kadar beklenir" sorusu üstel.
- Normal soruyu önce z'ye çevir, sonra tabloya bak.
- "En az bir" için yine tümleyen: $1 - P(X = 0)$.

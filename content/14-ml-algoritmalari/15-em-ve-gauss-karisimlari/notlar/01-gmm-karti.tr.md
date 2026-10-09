## Model

Yoğunluk: `p(x) = Σⱼ πⱼ · N(x; μⱼ, Σⱼ)`, paylar `πⱼ` toplamı 1.

## EM adımları

| Adım | Ne hesaplanır |
|---|---|
| E | `rᵢⱼ = πⱼ N(xᵢ; μⱼ, Σⱼ) / Σₗ πₗ N(xᵢ; μₗ, Σₗ)` |
| M | `Nⱼ = Σᵢ rᵢⱼ`, `πⱼ = Nⱼ / n` |
| M | `μⱼ = Σᵢ rᵢⱼ xᵢ / Nⱼ` |
| M | `Σⱼ = Σᵢ rᵢⱼ (xᵢ − μⱼ)(xᵢ − μⱼ)ᵀ / Nⱼ` |

Log-olabilirlik `Σᵢ ln p(xᵢ)` her turda azalmaz; artış çok küçülünce durulur.

## Kovaryans türleri (`covariance_type`)

| Tür | Şekil | Parametre |
|---|---|---|
| `spherical` | yuvarlak, bileşen başına tek varyans | en az |
| `diag` | eksenlere paralel elips | orta |
| `tied` | bütün bileşenler aynı elips | orta |
| `full` | her bileşen kendi eğik elipsi | en çok |

## K-Means ile karşılaştırma

| | K-Means | GMM |
|---|---|---|
| Atama | sert (tek küme) | yumuşak (olasılık) |
| Küme şekli | yuvarlak | elips (`full`) |
| Ölçüt | inertia | log-olabilirlik, BIC |
| Hız | hızlı | daha yavaş |

K-Means, bütün varyansları eşit ve çok küçük olan bir GMM'in sert atamalı
hâli gibi düşünülebilir.

## Sık hatalar

- Bileşen sayısını log-olabilirliğe göre seçmek: hep en büyük `k` kazanır;
  BIC ya da AIC kullan.
- Tek başlangıç: EM yerel en iyiye takılır (`n_init`).
- Bir bileşenin tek noktaya çökmesi: varyans sıfıra gider, olabilirlik
  sonsuza; scikit-learn köşegene küçük bir `reg_covar` ekler.
- Ölçeklememek: farklı birimler kovaryansı da çarpıtır.

VAE'nin kaybında iki terim çekişir: yeniden kurma iyi bir kopya ister, KL
kodların standart normale yakın durmasını. KL'nin ne zaman büyüdüğünü küçük
tensörlerle görelim:

```python
import torch


def kl_term(mu, logvar):
    return -0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))


zeros = torch.zeros(1, 4)
print(kl_term(torch.ones(1, 4), zeros).item())
print(kl_term(zeros, torch.full((1, 4), -2.0)).item() > 0)
```

```text
2.0
True
```

- Ortalama 0'dan uzaklaşınca KL büyür: her boyutta `mu = 1` için
  `0,5 · 1² = 0,5`, dört boyutta 2.
- Varyans 1'den küçülünce de büyür (`logvar = −2`): kod tek bir noktaya
  çökmeye çalışırsa ceza alır.

## β ile denge

Kaybı `yeniden kurma + β · KL` diye yazmak yaygın (β-VAE):

| β | Ne olur |
|---|---|
| Küçük (0,1) | Yeniden kurma çok iyi; gizli uzay düzensiz, çekilen kodlar anlamsız görüntü verebilir |
| 1 | Klasik VAE |
| Büyük (4+) | Kodlar düzenli ve birbirinden bağımsız; görüntüler bulanık |
| Çok büyük | Kod girdiyi taşımayı bırakır, her girdiye aynı ortalama görüntü (arka çökme, posterior collapse) |

Eğitimin başında β'yı 0'dan 1'e yavaş yavaş çıkarmak (KL ısınması, KL
annealing) arka çökmeyi önlemenin bilinen yollarından biri.

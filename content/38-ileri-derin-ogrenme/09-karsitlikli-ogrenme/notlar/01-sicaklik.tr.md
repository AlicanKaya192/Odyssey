NT-Xent'teki `tau` (sıcaklık) benzerlikleri softmax'tan önce böler. Kosinüs
benzerliği -1 ile 1 arasında kalır; `tau = 1` iken logitler de o kadar dar
bir aralıkta olur ve softmax neredeyse düz çıkar. `tau` küçüldükçe aynı
benzerlik farkları büyür ve olasılık en benzer adaylarda toplanır.

```python
import torch
import torch.nn.functional as F


def nt_xent(z1, z2, tau=0.1):
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    sim = z @ z.T / tau
    sim.fill_diagonal_(float("-inf"))
    n = len(z1)
    target = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return F.cross_entropy(sim, target)


gen = torch.Generator().manual_seed(0)
z1 = torch.randn(8, 16, generator=gen)
z2 = z1 + 0.5 * torch.randn(8, 16, generator=gen)
for tau in [1.0, 0.5, 0.1]:
    print(tau, round(nt_xent(z1, z2, tau).item(), 2))
```

```text
1.0 1.85
0.5 1.14
0.1 0.01
```

- Burada eşler (`z2`, `z1`'in gürültülü kopyası) zaten öbürlerinden belirgin
  biçimde benzer. `tau = 1` iken bu fark softmax'ta ezilir ve kayıp yüksek
  kalır; `tau` küçüldükçe eşin olasılığı 1'e yaklaşır ve kayıp düşer.
- Kayıp değerinin kendisi `tau`'lar arasında karşılaştırılamaz; `tau` bir
  ayar (hiperparametre), en iyisi doğrulamayla seçilir. Yayınlarda 0,05 ile
  0,5 arası değerler yaygın.
- Küçük `tau` **zor negatiflere** (eşe en çok benzeyen yabancılara) büyük
  ceza verir. Çok küçük seçilirse eğitim, aslında aynı sınıftan olan iki
  farklı görüntüyü de zorla ayırmaya çalışır: iki farklı daire birbirinin
  negatifidir. Karşıtlıklı öğrenmenin bilinen bir sınırı budur.

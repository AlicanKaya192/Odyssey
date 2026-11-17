Üretici ayırt ediciyi kandırmak için dağılımın **tamamını** öğrenmek
zorunda değildir. Verinin iki öbeği varsa (örneğin -2 ve 2 çevresinde)
yalnızca birini çok iyi taklit etmek de ayırt ediciyi bir süre kandırır. Bu
hâle **mod çöküşü** (mode collapse) denir: üretilen örnekler gerçekçi ama
hep aynı türden. Kayıp bunu göstermez; örneklere bakmak gerekir.

## Öbekleri saymak

Üretilen her örneği en yakın öbek merkezine atayıp her merkezin payını
hesaplayan küçük bir ölçü yeter. Aşağıda biri sağlıklı, biri çökmüş iki
örnek kümesini elle kurduk:

```python
import torch


def mode_share(samples, centers):
    nearest = (samples - torch.tensor(centers)).abs().argmin(dim=1)
    counts = torch.bincount(nearest, minlength=len(centers)).float()
    return (counts / len(samples)).tolist()


gen = torch.Generator().manual_seed(0)
left = -2 + 0.3 * torch.randn(500, 1, generator=gen)
right = 2 + 0.3 * torch.randn(500, 1, generator=gen)
healthy = torch.cat([left, right])
collapsed = 2 + 0.3 * torch.randn(1000, 1, generator=gen)
print(mode_share(healthy, [-2.0, 2.0]))
print(mode_share(collapsed, [-2.0, 2.0]))
```

```text
[0.5, 0.5]
[0.0, 1.0]
```

- `samples` `(N, 1)`, merkezler `(2,)`: çıkarma yayınlamayla `(N, 2)`
  uzaklık tablosu veriyor; `argmin(dim=1)` her örneğin en yakın merkezini
  seçiyor.
- Sağlıklı küme iki öbeğe yarı yarıya dağılmış; çökmüş kümenin tamamı tek
  öbekte. İki kümenin de her örneği "gerçekçi": tek tek bakınca fark
  görünmez, ancak sayınca görünür.

Görüntülerde öbek merkezi yoktur; aynı fikir, üretilen görüntüleri önceden
eğitilmiş bir sınıflandırıcıdan geçirip sınıf dağılımına bakarak uygulanır.

## Çareler

- **Daha küçük öğrenme oranı ve ayırt ediciye zaman:** çöküş çoğu zaman
  oyunun hızlı salınımından doğar.
- **Etiket yumuşatma** (önceki not): ayırt edici aşırı emin olmayınca
  üreticiye daha düzgün bir türev ulaşır.
- **Kayıp değiştirmek:** Wasserstein kaybı gibi alternatifler eğitimi
  sakinleştirmek için önerildi; gradyan cezası (gradient penalty) gibi ek
  terimlerle birlikte kullanılır.
- **Başka bir model ailesi:** Üretken YZ Temelleri modülündeki difüzyon
  modelleri, kararlı eğitimleri ve çeşitlilikleri yüzünden görüntü üretiminde
  GAN'ların yerini büyük ölçüde aldı. GAN'lar hızlı tek adımlı üretim
  gereken yerlerde hâlâ kullanılıyor.

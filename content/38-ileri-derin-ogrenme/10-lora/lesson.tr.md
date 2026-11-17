# LoRA ve Verimli İnce Ayar

Üretken YZ Temelleri modülünde LoRA'yı (low-rank adaptation, düşük ranklı
uyarlama) NumPy ile anlattık. Fikir şu: eğitilmiş bir modeli yeni bir işe
uyarlarken ağırlıkların **değişimi** `ΔW` çoğu zaman düşük ranklıdır; onu
iki ince matrisin çarpımı `B · A` olarak yazabiliriz. Asıl ağırlık `W`
**dondurulur**, yalnızca `A` ve `B` eğitilir. Eğitilen sayı binlerce kat
azalır; taban model bozulmaz, uyarlama ayrı bir küçük dosya olarak takılıp
çıkarılabilir.

<figure class="fig">
<div class="flow">
<span class="node">x</span><span class="arrow">→</span>
<span class="node">W (donmuş)</span><span class="arrow">+</span>
<span class="node acc">B · A (eğitilir)</span><span class="arrow">→</span>
<span class="node">çıkış</span>
</div>
<figcaption>LoRA katmanı: çıkış = W·x + (α/r)·B·A·x. A rank r'lik bir daraltma, B geri genişletme.</figcaption>
</figure>

Bu bölümde aynı fikri PyTorch'ta bir `nn.Module` olarak yazıyoruz: hangi
parametrelerin eğitileceğini `requires_grad` ile seçmek, eğitilen
parametreleri saymak ve sonunda uyarlamayı ağırlığa katmak.

## LoRA katmanı

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_table


class LoRALinear(nn.Module):
    def __init__(self, base, r=4, alpha=8):
        super().__init__()
        self.base = base.requires_grad_(False)
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale


torch.manual_seed(0)
layer = nn.Linear(64, 64)
lora = LoRALinear(layer, r=4)
x = torch.randn(5, 64)
print(torch.equal(lora(x), layer(x)))
trainable = sum(p.numel() for p in lora.parameters() if p.requires_grad)
print(trainable, layer.weight.numel() + layer.bias.numel())
```

```text
True
512 4160
```

- `base.requires_grad_(False)`: taban katmanın ağırlığı ve sapması donar;
  optimizer'a verilse bile değişmez, türev de hesaplanmaz.
- `B` sıfırla başlar: eğitimin başında `B · A = 0`, yani LoRA katmanı taban
  katmanla **birebir aynı** çıktıyı verir. Uyarlama sıfırdan büyür.
- `A` küçük rastgele sayılarla başlar; ikisi birden sıfır olsaydı türev de
  sıfır olur, hiçbiri öğrenmezdi.
- 64 × 64'lük katmanda taban 4160 sayı; rank 4'lük LoRA `4 · 64 + 64 · 4 =
  512` sayı eğitiyor.

## Taban model ve yeni görev

Tablo verisinde (6 özellik, 3 sınıf) bir sınıflandırıcı eğitelim. Yeni
görevde veri aynı türden ama **özelliklerin sırası değişmiş**: bir sensörün
kabloları yer değiştirmiş gibi. Taban model bunu bilmiyor.

```python
xa, ya = map(torch.tensor, make_table(800, seed=7))
xb, yb = map(torch.tensor, make_table(800, seed=8))
xb = xb[:, [1, 0, 2, 5, 4, 3]]


def fit(model, x, y, epochs=30, lr=0.01):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=lr)
    gen = torch.Generator().manual_seed(1)
    for _ in range(epochs):
        perm = torch.randperm(600, generator=gen)
        for i in range(0, 600, 50):
            idx = perm[i:i + 50]
            opt.zero_grad()
            F.cross_entropy(model(x[idx]), y[idx]).backward()
            opt.step()


def accuracy(model, x, y):
    with torch.no_grad():
        return (model(x[600:]).argmax(1) == y[600:]).float().mean().item()


torch.manual_seed(0)
net = nn.Sequential(nn.Linear(6, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(),
                    nn.Linear(64, 3))
fit(net, xa, ya)
acc_a = accuracy(net, xa, ya)
print(round(acc_a, 1), round(accuracy(net, xb, yb), 1))
```

```text
0.8 0.5
```

- İlk 600 satır eğitim, son 200 test.
- Taban model kendi görevinde iyi; yeni görevde neredeyse yarı yarıya
  yanılıyor.
- `fit` yalnızca `requires_grad` olan parametreleri optimizer'a veriyor;
  aşağıda bunun önemini göreceğiz.

## LoRA ile ince ayar

Bütün ağı donduruyor, yalnızca ilk katmanı rank 2'lik bir LoRA katmanıyla
sarıyoruz.

```python
net.requires_grad_(False)
net[0] = LoRALinear(net[0], r=2)
fit(net, xb, yb)
trainable = sum(p.numel() for p in net.parameters() if p.requires_grad)
total = sum(p.numel() for p in net.parameters())
print(trainable, total)
print(accuracy(net, xb, yb) > 0.8)
plain = nn.Sequential(net[0].base, *net[1:])
print(accuracy(plain, xa, ya) == acc_a)
```

```text
140 4943
True
True
```

- Eğitilen yalnızca 140 sayı (`2 · 6 + 64 · 2`); modelin tamamı 4943. Yüzde
  üçten az.
- Yeni görevde doğruluk 0,8'in üstüne çıktı: özelliklerin sırasındaki
  değişim ilk katmanda düşük ranklı bir düzeltmeyle karşılanabiliyor.
- Son satır: uyarlamayı çıkarıp taban katmanı kullanınca eski görevdeki
  doğruluk **birebir aynı**. Taban ağırlıklar hiç değişmedi.

## Uyarlamayı ağırlığa katmak

Sunarken her çağrıda iki yol (`W·x` ve `B·A·x`) hesaplamak gereksiz. Eğitim
bitince `W' = W + (α/r) · B · A` tek bir ağırlık olarak yazılır; çıkış aynı,
hız taban modelinkiyle aynı.

```python
def merge(lora):
    merged = nn.Linear(lora.base.in_features, lora.base.out_features)
    with torch.no_grad():
        merged.weight.copy_(lora.base.weight + lora.scale * lora.B @ lora.A)
        merged.bias.copy_(lora.base.bias)
    return merged


merged_net = nn.Sequential(merge(net[0]), *net[1:])
with torch.no_grad():
    print(torch.allclose(merged_net(xb), net(xb), atol=1e-5))
```

```text
True
```

`allclose` kullanmamızın nedeni: iki yol aynı hesabı farklı sırada yapıyor;
kayan nokta toplamında sıra son basamakları değiştirebilir.

## Özet

- LoRA: `W` donmuş, `ΔW = B · A` eğitilir; `B` sıfırla başlar, başlangıçta
  çıkış taban modelinki.
- PyTorch'ta dondurmak `requires_grad_(False)`; optimizer'a yalnızca
  `requires_grad` olanları ver.
- Eğitilen parametre sayısı `r · (giriş + çıkış)`.
- Uyarlama çıkarılınca taban model eski hâlinde.
- Sunmadan önce `W + (α/r)·B·A` ile ağırlığa katılabilir.

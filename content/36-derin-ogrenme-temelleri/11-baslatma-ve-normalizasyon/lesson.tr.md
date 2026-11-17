# Ağırlık Başlatma ve Normalizasyon

Ağ derinleştikçe yeni bir sorun çıkar: sinyal katmanlardan geçerken
büyüyebilir ya da sönebilir. Her katman girdisini bir matrisle çarpıyor;
çarpanlar biraz büyükse on katmanda sayılar patlar, biraz küçükse sıfıra
iner. Gradyanlar da geri yayılımda aynı yolu tersinden yürüdüğü için aynı
kaderi paylaşır. Bu bölümde iki çareyi göreceğiz: ağırlıkları **doğru
ölçekte başlatmak** ve katmanların arasına **normalizasyon** katmanı koymak.

## On katmanda sinyal

Rastgele bir girdiyi, ağırlıkları farklı biçimlerde başlatılmış on
`Linear + ReLU` katmanından geçirip çıktının standart sapmasına bakalım.
Sayılar çok büyük ya da çok küçük olabileceği için onluk logaritmasını
yazdırıyoruz (`3` → bin, `−3` → binde bir):

```python
import math

import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(512, 256)


def depth_test(init):
    torch.manual_seed(1)
    h = x
    for _ in range(10):
        layer = nn.Linear(256, 256, bias=False)
        init(layer.weight)
        h = torch.relu(layer(h))
    return h.std().item()


for name, init in [("std 1.0", lambda w: nn.init.normal_(w, std=1.0)),
                   ("std 0.01", lambda w: nn.init.normal_(w, std=0.01)),
                   ("kaiming", lambda w: nn.init.kaiming_normal_(w, nonlinearity="relu")),
                   ("default", lambda w: None)]:
    print(name, round(math.log10(depth_test(init)), 1))
```

```text
std 1.0 10.4
std 0.01 -9.6
kaiming -0.1
default -3.9
```

- Standart sapması 1 olan ağırlıklarla çıktı 10¹⁰ mertebesinde: patladı.
  0,01 ile 10⁻¹⁰ mertebesinde: söndü. İkisinde de gradyanlar ya taşar ya
  kaybolur; ağ öğrenemez.
- **Kaiming (He) başlatması** standart sapmayı girdi sayısına göre seçer:
  `sqrt(2 / girdi)`. ReLU sinyalin yarısını sıfırladığı için 2 çarpanı onu
  telafi ediyor; sinyal on katman sonra da 1 civarında (log ≈ 0).
- PyTorch'un `nn.Linear` için varsayılan başlatması tek katmanda iyi ama
  derin ReLU yığınında sinyali yavaş yavaş küçültüyor (10⁻⁴). Derin ve ReLU'lu
  ağlarda başlatmayı açıkça Kaiming yapmak iyi bir alışkanlık.

<figure class="fig">
  <div class="versus">
    <div class="no"><h5>Çok büyük / çok küçük</h5>Sinyal katman katman büyür ya da söner; gradyanlar taşar ya da kaybolur.</div>
    <div class="ok"><h5>Kaiming / Xavier</h5>Ölçek girdi sayısına göre seçilir; sinyal derinlik boyunca aynı büyüklükte kalır.</div>
  </div>
  <figcaption>ReLU'lu ağlarda Kaiming (<code>kaiming_normal_</code>), tanh/sigmoid'li ağlarda Xavier (<code>xavier_normal_</code>).</figcaption>
</figure>

## BatchNorm

Başlatma yalnızca **başlangıcı** düzeltir; eğitim ilerledikçe katmanların
girdileri yine kayabilir. **Batch normalizasyonu** (BatchNorm) her
özelliği, o kümedeki örneklerin ortalamasını çıkarıp standart sapmasına
bölerek normalleştirir; sonra öğrenilen bir ölçek ve kayma uygular.

```python
bn = nn.BatchNorm1d(3)
batch = torch.tensor([[1.0, 100.0, -5.0], [3.0, 300.0, -5.5],
                      [5.0, 200.0, -4.5], [7.0, 400.0, -5.0]])
out = bn(batch)
print([round(v, 3) + 0.0 for v in out.mean(dim=0).tolist()])
print([round(v, 3) for v in out.std(dim=0, unbiased=False).tolist()])
print([round(v, 1) for v in bn.running_mean.tolist()])
```

```text
[0.0, 0.0, 0.0]
[1.0, 1.0, 1.0]
[0.4, 25.0, -0.5]
```

- Üç sütun bambaşka ölçeklerdeydi (birler, yüzler, eksi beşler); her
  sütunun ortalaması 0, standart sapması 1 oldu.
- `running_mean` eğitim boyunca görülen ortalamaların yürüyen ortalaması;
  0'dan başladı ve bu kümenin ortalamalarına doğru onda bir (momentum 0,1)
  ilerledi: 4 → 0,4, 250 → 25.
  Değerlendirmede (`eval()`) kümenin değil bu kayıtlı değerlerin
  kullanılmasının sebebi: tahmin yaparken tek bir örnek bile gelebilir ve
  sonuç kümedeki öteki örneklere bağlı olmamalı.

## BatchNorm'un etkisi

Sigmoid kullanan sekiz katmanlı derin bir ağı aynı ayarlarla bir kez
BatchNorm'suz, bir kez her katmanın arkasında BatchNorm ile eğitelim:

```python
from dl_data import make_table

x_np, y_np = make_table(1000)
X, Y = torch.from_numpy(x_np), torch.from_numpy(y_np)


def deep_net(batch_norm):
    torch.manual_seed(0)
    layers, n_in = [], 6
    for _ in range(8):
        layers.append(nn.Linear(n_in, 32))
        if batch_norm:
            layers.append(nn.BatchNorm1d(32))
        layers.append(nn.Sigmoid())
        n_in = 32
    return nn.Sequential(*layers, nn.Linear(32, 3))


for batch_norm in [False, True]:
    model = deep_net(batch_norm)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        loss = loss_fn(model(X[:800]), Y[:800])
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        accuracy = (model(X[800:]).argmax(dim=1) == Y[800:]).float().mean().item()
    print(batch_norm, round(loss.item(), 2), round(100 * accuracy, 1))
```

```text
False 1.1 33.5
True 0.35 88.5
```

- BatchNorm'suz ağ hiç öğrenemedi: kayıp `log 3 ≈ 1,10`'da takıldı, test
  doğruluğu %33,5 (üç sınıflı veride tek sınıfı söylemek
  kadar). Sekiz sigmoid'den geçen gradyan neredeyse sıfıra iniyor
  (**sönen gradyan**, vanishing gradient).
- BatchNorm'lu aynı ağ, aynı öğrenme oranıyla öğrendi: test doğruluğu
  %88,5.

## LayerNorm

BatchNorm kümedeki örneklere bakar; küme çok küçükse ya da örnekler
farklı uzunlukta dizilerse (metin) zorlanır. **LayerNorm** her örneği kendi
içinde, özellikleri üzerinden normalleştirir; kümeye bağlı değildir:

```python
ln = nn.LayerNorm(3)
out = ln(batch)
print([round(v, 2) for v in out[0].tolist()])
print([round(v, 3) + 0.0 for v in out.mean(dim=1).tolist()])
```

```text
[-0.64, 1.41, -0.77]
[0.0, 0.0, 0.0, 0.0]
```

Her **satırın** ortalaması 0 oldu. (`+ 0.0`, yuvarlanınca `-0.0` çıkan çok
küçük negatif sayıları düz `0.0` yazdırmak için.) Transformer'larda (İleri Derin Öğrenme
modülü) her yerde LayerNorm kullanılıyor; görüntü ağlarında BatchNorm
yaygın.

## Özet

- Ağırlık ölçeği yanlışsa sinyal derinlikte patlar ya da söner.
- ReLU'lu derin ağlarda `nn.init.kaiming_normal_`.
- BatchNorm her özelliği kümede normalleştirir; eğitimde kümenin,
  değerlendirmede kayıtlı ortalamaları kullanır. Derin ağların eğitimini
  kolaylaştırır.
- LayerNorm her örneği kendi içinde normalleştirir; kümeye bağlı değil.

# Optimizasyon Algoritmaları

Gradyan inişi parametreyi gradyanın tersine küçük bir adım kaydırıyordu:
`w ← w − lr · gradyan`. Bu kuralın bir zayıflığı var: her yönde aynı
öğrenme oranını kullanıyor. Kaybın bir yönde dik, öbür yönde yatık olduğu
(ki sinir ağlarında hep böyledir) durumlarda ya dik yönde zıplıyor ya yatık
yönde sürünüyor. Bu bölümde PyTorch'un optimizer'larını (`SGD`, momentumlu
`SGD`, `Adam`) bu zayıflık üzerinden karşılaştıracağız.

## Uzun bir çukur

İki parametreli bir kayıp düşünelim: `10·w₁² + w₂²`. En iyi nokta `(0, 0)`.
`w₁` yönünde çukur on kat daha dik. Bir optimizer'ı 50 adım çalıştırıp
kalan kaybı veren küçük bir fonksiyon yazalım:

```python
import torch


def bowl(w):
    return 10 * w[0] ** 2 + w[1] ** 2


def run(make_optimizer, steps=50):
    w = torch.tensor([1.0, 1.0], dtype=torch.float64, requires_grad=True)
    optimizer = make_optimizer([w])
    for _ in range(steps):
        optimizer.zero_grad()
        bowl(w).backward()
        optimizer.step()
    return bowl(w).item()


for lr in [0.01, 0.09, 0.11]:
    loss = run(lambda p: torch.optim.SGD(p, lr=lr))
    print("SGD", lr, round(loss, 3) if loss < 1000 else "> 1000")
```

```text
SGD 0.01 0.133
SGD 0.09 0.0
SGD 0.11 > 1000
```

- `lr = 0.01`: dik yön (`w₁`) çabucak bitiyor ama yatık yön (`w₂`) 50
  adımda hâlâ yolda; kayıp 0,133.
- `lr = 0.09`: iyi; ama dik yönde her adım çukurun öbür yanına geçiyor
  (zikzak).
- `lr = 0.11`: dik yön ıraksıyor, kayıp patlıyor. SGD için öğrenme oranının
  üst sınırını **en dik yön** belirliyor; yatık yön de o yüzden yavaş.

## Momentum

**Momentum** gradyanı doğrudan kullanmak yerine bir **hız** biriktirir:
her adımda hız, önceki hızın büyük kısmı artı yeni gradyan. Aynı yönü
gösteren gradyanlar birikip hızlanır; zikzak yapan gradyanlar birbirini
söndürür.

```python
for momentum in [0.0, 0.9]:
    loss = run(lambda p: torch.optim.SGD(p, lr=0.01, momentum=momentum))
    print("momentum", momentum, round(loss, 3))
```

```text
momentum 0.0 0.133
momentum 0.9 0.015
```

Aynı küçük öğrenme oranıyla momentum yatık yönde çok daha hızlı ilerledi:
kayıp yaklaşık 9 kat küçük. `momentum=0.9` en yaygın değer.

## Adam

**Adam** iki fikri birleştirir: momentum gibi gradyanın ortalamasını
tutar, ayrıca her parametre için gradyanın büyüklüğünün ortalamasını tutup
adımı ona böler. Böylece her parametre **kendi ölçeğinde** ilerler: dik
yönde adım küçülür, yatık yönde büyür.

```python
for lr in [0.01, 0.1]:
    print("Adam", lr, round(run(lambda p: torch.optim.Adam(p, lr=lr)), 3))
```

```text
Adam 0.01 3.17
Adam 0.1 0.0
```

- `lr = 0.1` ile Adam yatık yönü de kısa sürede bitirdi.
- `lr = 0.01` ile yavaş: Adam'da bir adım kabaca öğrenme oranı
  büyüklüğünde, gradyan ne olursa olsun. 50 adımda en fazla yaklaşık 0,5
  yol alınabiliyor. Adam'ın öğrenme oranı "parametre başına adım
  büyüklüğü" gibi okunur.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>SGD(lr)</code></span><span>Adım = lr · gradyan. Basit, bellek istemez; öğrenme oranını en dik yön sınırlar.</span></div>
    <div class="anat-row"><span><code>SGD(lr, momentum=0.9)</code></span><span>Gradyanlardan bir hız biriktirir; zikzağı söndürür, yatık yönde hızlanır.</span></div>
    <div class="anat-row"><span><code>Adam(lr)</code></span><span>Her parametrenin adımını kendi gradyan büyüklüğüne göre ayarlar. Çoğu problemde iyi bir başlangıç; tipik lr 0,001–0,01.</span></div>
  </div>
  <figcaption>Üç optimizer'ın özeti.</figcaption>
</figure>

## Gerçek bir ağda

Aynı karşılaştırmayı giriş bölümündeki rakam ağıyla yapalım: iki optimizer,
40 tur, aynı başlangıç ağırlıkları.

```python
from torch import nn
from sklearn.datasets import load_digits

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)


def train(make_optimizer, epochs=40):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
    optimizer = make_optimizer(model.parameters())
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(X[:1200]), y[:1200])
        loss.backward()
        optimizer.step()
    return loss.item()


print("SGD ", round(train(lambda p: torch.optim.SGD(p, lr=0.1)), 2))
print("Adam", round(train(lambda p: torch.optim.Adam(p, lr=0.01)), 2))
```

```text
SGD  2.11
Adam 0.16
```

40 turda SGD'nin kaybı hâlâ yüksek, Adam'ınki çok daha aşağıda. Bu, Adam'ın
her zaman daha iyi olduğu demek değil: iyi ayarlanmış momentumlu SGD birçok
görüntü modelinde sonunda Adam kadar, bazen ondan iyi sonuç verir. Ama
Adam az ayarla hızlı başlar; bu modülde çoğunlukla onu kullanacağız.

## Özet

- SGD her yönde aynı öğrenme oranını kullanır; en dik yön sınırı koyar,
  yatık yönler yavaş kalır.
- Momentum gradyanlardan hız biriktirir; zikzağı söndürür.
- Adam her parametrenin adımını kendi ölçeğine göre ayarlar; lr ≈ adım
  büyüklüğü.
- Optimizer değişse de eğitim döngüsü aynı: `zero_grad`, `backward`,
  `step`.

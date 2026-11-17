# Öğrenme Oranı Planlama ve Gradyan Kırpma

Şimdiye kadar öğrenme oranı (learning rate) eğitim boyunca sabitti. Oysa
iyi bir eğitim çoğu zaman iki evreden geçer: başta büyük adımlarla hızla
iyi bir bölgeye yaklaşmak, sonda küçük adımlarla oraya oturmak. Sabit ve
büyük bir oran sonda modelin çukurun dibinde bir o yana bir bu yana
sekmesine yol açar; sabit ve küçük bir oran ise baştan yavaştır. Bu bölümde
oranı eğitim boyunca değiştiren **zamanlayıcıları** (scheduler) ve tek bir
büyük gradyanın modeli bozmasını önleyen **gradyan kırpmayı** (gradient
clipping) görüyoruz.

## Zamanlayıcı: StepLR

Zamanlayıcı bir optimizer'ı sarar ve her `step()` çağrısında onun öğrenme
oranını bir kurala göre değiştirir. Optimizer'ın o anki oranı
`optimizer.param_groups[0]["lr"]` içinde durur. Zamanlayıcılar
`torch.optim.lr_scheduler` modülünde. `StepLR` her `step_size` turda oranı
`gamma` ile çarpar:

```python
import torch
from torch import nn
from torch.optim import lr_scheduler

w = nn.Parameter(torch.zeros(1))
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
rates = []
for epoch in range(8):
    rates.append(optimizer.param_groups[0]["lr"])
    optimizer.step()
    scheduler.step()
print(rates)
```

```text
[0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025]
```

- İlk üç tur 0,1, sonraki üç tur 0,05, sonra 0,025: oran basamak basamak
  iniyor.
- Sıra önemli: önce `optimizer.step()` (bu turun adımı), sonra
  `scheduler.step()` (bir sonraki turun oranı). Burada gradyan olmadığı
  için adım hiçbir şeyi değiştirmiyor; yalnızca oranları görmek için var.

## Kosinüs planı

`CosineAnnealingLR` oranı basamaksız, kosinüs eğrisi boyunca `T_max` turda
sıfıra indirir: başta yavaş, ortada hızlı, sonda yine yavaş.

```python
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=8)
rates = []
for epoch in range(9):
    rates.append(round(optimizer.param_groups[0]["lr"], 3))
    optimizer.step()
    scheduler.step()
print(rates)
```

```text
[0.1, 0.096, 0.085, 0.069, 0.05, 0.031, 0.015, 0.004, 0.0]
```

Ortadaki turda (4.) oran tam yarıya, 0,05'e iniyor; 8. turda sıfır.
Formülü: `lr · (1 + cos(π · tur / T_max)) / 2`.

## Isınma (warmup)

Bazen tam tersi gerekir: eğitimin en başında ağırlıklar rastgele, gradyanlar
düzensizdir ve büyük bir oran ilk adımlarda modeli bozabilir. **Isınma**
oranı küçük başlatıp birkaç turda asıl değerine çıkarır. `LinearLR` bunu
yapar:

```python
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.LinearLR(optimizer, start_factor=0.25,
                                  total_iters=3)
rates = []
for epoch in range(6):
    rates.append(round(optimizer.param_groups[0]["lr"], 4))
    optimizer.step()
    scheduler.step()
print(rates)
```

```text
[0.025, 0.05, 0.075, 0.1, 0.1, 0.1]
```

Oran 0,1'in dörtte birinden başladı, üç turda 0,1'e çıktı ve orada kaldı.
Büyük modellerde ısınma ile kosinüs çoğu zaman art arda kullanılır.

<figure class="fig">
  <div class="versus">
    <div><h5>StepLR</h5>Her birkaç turda bir oranı sabit bir katsayıyla çarpar; basamaklı iner.</div>
    <div><h5>CosineAnnealingLR</h5>Oranı kosinüs eğrisiyle yumuşakça sıfıra indirir.</div>
    <div><h5>LinearLR (ısınma)</h5>Oranı küçük başlatıp birkaç turda asıl değerine çıkarır.</div>
  </div>
  <figcaption>Üçü de aynı kalıpla kullanılır: optimizer'ı sar, her turun sonunda <code>scheduler.step()</code>.</figcaption>
</figure>

## Etkisi

Tablo verisinde küçük bir ağı **büyük** bir oranla (1,0) 60 tur eğitelim;
bir kez sabit oranla, bir kez StepLR ile, bir kez kosinüsle. Her eğitimin
sonunda son beş turun eğitim kaybındaki **oynamayı** (en büyük − en küçük)
ve test doğruluğunu yazdıralım:

```python
from dl_data import make_table

x_np, y_np = make_table(1000)
X, Y = torch.from_numpy(x_np), torch.from_numpy(y_np)
loss_fn = nn.CrossEntropyLoss()


def train(make_scheduler):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, 3))
    optimizer = torch.optim.SGD(model.parameters(), lr=1.0)
    scheduler = make_scheduler(optimizer)
    generator = torch.Generator().manual_seed(0)
    history = []
    for epoch in range(60):
        order = torch.randperm(800, generator=generator)
        for start in range(0, 800, 32):
            idx = order[start:start + 32]
            optimizer.zero_grad()
            loss_fn(model(X[idx]), Y[idx]).backward()
            optimizer.step()
        if scheduler is not None:
            scheduler.step()
        with torch.no_grad():
            history.append(loss_fn(model(X[:800]), Y[:800]).item())
    with torch.no_grad():
        hits = model(X[800:]).argmax(dim=1) == Y[800:]
    accuracy = hits.float().mean().item()
    last = history[-5:]
    return round(max(last) - min(last), 2), round(100 * accuracy, 1)


schedules = {
    "constant": lambda opt: None,
    "step": lambda opt: lr_scheduler.StepLR(opt, 20, gamma=0.1),
    "cosine": lambda opt: lr_scheduler.CosineAnnealingLR(opt, 60),
}
for name, make in schedules.items():
    print(name, train(make))
```

```text
constant (0.05, 82.0)
step (0.0, 88.5)
cosine (0.0, 88.0)
```

- Sabit oranda son turların kaybı 0,05 kadar oynuyor: model
  dibe oturamıyor, her tur başka bir yere sekiyor. Test doğruluğu
  %82,0.
- İki planda da oran sonda küçüldüğü için kayıp oturdu (oynama sıfıra yakın)
  ve test doğruluğu %88,5 ile %88,0 oldu.
- Bu, aynı başlangıç oranıyla yalnızca **sonu** değiştirmenin kazancı. Plan,
  büyük oranın hızından vazgeçmeden sonda küçük oranın inceliğini veriyor.

## Gradyan kırpma

Bazen tek bir kümede gradyan çok büyük çıkar: ölçeklenmemiş bir özellik,
uç bir örnek ya da derin bir ağ yüzünden. Optimizer o gradyanla dev bir
adım atar ve model bir anda bozulur. **Gradyan kırpma** bütün
parametrelerin gradyanlarını tek bir vektör gibi düşünür; bu vektörün
uzunluğu (normu) bir sınırı aşarsa vektörü o sınıra kısaltır, yönünü
değiştirmez:

```python
torch.manual_seed(0)
layer = nn.Linear(3, 1)
loss = (layer(torch.tensor([[100.0, 200.0, -50.0]])) - 1).pow(2).sum()
loss.backward()
norm = nn.utils.clip_grad_norm_(layer.parameters(), max_norm=1.0)
after = torch.sqrt(sum(p.grad.pow(2).sum() for p in layer.parameters()))
print(round(norm.item()), round(after.item(), 4))
```

```text
38423 1.0
```

- `clip_grad_norm_` kırpmadan **önceki** normu döndürüyor: 38423.
  Kırpmadan sonra norm tam 1.
- Kırpma `backward()` ile `optimizer.step()` arasına yazılır: gradyan
  hesaplandıktan sonra, kullanılmadan önce.

Etkisini görmek için ölçeklenmemiş bir özellikle (0 ile 100 arası)
`y = 3x + 2` doğrusunu öğrenelim:

```python
import math

torch.manual_seed(0)
x = torch.rand(100, 1) * 100
y = 3 * x + 2
for clip in [None, 1.0]:
    torch.manual_seed(1)
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    for step in range(300):
        optimizer.zero_grad()
        ((model(x) - y) ** 2).mean().backward()
        if clip is not None:
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip)
        optimizer.step()
    weight = model.weight.item()
    if math.isfinite(weight):
        weight = round(weight, 1)
    print(clip, weight)
```

```text
None nan
1.0 3.0
```

- Kırpmasız eğitim ilk adımlarda ıraksadı ve ağırlık `nan` oldu.
- Aynı oranla kırpılmış eğitim ağırlığı 3'e getirdi. Her adımın boyu en çok
  `lr · max_norm` olduğu için model kontrolden çıkamadı.
- Kırpma ölçeklemenin yerini tutmaz (sabit terim bu sürede tam öğrenilemedi),
  ama ara sıra gelen büyük gradyana karşı ucuz bir sigortadır. Yinelemeli
  ağlarda (ileri modül) neredeyse her zaman kullanılır.

## Özet

- Zamanlayıcı optimizer'ın öğrenme oranını eğitim boyunca değiştirir:
  `StepLR` basamaklı, `CosineAnnealingLR` yumuşak, `LinearLR` ısınma.
- Sıra: `optimizer.step()`, sonra `scheduler.step()`.
- Büyük oranla başlayıp sonda küçültmek, kaybın dibe oturmasını sağlar.
- `nn.utils.clip_grad_norm_` gradyanların toplam normunu sınırlar;
  `backward()` ile `step()` arasına yazılır.
